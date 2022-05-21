from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail

# Create your views here.
def send_login_email(request):
    email = request.POST['email']
    send_mail('Your login link for Superlists', 'body', 'noreply@superlists', [email])

    messages.success(
        request, 
        "Check your email, we've sent you a link you can use to log in."
    )
    return redirect('/')

