from django import forms

class ContactForm(forms.Form):
    uname = forms.CharField(max_length=100, required=True)
    uemail = forms.EmailField(required=True)
    phone_number = forms.CharField(max_length=15, required=True)
    message = forms.CharField(widget=forms.Textarea, required=True)

# class UserForm(forms.Form):
#     uname = forms.CharField(max_length=100)
#     uemail = forms.EmailField()
#     reward = forms.IntegerField(default=0)