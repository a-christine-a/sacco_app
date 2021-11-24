from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from appliction.models import UpdateProfile
# from .models import LoanApplication


# class ApplyLoan():
#     income_level = forms.FloatField(UserCreationForm)
#     amount_applied = forms.FloatField() 
#     repayment_period_in_months = forms.IntegerField(max_value=15)
#     guarantor_id = forms.IntegerField()
#     guarantor_name = forms.CharField(max_length=50)
#     guarantor_email = forms.EmailField()
#     gurantor_income_level = forms.FloatField()

#     class Meta:
#         model =  User
#         fields = (
#                 'income_level', 'amount_applied', 'repayment_period_in_months',
#                 'guarantor_id', 'guarantor_name', 'guarantor_email', 'gurantor_income_level'
#         )

class UserForm(UserCreationForm):
    first_name = forms.CharField(max_length=50, required=True)
    last_name = forms.CharField(max_length=50, required=True)
    email = forms.EmailField(max_length=200)
       
    class Meta():
        model = User
        fields = (
            'username', 'first_name', 'last_name', 'email'
        )

class UserProfileInfoForm(forms.ModelForm):
    id_number = forms.IntegerField()
    address = forms.CharField(max_length=50, required=False)
    phone_number = forms.IntegerField()
    date_of_birth = forms.CharField(max_length=50)

    class Meta():
        model = UpdateProfile
        fields = ('id_number','address', 'phone_number', 'date_of_birth')