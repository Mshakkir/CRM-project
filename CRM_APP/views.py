from django.core.paginator import Paginator
from django.shortcuts import render,get_object_or_404,redirect
from django.http import HttpResponseForbidden,HttpResponseRedirect
from .models import Ticket
import openpyxl
from django.http import HttpResponse
from django.contrib import messages
from django.core.mail import send_mail
from django.http import HttpResponse, JsonResponse
from django.views.decorators.csrf import csrf_protect
from .models import *
from django.contrib.auth import authenticate, login
from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
import random
from datetime import datetime
from django.urls import reverse_lazy, reverse
from django.views.generic import DeleteView
from .forms import DoctorForm
from django.db.models import Q



# def home(request):
#     return render(request,'login.html')


@login_required
def dashboard_view(request):
    current_date = datetime.now().strftime("%B %d, %Y")
    total_interested = interaction.objects.filter(
        Q(payment=True) |
        Q(next_follow_up__isnull=False) |
        Q(next_calling__isnull=False) |
        Q(call_later__isnull=False)
    ).count()
    total_closed = interaction.objects.filter(payment__isnull=False).count()
    total_leads = lead.objects.count()
    
    if total_leads > 0:
        percentage = ((total_interested + total_closed) / total_leads) * 100
        successful_calls = (total_interested / total_leads) * 100
        sales_services = (total_closed / total_leads) * 100
    else:
        percentage = 0
        successful_calls = 0
        sales_services = 0

    return render(request, 'dashboard.html', {
        'email': request.user.email.split('@')[0],
        'date': current_date,
        'successful_calls': successful_calls,
        'sales_services': sales_services,
        'total': total_leads,
        'remaining': total_leads - (total_interested + total_closed),
        'percentage': percentage
    })


def generate_otp():
    """Generate a 4-digit OTP."""
    return random.randint(1000, 9999)

def send_otp_email(user_email):
    """Send an OTP email to the user."""
    try:
        otp = generate_otp()  # Generate the OTP
        subject = 'Your Password Reset OTP'
        message = f'Your OTP is: {otp}. It is valid for 10 minutes.'
        from_email = 'crmbde@gmail.com'

        # Send the email
        send_mail(subject, message, from_email, [user_email])

        return otp
    except Exception as e:
        print(f"Error sending email: {e}")
        return None  # Return None if the email fails


def forgot_pass(request):
    """Handle the forgot password flow."""
    if request.method == 'POST':
        user_email = request.POST.get('email')  # Get the email from the form

        if user_email:
            otp = send_otp_email(user_email)  # Attempt to send OTP email
            if otp:
                # Save the OTP and email in the session for validation
                request.session['otp'] = otp
                request.session['user_email'] = user_email
                messages.success(request, 'OTP sent successfully to your email!')

                # Redirect to the OTP verification page
                return redirect('otp_verification')  # Use the name of the OTP verification route
            else:
                # Email sending failed
                messages.error(request, 'Failed to send OTP. Please try again later.')
        else:
            # Email field is empty or invalid
            messages.error(request, 'Please enter a valid email address.')

    return render(request, 'forgotpassword.html')

def otp_verification(request):
    """Handle OTP verification."""
    if request.method == 'POST':
        user_otp = request.POST.get('otp')  # Get the OTP entered by the user
        session_otp = request.session.get('otp')  # Get the OTP stored in the session

        if user_otp and session_otp and int(user_otp) == session_otp:
            # OTP is correct
            messages.success(request, 'OTP verified successfully! You can reset your password.')
            
            # Redirect to the password reset page
            return redirect('resetpassword')  # Replace with your password reset route
        else:
            # OTP is incorrect or missing
            messages.error(request, 'Invalid OTP. Please try again.')
    return render(request, 'verifycode.html')

    

