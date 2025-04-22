# forms.py
from django import forms
from .models import doctor

class DoctorForm(forms.ModelForm):
    class Meta:
        model = doctor
        fields = ['Name','Clinic_name','Email','Phone','specialization',]  # Include all fields from the model