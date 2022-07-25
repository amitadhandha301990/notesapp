from dataclasses import fields
from pyexpat import model
from django import forms
from .models import usersignup,notesdata,contactdata

class usersignupform(forms.ModelForm):
    class Meta:
        model=usersignup
        fields='__all__'

class notesdataform(forms.ModelForm):
    class Meta:
        model=notesdata
        fields='__all__'

class contactdataform(forms.ModelForm):
    class Meta:
        model=contactdata
        fields='__all__'