@csrf_protect
def reset_password(request):
    if request.method == 'POST':
        password = request.POST.get('password')
        confirm_password = request.POST.get('confirm_password')
        user_email = request.session.get('user_email')  # Get the email from the session

        if password and confirm_password and password == confirm_password:
            try:
                user = User.objects.get(email=user_email)
                user.password = make_password(password)
                user.save()
                messages.success(request, 'Password reset successfully! You can now log in.')
                return redirect('login')
            except User.DoesNotExist:
                messages.error(request, 'User does not exist.')
        else:
            messages.error(request, 'Passwords do not match. Please try again.')

    return render(request, 'resetpassword.html')


def new_leads(request):
    if request.method == 'POST':
        # Lid = request.POST.get('Lid')
        state = request.POST.get('state')
        specialization = request.POST.get('specialization')
        assigned = request.POST.get('assigned', 'assigned')
        mode = request.POST.get('mode')
        name = request.POST.get('name')
        address = request.POST.get('address')
        position = request.POST.get('position')
        city = request.POST.get('city')
        email = request.POST.get('email')
        website = request.POST.get('website')
        country = request.POST.get('country')
        phone = request.POST.get('phone')
        zipcode = request.POST.get('zipcode')
        clinic_name = request.POST.get('clinic_name')
        default_language = request.POST.get('default_language')
        priority = request.POST.get('priority')
        notes = request.POST.get('notes')
        status = request.POST.get('status')
        default_doctor = doctor.objects.first()

        lead_obj = lead(
            # Lid=Lid,
            state=state,
            specialization=specialization,
            assigned=assigned,
            mode=mode,
            name=name,
            address=address,
            position=position,
            city=city,
            email=email,
            website=website,
            country=country,
            phone=phone,
            zipcode=zipcode,
            clinic_name=clinic_name,
            default_language =default_language,
            priority=priority,
            notes=notes,
            status=status,
            doctors=default_doctor

        )
        lead_obj.save()
        messages.success(request, 'Lead added successfully!')
        return redirect('leads')    

    return render(request, 'newleads.html')


def leads_view(request):

    Leads = lead.objects.all()

    # Get filter values from the request
    assigned_filter = request.GET.get('assigned', '')  # Default to empty string if not provided
    status_filter = request.GET.get('status', '')  # Default to empty string if not provided
    mobile_filter = request.GET.get('phone', '')  # Default to empty string if not provided
    specialization_filter = request.GET.get('specialization', '')

    # Start with all tickets
    lead_list = lead.objects.all()

    # Apply filters
    if assigned_filter:
        lead_list = lead_list.filter(assigned=assigned_filter)
    if status_filter:
        lead_list = lead_list.filter(status=status_filter)
    if specialization_filter:
        lead_list = lead_list.filter(specialization=specialization_filter)    
    if mobile_filter:
        lead_list = lead_list.filter(phone__icontains=mobile_filter)  # Partial match for mobile


    paginator = Paginator(lead_list, 8)  # Show 8 leads per page
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    context = {
        'leads': page_obj,
        'assigned': assigned_filter,
        'status': status_filter,
        'specialization': specialization_filter,
        'phone': mobile_filter,
    }
    
        
    return render(request, 'leads.html',context)    




def edit_lead(request, lead_id):
    Lead = get_object_or_404(lead, id=lead_id)
    if request.method == 'POST':
        assigned = request.POST.get('assigned')
        name = request.POST.get('name')
        clinic_name = request.POST.get('clinic_name')
        phone = request.POST.get('phone')
        email = request.POST.get('email')
        state = request.POST.get('state')
        specialization = request.POST.get('specialization')
        mode = request.POST.get('mode')
        address = request.POST.get('address')
        position = request.POST.get('position')
        city = request.POST.get('city')
        website = request.POST.get('website')
        country = request.POST.get('country')
        zipcode = request.POST.get('zipcode')
        clinic_name = request.POST.get('clinic_name')
        default_language = request.POST.get('default_language')
        priority = request.POST.get('priority')
        notes = request.POST.get('notes')

        
       
        Lead.assigned = assigned
        Lead.name = name
        Lead.clinic_name = clinic_name
        Lead.email = email
        Lead.phone = phone
        Lead.state = state
        Lead.specialization = specialization
        Lead.mode = mode
        Lead.address = address
        Lead.position = position
        Lead.city = city
        Lead.website = website
        Lead.country = country
        Lead.zipcode = zipcode
        Lead.default_language = default_language
        Lead.priority = priority
        Lead.notes = notes
       

        Lead.save()
        
        return redirect('leads')
    return render(request, 'edit_leads.html', {'lead': Lead})


