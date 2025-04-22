from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils.timezone import now
from datetime import timedelta

class BDE(models.Model):
    bid=models.AutoField(primary_key=True)
    username=models.CharField(max_length=20,unique=True)
    email=models.EmailField(max_length=300,unique=True)
    password=models.CharField(max_length=200,unique=True)


# 
class doctor(models.Model):
    STATE_CHOICES = [
        ('AP', 'Andhra Pradesh'),
        ('AR', 'Arunachal Pradesh'),
        ('AS', 'Assam'),
        ('BR', 'Bihar'),
        ('CT', 'Chhattisgarh'),
        ('GA', 'Goa'),
        ('GJ', 'Gujarat'),
        ('HR', 'Haryana'),
        ('HP', 'Himachal Pradesh'),
        ('JH', 'Jharkhand'),
        ('KA', 'Karnataka'),
        ('KL', 'Kerala'),
        ('MP', 'Madhya Pradesh'),
        ('MH', 'Maharashtra'),
        ('MN', 'Manipur'),
        ('ML', 'Meghalaya'),
        ('MZ', 'Mizoram'),
        ('NL', 'Nagaland'),
        ('OR', 'Odisha'),
        ('PB', 'Punjab'),
        ('RJ', 'Rajasthan'),
        ('SK', 'Sikkim'),
        ('TN', 'Tamil Nadu'),
        ('TG', 'Telangana'),
        ('TR', 'Tripura'),
        ('UP', 'Uttar Pradesh'),
        ('UT', 'Uttarakhand'),
        ('WB', 'West Bengal'),
        ('AN', 'Andaman and Nicobar Islands'),
        ('CH', 'Chandigarh'),
        ('DN', 'Dadra and Nagar Haveli and Daman and Diu'),
        ('DL', 'Delhi'),
        ('JK', 'Jammu and Kashmir'),
        ('LA', 'Ladakh'),
        ('LD', 'Lakshadweep'),
        ('PY', 'Puducherry'),
    ]
    
    Did = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100)
    Name = models.CharField(max_length=100)
    Phone = models.CharField(max_length=100)
    Email = models.EmailField()
    Clinic_name = models.CharField(max_length=100)
    specialization = models.CharField(max_length=100)
    state = models.CharField(max_length=20, choices=STATE_CHOICES)
    City = models.CharField(max_length=100)
    call_status = models.CharField(max_length=100)
    Age = models.PositiveIntegerField()

class Product(models.Model):
    product_name = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    type = models.CharField(max_length=50)
    packages = models.TextField()

    def __str__(self):
        return self.product_name

class interaction(models.Model):
    doc_id = models.ForeignKey('doctor', on_delete=models.CASCADE, related_name='interaction', blank=True,null=True)
    next_follow_up = models.DateField(null=True, blank=True)
    description = models.CharField(max_length=250)
    type = models.CharField(max_length=250)
    priority = models.CharField(max_length=250)
    product_type = models.CharField(max_length=250)
    demo_date = models.DateField(null=True, blank=True)
    notes = models.TextField(null=True, blank=True)
    next_follow_up = models.DateField(null=True, blank=True)
    reason = models.CharField(max_length=250)    
    product_type = models.CharField(max_length=200, null=True)
    product = models.CharField(max_length=100)
    quantity = models.IntegerField(null=True, blank=True)
    price = models.IntegerField(null=True, blank=True)
    discount = models.IntegerField(null=True, blank=True)
    offer = models.CharField(max_length=100, null=True, blank=True)
    installation_type = models.CharField(max_length=200)
    installation_date = models.DateField(null=True, blank=True)
    duration_from = models.DateField(null=True, blank=True)
    duration_to = models.DateField(null=True, blank=True)
    payment_type = models.CharField(max_length=100, null=True, blank=True)
    payment = models.IntegerField(null=True, blank=True)
    description = models.CharField(max_length=250)
    next_calling = models.DateField(null=True, blank=True)
    call_later = models.DateField(null=True, blank=True)
    reason = models.CharField(max_length=400)  

class lead(models.Model):
    state = models.CharField(max_length=60)
    specialization = models.CharField(max_length=50)
    assigned = models.CharField(max_length=50, default='assigned')
    mode = models.CharField(max_length=40)
    name = models.CharField(max_length=50)
    address = models.CharField(max_length=100)
    position = models.CharField(max_length=50)
    city = models.CharField(max_length=50)
    email = models.EmailField()
    website = models.CharField(max_length=100)
    country = models.CharField(max_length=100)
    phone = models.CharField(max_length=30)
    zipcode = models.IntegerField()
    clinic_name = models.CharField(max_length=100)
    default_language = models.CharField(max_length=100)
    priority = models.CharField(max_length=100)
    notes = models.CharField(max_length=200)
    status = models.CharField(max_length=200)
    doctors = models.ForeignKey('doctor', on_delete=models.CASCADE, related_name='leads', blank=True,null=True)

class UserManager(BaseUserManager):
    def create_user(self, email, password=None):
        if not email:
            raise ValueError("Users must have an email address")
        user = self.model(email=self.normalize_email(email))
        user.set_password(password)  # Hashes the password
        user.save(using=self._db)
        return user

    def create_superuser(self, email, password=None):
        user = self.create_user(email, password)
        user.is_admin = True
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user


class User(AbstractBaseUser, PermissionsMixin):
    email = models.EmailField(max_length=100, unique=True)
    is_active = models.BooleanField(default=True)
    is_admin = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)

    objects = UserManager()
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []  

class Ticket(models.Model):
    # Basic Details
    name = models.CharField(max_length=100)
    email = models.EmailField()
    contact = models.CharField(max_length=15, blank=True, null=True)  # For phone numbers
    
    # Ticket Details
    company = models.CharField(max_length=100, default="Unknown")
    subject = models.CharField(max_length=255)
    assign_ticket = models.CharField(max_length=100, default="Current User")  # Assuming default
    
    # Priority, Service, and Department
    PRIORITY_CHOICES = [
        ('Low', 'Low'),
        ('Medium', 'Medium'),
        ('High', 'High'),
    ]
    priority = models.CharField(max_length=10, choices=PRIORITY_CHOICES, default='Medium')
    STATUS_CHOICES = [
        ('Open', 'Open'),
        ('In Progress', 'In Progress'),
        ('On Hold', 'On Hold'),
        ('Answered', 'Answered'),
        ('Closed', 'Closed'),
    ]
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='Open')
    service = models.CharField(max_length=100,default="General")
    department = models.CharField(max_length=100, default="General")    

    # Tickets Body
    predefined_reply = models.TextField(blank=True, null=True)
    additional_notes = models.TextField(blank=True, null=True)

    # Knowledge Base Link
    knowledge_base_link = models.URLField(blank=True, null=True)

    # File Upload
    attachments = models.FileField(upload_to='attachments/', blank=True, null=True)

    # # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)  # Auto-set on ticket creation
    updated_at = models.DateTimeField(auto_now=True)  # Auto-update on ticket modification

    def __str__(self):
        return f"{self.name} - {self.subject}"

    class Meta:
        ordering = ['-id']




