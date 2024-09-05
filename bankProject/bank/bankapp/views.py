from django.utils import timezone

from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .forms import CustomUserCreationForm
from .models import BankAccount,Transaction
from .forms import BankAccountForm,TransactionForm


from django.core.paginator import Paginator

# Register View: Handles user registration
def register(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(f"User {user.username} saved successfully")  # Debug
            messages.success(request, "Registration successful. You can now log in.")
            return redirect('login')
        else:
            print(form.errors)  # Debug any form errors

    else:
        form = CustomUserCreationForm()
    return render(request, 'account/register.html', {'form': form})

# Login View: Handles user login
def login_user(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=username, password=password)
            if user is not None:
                login(request, user)
                return redirect('manage_account')  # Redirect to the account management page
            else:
                messages.error(request, 'Invalid username or password.')
        else:
            messages.error(request, 'Invalid username or password.')
    else:
        form = AuthenticationForm()
    return render(request, 'account/login.html', {'form': form})



# Logout View: Handles user logout
@login_required
def logout_user(request):
    logout(request)
    return redirect('login')



def home(request):
    return render(request, 'home.html')






# @login_required
# def manage_account(request):
#     try:
#         # Check if the user already has an account
#         account = BankAccount.objects.get(user=request.user)
#         return render(request, 'account/account_details.html', {'account': account})
#     except BankAccount.DoesNotExist:
#         # If no account exists, allow user to create one
#         if request.method == 'POST':
#             form = BankAccountForm(request.POST)
#             if form.is_valid():
#                 account = form.save(commit=False)
#                 account.user = request.user
#                 account.save()
#                 messages.success(request, 'Bank account created successfully!')
#                 return redirect('manage_account')  # Redirect to account details page
#         else:
#             form = BankAccountForm()
#         return render(request, 'account/create_account.html', {'form': form})
@login_required
def manage_account(request):
    try:
        # Check if the user already has an account
        account = BankAccount.objects.get(user=request.user)
    except BankAccount.DoesNotExist:
        account = None

    if request.method == 'POST':
        form = BankAccountForm(request.POST)
        if form.is_valid():
            account = form.save(commit=False)
            account.user = request.user
            # Set the initial deposit as the balance
            initial_deposit = form.cleaned_data.get('initial_deposit')
            account.balance = initial_deposit
            account.save()

            # Log the initial deposit as a transaction
            Transaction.objects.create(
                account=account,
                transaction_id=f'TXN{timezone.now().timestamp()}',
                transaction_type='deposit',
                amount=initial_deposit,
                date=timezone.now()
            )

            messages.success(request, 'Bank account created successfully with an initial deposit!')
            return redirect('manage_account')
    else:
        form = BankAccountForm()

    return render(request, 'account/manage_account.html', {'form': form, 'account': account})

@login_required
def transaction(request):
    account = BankAccount.objects.get(user=request.user)
    if request.method == 'POST':
        form = TransactionForm(request.POST)
        if form.is_valid():
            transaction = form.save(commit=False)
            transaction.account = account

            if transaction.transaction_type == 'withdrawal':
                if account.balance >= transaction.amount:
                    account.balance -= transaction.amount
                    messages.success(request, f'Withdrawal of {transaction.amount} successful.')
                else:
                    messages.error(request, 'Insufficient balance for this withdrawal.')
                    return redirect('transaction')

            elif transaction.transaction_type == 'deposit':
                account.balance += transaction.amount
                messages.success(request, f'Deposit of {transaction.amount} successful.')

            # Save the transaction and update balance
            transaction.transaction_id = f'TXN{timezone.now().timestamp()}'  # Example ID generation
            transaction.save()
            account.save()
            return redirect('transaction')

    else:
        form = TransactionForm()

    return render(request, 'account/transaction.html', {'form': form, 'account': account})


@login_required
def transaction_history(request):
    account = BankAccount.objects.get(user=request.user)
    transactions = Transaction.objects.filter(account=account).order_by('-date')

    # Pagination
    paginator = Paginator(transactions, 10)  # Show 10 transactions per page
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    return render(request, 'account/transaction_history.html', {'page_obj': page_obj, 'account': account})