def delete_lead(request, id):
    lead.objects.filter(id=id).delete()
    return redirect('leads')


def login_view(request):
    if request.method == "POST":
        email = request.POST.get('email')
        password = request.POST.get('password')

        if not email or not password:
            messages.error(request, "Please fill out both fields.")
            return render(request, 'login.html')

        user = authenticate(request, username=email, password=password)
        if user is not None:
            login(request, user)
            messages.success(request, "Login successful")
            return redirect("dashboard")
        else:
            messages.error(request, "Invalid email or password")
            return render(request, 'login.html')

    return render(request, 'login.html')




def forgot_password(request):
    """Handle the forgot password flow."""
    if request.method == 'POST':
        user_email = request.POST.get('email')  # Get the email from the form

        if user_email:
            otp = send_otp_email(user_email)  # Attempt to send OTP email
            if otp:
                # Save the OTP and email in the session for validation
                request.session['otp'] = otp
                request.session['user_email'] = user_email
                messages.success(request, 'OTP sent successfully to your email!')

                # Redirect to the OTP verification page
                return redirect('otp_verification')  # Use the name of the OTP verification route
            else:
                # Email sending failed
                messages.error(request, 'Failed to send OTP. Please try again later.')
        else:
            # Email field is empty or invalid
            messages.error(request, 'Please enter a valid email address.')

    return render(request, 'forgotpassword.html')


def about(request):
    return render(request, 'about.html')

def ticket_view(request):
    # Get filter values from the request
    assigned_filter = request.GET.get('assigned', '')  # Default to empty string if not provided
    status_filter = request.GET.get('status', '')  # Default to empty string if not provided
    mobile_filter = request.GET.get('mobile', '')  # Default to empty string if not provided

    # Start with all tickets
    tickets_list = Ticket.objects.all()

    # Apply filters
    if assigned_filter:
        tickets_list = tickets_list.filter(assign_ticket=assigned_filter)
    if status_filter:
        tickets_list = tickets_list.filter(status=status_filter)
    if mobile_filter:
        tickets_list = tickets_list.filter(contact__icontains=mobile_filter)  # Partial match for mobile

    # Pagination
    paginator = Paginator(tickets_list, 5)  # Show 5 tickets per page
    page_number = request.GET.get('page')
    tickets = paginator.get_page(page_number)

    # Fetch unique values for the "Assigned" filter
    assigned_values = Ticket.objects.values_list('assign_ticket', flat=True).distinct()

    # Calculate ticket counts based on status, applying the same filters
    ticket_counts = {
        'open': tickets_list.filter(status='Open').count(),
        'in_progress': tickets_list.filter(status='In Progress').count(),
        'on_hold': tickets_list.filter(status='On Hold').count(),
        'answered': tickets_list.filter(status='Answered').count(),
        'closed': tickets_list.filter(status='Closed').count(),
    }

    return render(request, 'ticket_view.html', {
        'tickets': tickets,
        'ticket_counts': ticket_counts,
        'assigned_values': assigned_values,
        'filters': {
            'assigned': assigned_filter,
            'status': status_filter,
            'mobile': mobile_filter,
        },
    })

