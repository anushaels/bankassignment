from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth import get_user_model
from django.utils import timezone

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)
    name = models.CharField(max_length=100)

    # Adding related_name to avoid clashes
    groups = models.ManyToManyField(
        'auth.Group',
        related_name='custom_user_set',
        blank=True,
        help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.',
        verbose_name='groups'
    )
    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='custom_user_set',
        blank=True,
        help_text='Specific permissions for this user.',
        verbose_name='user permissions'
    )

    def _str_(self):
        return self.username


class BankAccount(models.Model):
    ACCOUNT_TYPES = [
        ('savings', 'Savings'),
        ('current', 'Current'),
    ]

    user = models.OneToOneField(get_user_model(), on_delete=models.CASCADE)  # Ensure one account per user
    account_number = models.CharField(max_length=12, unique=True)
    account_type = models.CharField(max_length=10, choices=ACCOUNT_TYPES, default='savings')
    balance = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    date_created = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.user.username} - {self.account_number}"


class Transaction(models.Model):
    TRANSACTION_TYPES = [
        ('deposit', 'Deposit'),
        ('withdrawal', 'Withdrawal'),
    ]

    account = models.ForeignKey(BankAccount, on_delete=models.CASCADE)
    transaction_id = models.CharField(max_length=100, unique=True)
    transaction_type = models.CharField(max_length=10, choices=TRANSACTION_TYPES)
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateTimeField(default=timezone.now)

    def __str__(self):
        return f"{self.transaction_id} - {self.transaction_type} - {self.amount}"
