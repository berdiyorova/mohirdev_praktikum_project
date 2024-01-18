from django import forms
from .models import Contact,Comment

class ConatactForm(forms.ModelForm):

    class Meta():
        model = Contact
        fields = "__all__"  # yoki ['name', 'email', 'message'] deb bersak ham buladi


class SubscriptionForm(forms.Form):
    subject = forms.CharField(max_length=100)
    message = forms.CharField()
    email = forms.EmailField()


class CommentForm(forms.ModelForm):
     class Meta:
         model = Comment
         fields = ['body']