def export_tickets_to_excel(request):
    # Create an Excel workbook and sheet
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet.title = "Tickets"

    # Define the table headers
    headers = ["SL NO", "Name", "Company", "Phone Number", "Email", "Assigned", "Status"]
    sheet.append(headers)

    # Fetch tickets with filters (reuse the filtering logic from ticket_view)
    tickets = Ticket.objects.all()
    if request.GET.get("assigned"):
        tickets = tickets.filter(assign_ticket=request.GET.get("assigned"))
    if request.GET.get("status"):
        tickets = tickets.filter(status=request.GET.get("status"))
    if request.GET.get("mobile"):
        tickets = tickets.filter(contact__icontains=request.GET.get("mobile"))

    # Add data to the Excel sheet
    for index, ticket in enumerate(tickets, start=1):
        sheet.append([
            index,
            ticket.name,
            ticket.company or "N/A",
            ticket.contact,
            ticket.email,
            ticket.assign_ticket,
            ticket.status,
        ])

    # Set response to download the file
    response = HttpResponse(content_type="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet")
    response["Content-Disposition"] = 'attachment; filename="tickets.xlsx"'
    workbook.save(response)
    return response

def customer_summary(request):
    return render(request, 'customer_summary.html')

def logout_view(request):
    return redirect('login')


def ticket_with_contact(request):
    if request.method == "POST":
        # Extract data from the request.POST and request.FILES
        name = request.POST.get("name")
        email = request.POST.get("email")
        contact = request.POST.get("contact")
        subject = request.POST.get("subject")
        assign_ticket = request.POST.get("assign_ticket", "Current User")
        priority = request.POST.get("priority", "Medium")
        service = request.POST.get("service", "General")
        department = request.POST.get("department", "General")
        predefined_reply = request.POST.get("predefined_reply")
        additional_notes = request.POST.get("additional_notes")
        knowledge_base_link = request.POST.get("knowledge_base")
        attachments = request.FILES.get("file")

        # Save the data to the database
        ticket = Ticket.objects.create(
            name=name,
            email=email,
            contact=contact,
            subject=subject,
            assign_ticket=assign_ticket,
            priority=priority,
            service=service,
            department=department,
            predefined_reply=predefined_reply,
            additional_notes=additional_notes,
            knowledge_base_link=knowledge_base_link,
            attachments=attachments,
        )
        ticket.save()

       # Send email with predefined reply
        try:
            send_mail(
                subject=f"Ticket: {subject}",  # Ticket subject
                message=predefined_reply,  # Body of the email (predefined reply)
                from_email='crmdbe@gmail.com',  # Replace with your email
                recipient_list=[email],  # Recipient email (from the form data)
                fail_silently=False,  # Don't fail silently if there's an error
            )
            messages.success(request, "Ticket created successfully and email sent!") 
           
            # Alert box
            return render(request, "ticket_with_contact.html", {"alert": "Ticket created successfully and email sent!"})
        except Exception as e:
            messages.error(request, f"Error sending email: {e}")  # Error handling

        # Redirect to another page or reload the form after saving
        return redirect("ticket_view")


    return render(request, "ticket_with_contact.html")

def ticket_without_contact(request):
    if request.method == "POST":
        # Extract data from the request.POST and request.FILES
        name = request.POST.get("name")
        email = request.POST.get("email")
        subject = request.POST.get("subject")
        assign_ticket = request.POST.get("assign_ticket", "Current User")
        priority = request.POST.get("priority", "Medium")
        service = request.POST.get("service", "General")
        department = request.POST.get("department", "General")
        predefined_reply = request.POST.get("predefined_reply")
        additional_notes = request.POST.get("additional_notes")
        knowledge_base_link = request.POST.get("knowledge_base")
        attachments = request.FILES.get("file")

        # Save the data to the database
        ticket = Ticket.objects.create(
            name=name,
            email=email,
            subject=subject,
            assign_ticket=assign_ticket,
            priority=priority,
            service=service,
            department=department,
            predefined_reply=predefined_reply,
            additional_notes=additional_notes,
            knowledge_base_link=knowledge_base_link,
            attachments=attachments,
        )
        ticket.save()

        # Send email with predefined reply
        try:
            send_mail(
                subject=f"Ticket: {subject}",  # Ticket subject
                message=predefined_reply,  # Body of the email (predefined reply)
                from_email='crmdbe@gmail.com',  # Replace with your email
                recipient_list=[email],  # Recipient email (from the form data)
                fail_silently=False,  # Don't fail silently if there's an error
            )
            messages.success(request, "Ticket created successfully and email sent!") 
           
            # Alert box
            return render(request, "ticket_without_contact.html", {"alert": "Ticket created successfully and email sent!"})
        except Exception as e:
            messages.error(request, f"Error sending email: {e}")  # Error handling

        # Redirect to another page or reload the form after saving
        return redirect("ticket_view")



    return render(request, "ticket_without_contact.html")

