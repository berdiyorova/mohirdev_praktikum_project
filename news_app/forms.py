from django import forms
from .models import Contact

class ConatactForm(forms.ModelForm):

    class Meta():
        model = Contact
        fields = "__all__"  # yoki ['name', 'email', 'message'] deb bersak ham buladi