from django.shortcuts import render
from .forms import LoginModelForm
from django.contrib.auth.decorators import login_required
from django.views.decorators.cache import cache_control

from django.shortcuts import render

def greeting(request):
    return render(request, 'home.html')


from django.contrib.auth.forms import UserCreationForm
from django import forms


class CustomUserCreationForm(UserCreationForm):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Hiding help text for email and password fields
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        self.fields['username'].help_text =None

       
from django.contrib.auth.forms import UserCreationForm
from django.shortcuts import render,redirect

def signup_page(request):
    if request.method == 'POST':
        form = CustomUserCreationForm(request.POST)
        if form.is_valid():
            cust = form.save()           
            return redirect('login')    
            
    else:
        form = CustomUserCreationForm()
    return render(request, 'signup.html', {'form': form})

from django.contrib.auth.forms import AuthenticationForm
from django.shortcuts import render,redirect
from django.contrib.auth import login 

def login_page(request):
    if request.method == 'POST':
        form = AuthenticationForm(data=request.POST)
        if form.is_valid():
            # Authenticate the user
            user = form.get_user()
            login(request, user)
            # Redirect to home page after successful login
            return redirect('home')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})
    

from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

@login_required(login_url='/login/')
def logout_view(request):
    if request.method == 'POST':
        logout(request)
        return redirect('login')

    context = {
        'user': request.user
    }

    return render(request, 'logout.html', context)