def edit_ticket(request, id):
    ticket = get_object_or_404(Ticket, id=id)
    
    if request.method == 'POST':
        # Update ticket details if the form is submitted
        ticket.name = request.POST.get('name')
        ticket.email = request.POST.get('email')
        ticket.contact = request.POST.get('contact')
        ticket.assign_ticket = request.POST.get('assign_ticket')
        ticket.subject = request.POST.get('subject')
        ticket.priority = request.POST.get('priority')
        ticket.status = request.POST.get('status')
        ticket.service = request.POST.get('service')
        ticket.department = request.POST.get('department')
        ticket.predefined_reply = request.POST.get('predefined_reply')
        ticket.additional_notes = request.POST.get('additional_notes')
        ticket.knowledge_base_link= request.POST.get('knowledge_base')
        
        # Handle file upload
        if request.FILES.get('file'):
            ticket.file = request.FILES.get('file')
        
        ticket.save()

        # Send email with predefined reply
        try:
            send_mail(
                subject=f"Ticket: {ticket.subject}",  # Ticket subject
                message=ticket.predefined_reply,  # Body of the email (predefined reply)
                from_email='crmdbe@gmail.com',  # Replace with your email
                recipient_list=[ticket.email],  # Recipient email (from the form data)
                fail_silently=False,  # Don't fail silently if there's an error
            )
            messages.success(request, "Ticket created successfully and email sent!") 
           
            # Alert box
            return render(request, "ticket_view.html", {"alert": "Ticket created successfully and email sent!"})
        except Exception as e:
            messages.error(request, f"Error sending email: {e}")  # Error handling

        # Redirect to another page or reload the form after saving
        return redirect("ticket_view")



    return render(request, 'edit_ticket.html', {'ticket': ticket})


def delete(request, id):
    try:
        # Get the ticket object by ID or return a 404
        ticket = get_object_or_404(Ticket, id=id)

        if request.method == 'POST':
            ticket.delete()
            messages.success(request, 'Ticket deleted successfully!')
            return HttpResponseRedirect(reverse('ticket_view'))
        
        # If not POST, return forbidden response
        return HttpResponseForbidden("Delete action only allowed via POST")
    
    except Exception as e:
        messages.error(request, f'Error deleting ticket: {str(e)}')
        return HttpResponseRedirect(reverse('ticket_view'))

# View to handle new product creation
def new_product1(request):
    if request.method == 'POST':
        try:
            product_name = request.POST.get("product_name")
            price = request.POST.get("price")
            types = request.POST.get("type")
            packages = request.POST.get("packages")
            
            if not product_name or not price or not types or not packages:
                messages.error(request, 'All fields are required!')
                return redirect('new_product')
            
            new_product = Product(
                product_name=product_name,
                price=price,
                type=types,
                packages=packages,
            )
            new_product.save()
            messages.success(request, 'Product added successfully!')
            return redirect('new_product')

        except Exception as e:
            print(f"Error: {e}")
            messages.error(request, 'An error occurred while adding the product!')
            return render(request, 'product.html')
    products = Product.objects.all()
    return render(request, 'product.html', {"products": products})

