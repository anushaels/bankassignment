from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser,BankAccount,Transaction

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'email', 'password1', 'password2']


class BankAccountForm(forms.ModelForm):
    initial_deposit = forms.DecimalField(max_digits=10, decimal_places=2, required=True, label='Initial Deposit')

    class Meta:
        model = BankAccount
        fields = ['account_number', 'account_type', 'initial_deposit']

class TransactionForm(forms.ModelForm):
    class Meta:
        model = Transaction
        fields = ['transaction_type', 'amount']
