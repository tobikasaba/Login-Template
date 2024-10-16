from django import forms
from django.contrib.auth.models import User
from .models import UserProfileInfo


class UserForm(forms.ModelForm):
    # django has an inbuilt password defined filed
    # this field replaces the default password field in the Django User model when this form is used.
    password = forms.CharField(widget=forms.PasswordInput())

    class Meta:
        model = User
        fields = ('username', 'email', 'password')


class UserProfileInfoForm(forms.ModelForm):
    """
    The UserProfileInfoForm form is created because these fields are not included in the inbuilt User Model
    this is because the inbuilt User model can't be modified.
    The fields in User are available in UserProfileInfo but a User form is particularly created because its best practice to manage the fields specific to the User model in a form dedicated to it.
    """

    class Meta:
        model = UserProfileInfo
        fields = ('portfolio_site', 'profile_pic')