# View to display the list of products
def display(request):
    products = Product.objects.all()
    return render(request, "product.html", {"products": products})

def edit_product(request, product_id):
    product = get_object_or_404(Product, id=product_id)
    if request.method == 'POST':
        Product_name = request.POST.get('product_name')
        Type = request.POST.get('type')
        Price = request.POST.get('price')
        Packages = request.POST.get('packages')
        
        product.product_name = Product_name
        product.type = Type
        product.price = Price
        product.packages = Packages
        
        product.save()
        return redirect('new_product')
    return render(request, 'edit_product.html', {'product': product})

def delete_product(request,product_id): 
    try:
        product = get_object_or_404(Product, id=product_id)
        if request.method == 'POST':
            product.delete()
            messages.success(request, 'Product deleted successfully!')
            return HttpResponseRedirect(reverse('new_product'))
        
        return HttpResponseForbidden("Delete action only allowed via POST")
    
    except Exception as e:
        messages.error(request, f'Error deleting product: {str(e)}')
        return HttpResponseRedirect(reverse('new_product'))
class ProductDeleteView(DeleteView):
    model = Product
    template_name = 'product_confirm_delete.html'
    success_url = reverse_lazy('new_product')    

# doctor section

def submit_registration(request):
    context = {
        'state_choices': doctor.STATE_CHOICES
    }
    if request.method == 'POST':
        print(request.POST)
        title = request.POST.get('title')
        Name = request.POST.get('Name')
        Phone = request.POST.get('Phone')
        clinic_name = request.POST.get('Clinic_name')
        email = request.POST.get('Email')
        specialization = request.POST.get('specialization')
        state = request.POST.get('state')
        city = request.POST.get('City')
        call_status = request.POST.get('call_status')
        Age = request.POST.get('Age')

        try:
            new_doctor = doctor(
                title=title,
                Name=Name,
                Phone=Phone,
                Email=email,
                Clinic_name=clinic_name,
                specialization=specialization,
                state=state,
                City=city,
                call_status=call_status,
                Age=Age
            )
            new_doctor.save()
            return redirect('search')
        except Exception as e:
            messages.error(request, f'Error saving doctor: {e}')

    return render(request, 'doctorreg.html', context)

# Search
def search(request):
    query = request.GET.get('q', '')
    specialization = request.GET.get('specialization', '')
    status = request.GET.get('status', '')
    state = request.GET.get('state', '')
    city = request.GET.get('city', '')

    doctors = doctor.objects.all()

    if query:
        doctors = doctors.filter(Name__icontains=query)

    if specialization:
        doctors = doctors.filter(specialization__icontains=specialization)

    if status:
        doctors = doctors.filter(call_status__icontains=status)

    if state:
        doctors = doctors.filter(state__icontains=state)

    if city:
        doctors = doctors.filter(City__icontains=city)

    specializations = doctor.objects.values_list('specialization', flat=True).distinct()
    states = doctor.objects.values_list('state', flat=True).distinct()
    cities = doctor.objects.values_list('City', flat=True).distinct()

    context = {
        'doctors': doctors,
        'specializations': specializations,
        'states': states,
        'cities': cities
    }

    return render(request, 'search.html', context)

def edit_doctor(request, pk):
    Doctor = get_object_or_404(doctor, Did=pk)
    
    if request.method == 'POST':
        print("Form submitted!")
        form = DoctorForm(request.POST, instance=Doctor)
        if form.is_valid():
            print("Form is valid!") 
            form.save()
            return redirect('search')
        else:
            print("Form errors:", form.errors)
    else:
        form = DoctorForm(instance=doctor)
    
    return render(request, 'editpage.html', {'doctor': Doctor, 'form': form})

class DoctorDeleteView(DeleteView):
    model = doctor
    template_name = 'doctor_confirm_delete.html'
    success_url = reverse_lazy('search')

# followup section

