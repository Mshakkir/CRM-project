from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static


urlpatterns = [
        #    path('',views.home),
           path('', views.login_view, name='login'),
           path('ticket_view/', views.ticket_view, name='ticket_view'),
           path('about/', views.about, name='about'), 
           path('logout/', views.logout_view, name='logout'),
           path('export_tickets/', views.export_tickets_to_excel, name='export_tickets'),
           path('ticket_view/ticket_with_contact', views.ticket_with_contact, name='ticket_with_contact'),  
           path('ticket_view/ticket_without_contact', views.ticket_without_contact, name='ticket_without_contact'),  
           path('customer_summary/', views.customer_summary, name='customer_summary'),  
           path('edit_ticket/<int:id>/', views.edit_ticket, name='edit_ticket'), 
           path('delete/<int:id>/', views.delete, name='delete'),
         
           path('dashboard/', views.dashboard_view, name='dashboard'),  
           path('forgot_password/', views.forgot_pass, name='forgot_password'),
           path('otp-verification/',views.otp_verification, name='otp_verification'),
           path('resetpassword/',views.reset_password, name='resetpassword'),
           path('newleads/',views.new_leads, name='newleads'),
           path('leadsview/',views.leads_view,name='leads'),
           path('leadsview/edit/<int:lead_id>/', views.edit_lead, name='edit_lead'),
           path('deletelead/<int:id>/', views.delete_lead, name='deletelead'),
           path('new_product/', views.new_product1,name='new_product'), 
           path('new_product/edit/<int:product_id>/', views.edit_product, name='edit_product'),
           path('new_product/delete/<int:pk>/', views.ProductDeleteView.as_view(), name='delete_product'),
            
            path('doctor/', views.submit_registration, name='doctor'),
            path("search",views.search, name="search") ,
            path("follow/doctor/<int:pk>/",views.follow, name="follow") ,
            path('doctor/edit/<int:pk>/', views.edit_doctor, name='doctor_edit'),
            path('doctor/delete/<int:pk>/', views.DoctorDeleteView.as_view(), name='doctor_delete'),
                    
            

            
            path('followup/doctor/<int:pk>/',views.follow_up,name="follow_up"),
            
            path('interested/doctor/<int:pk>/',views.interested,name="interested"),
            
            path('not_interested/doctor/<int:pk>/',views.not_interested,name="not_interested"),
            
            path('closed/doctor/<int:pk>/',views.closed_view,name="closed"),
            
            path('not_response/doctor/<int:pk>/',views.not_response,name="not_response"),
            
            path('call_later/doctor/<int:pk>/',views.call_later,name="call_later"),
            
            path('followup_filter/',views.follow_filter,name="followup_filter")
    
               ]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)