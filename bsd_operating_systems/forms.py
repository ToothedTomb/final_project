from django import forms
from .models import OperatingSystems, Comment

class OperatingSystemsForm(forms.ModelForm):
    class Meta:
        model = OperatingSystems
        fields = ['name', 'Package_Manager', 'CPU_Architecture', 'Latest_Version', 'End_Of_Support', 'logo', 'website']
        widgets = {
            'End_Of_Support': forms.DateInput(
                attrs={
                    'type': 'date',
                    'class': 'date-input'
                }
            ),
            'name': forms.TextInput(
                attrs={
                    'placeholder': 'e.g: FreeBSD'
                }
            ),
            'Package_Manager': forms.TextInput(
                attrs={
                    'placeholder': 'e.g: dnf'
                }
            ),
            'Latest_Version': forms.TextInput(
                attrs={
                    'placeholder': 'e.g: 23.0'
                }
            ),
            'CPU_Architecture': forms.TextInput(
                attrs={
                    'placeholder': 'e.g: x86-64, -386'
                }
            ),
            'website': forms.URLInput(
                attrs={
                    'placeholder': 'e.g: https://www.freebsd.org'
                }
            )
        }