def follow(request, pk):
    obj = get_object_or_404(doctor, Did=pk)
    return render(request, "follow.html", {"doctor": obj})

def follow_up(request, pk):
    print("follow_up")
    obj = get_object_or_404(doctor, Did=pk)
    if request.method == 'POST':
        next_follow_up = request.POST.get('next_follow_up')
        description = request.POST.get('description')

        if next_follow_up:
            interaction.objects.create(doc_id=obj, next_follow_up=next_follow_up, description=description)
            messages.success(request, "Follow-Up saved successfully!")
            return redirect("follow",pk=obj.Did)

    return render(request, 'follow_up.html', {"doctor": obj})

def interested(request, pk):
    obj = get_object_or_404(doctor, Did=pk)
    
    if request.method == 'POST':
        type = request.POST.get('type')
        priority = request.POST.get('priority')
        product_type = request.POST.get('product_type')
        demo_date = request.POST.get('demo_date')
        notes = request.POST.get('notes')

        interested_to = interaction.objects.filter(doc_id=obj).first()

        if interested_to:
            interested_to.type = type
            interested_to.priority = priority
            interested_to.product_type = product_type
            interested_to.demo_date = demo_date
            interested_to.notes = notes
            interested_to.save()
            messages.success(request, "Interaction updated successfully!")
        else:
            interested_to = interaction(
                doc_id=obj,
                type=type,
                priority=priority,
                product_type=product_type,
                demo_date=demo_date,
                notes=notes
            )
            interested_to.save()
            messages.success(request, "Interaction created successfully!")
        return redirect("follow",pk=obj.Did)
    
    return render(request, 'interested.html', {"doctor": obj})

def not_interested(request, pk):
    obj = get_object_or_404(doctor, Did=pk)
    
    if request.method == 'POST':
        next_follow_up = request.POST.get('next_follow_up')
        reason = request.POST.get('reason')

        existing_interaction = interaction.objects.filter(doc_id=obj).first()
        if existing_interaction:
            existing_interaction.reason = reason
            existing_interaction.save()
            messages.success(request, "Not interested updated successfully!")
        else:
            interaction.objects.create(doc_id=obj, next_follow_up=next_follow_up, reason=reason)
            messages.success(request, "Not interested saved successfully!")

        return redirect("follow",pk=obj.Did)
    return render(request, "not_interested.html", {"doctor": obj})

def closed_view(request, pk):
    obj = get_object_or_404(doctor, Did=pk)
    
    if request.method == 'POST':
        product_type = request.POST.get('product_type')
        product = request.POST.get('product')
        quantity = request.POST.get('quantity')
        price = request.POST.get('price')
        discount = request.POST.get('discount')
        offer = request.POST.get('offer')
        installation_type = request.POST.get('installation_type')
        installation_date = request.POST.get('installation_date')
        duration_from = request.POST.get('duration_from')
        duration_to = request.POST.get('duration_to')
        payment_type = request.POST.get('payment_type')
        payment = request.POST.get('payment')
        description = request.POST.get('description')

        existing_interaction = interaction.objects.filter(doc_id=obj).first()
        if existing_interaction:
            existing_interaction.quantity = quantity
            existing_interaction.price = price
            existing_interaction.discount = discount
            existing_interaction.offer = offer
            existing_interaction.installation_type = installation_type
            existing_interaction.installation_date = installation_date
            existing_interaction.duration_from = duration_from
            existing_interaction.duration_to = duration_to
            existing_interaction.payment_type = payment_type
            existing_interaction.payment = payment
            existing_interaction.description = description
            existing_interaction.save()
            messages.success(request, "Interaction updated successfully!")
        else:
            interaction.objects.create(
                doc_id=obj,
                product_type=product_type,
                product=product,
                quantity=quantity,
                price=price,
                discount=discount,
                offer=offer,
                installation_type=installation_type,
                installation_date=installation_date,
                duration_from=duration_from,
                duration_to=duration_to,
                payment_type=payment_type,
                payment=payment,
                description=description
            )
            messages.success(request, "Added successfully!")

        return redirect("follow",pk=obj.Did)

    return render(request, "closed.html", {"doctor": obj})

def not_response(request, pk):
    obj = get_object_or_404(doctor, Did=pk)
    
    if request.method == 'POST':
        next_calling = request.POST.get('next_calling')

        existing_interaction = interaction.objects.filter(doc_id=obj).first()
        if existing_interaction:
            messages.info(request, "This next calling entry already exists.")
        else:
            interaction.objects.create(doc_id=obj, next_calling=next_calling)
            messages.success(request, "Data added successfully!")

        return redirect("follow",pk=obj.Did)

    return render(request, "not_response.html", {"doctor": obj})

def call_later(request, pk):
    obj = get_object_or_404(doctor, Did=pk)
    
    if request.method == 'POST':
        call_later = request.POST.get('call_later')
        reason = request.POST.get('reason')

        existing_interaction = interaction.objects.filter(doc_id=obj).first()
        if existing_interaction:
            existing_interaction.reason = reason
            existing_interaction.save()
            messages.success(request, "Data updated successfully!")
        else:
            interaction.objects.create(doc_id=obj, call_later=call_later, reason=reason)
            messages.success(request, "Data added successfully!")
        return redirect("follow",pk=obj.Did)
    return render(request, "call_later.html", {"doctor": obj})


from datetime import datetime
def follow_filter(request):
    # Get filter values from the request
    query = request.GET.get('q', '')
    staff_name = request.GET.get('assigned', '').strip()  
    mobile_number = request.GET.get('Phone', '').strip()  
    from_date_str = request.GET.get('from_date', '').strip()
    to_date_str = request.GET.get('to_date', '').strip()

    from_date = datetime.strptime(from_date_str, '%Y-%m-%d').date() if from_date_str else None
    to_date = datetime.strptime(to_date_str, '%Y-%m-%d').date() if from_date_str else None

    follow_list = lead.objects.select_related('doctors').all()


    if query:
        follow_list=follow_list.filter(doctors__Name__icontains=query)
    if staff_name:
        follow_list = follow_list.filter(assigned__icontains=staff_name)

    if mobile_number:
        follow_list = follow_list.filter(doctors__Phone__icontains=mobile_number)

    if from_date:
        follow_list = follow_list.filter(date__gte=from_date)

    if to_date:
        follow_list = follow_list.filter(date__lte=to_date)

    paginator = Paginator(follow_list, 8)
    page_number = request.GET.get('page', 1)
    page_obj = paginator.get_page(page_number)

    # Fetch doctors and staff for dropdowns
    data = []
    for follow in page_obj:
        doctor_obj = follow.doctors
        interactions = interaction.objects.filter(doc_id=doctor_obj).order_by('next_follow_up')
        if interactions.exists():
            interact = interactions.first()
            next_follow_up = interact.next_follow_up
            reminder = getattr(interact, 'reminder', 'No Reminder Available')
        else:
            next_follow_up = 'No Date Available'
            reminder = 'No Reminder Available'
        data.append({
            'follow': follow,
            'doctor': doctor_obj,
            'next_follow_up': next_follow_up,
            'reminder': reminder,
            'interactions': interactions,
        })

    # Dropdown data (if needed for the template)
    doctors = doctor.objects.all()
    staff_members = lead.objects.all()  # Assuming staff info is in lead objects
    mobile_numbers = doctor.objects.values_list('Phone', flat=True).distinct()

    context = {
        'data': data,
        'page_obj': page_obj,
        'doctors': doctors,
        'staff_members': staff_members,
        'mobile_numbers': mobile_numbers,
        'query': query,
        'staff_name': staff_name,
        'mobile_number': mobile_number,
        'from_date': from_date_str,
        'to_date': to_date_str,
    }
    return render(request, 'followup_filter.html', context)


