from django.contrib.auth import get_user_model, login as auth_login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.urls import reverse
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_decode
from django.contrib import messages
from .forms import  ProfileForm
from .models import Activation
from django.http import HttpResponse
from django.utils.http import urlsafe_base64_encode
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from .models import *
from django import forms
from .forms import *
from django.db import IntegrityError 



def myLogin(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            # Check if the user exists
            username = form.cleaned_data.get('username')
            if not User.objects.filter(username=username).exists():
                return render(request, 'registration/login.html', {'form': form, 'error_message': 'This account has been deleted.'})

            # If the user exists, proceed with login
            user = form.get_user()
            auth_login(request, user)
            return redirect('myProfile')
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})

@login_required()
def myProfile(request):
    return render(request,'projectdir/user_profile.html')


def register(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password1 = request.POST.get('password1')
        password2 = request.POST.get('password2')
        mobile = request.POST.get('mobile')
        first_name = request.POST.get('first_name')
        last_name = request.POST.get('last_name')

        if username and email and password1 and password2 and mobile and first_name and last_name:
            if password1 == password2:
                if not mobile.startswith('+20'):
                    return render(request, 'registration/register.html', {'error_message': 'Mobile number should start with +20'})

                try:
                    user = User.objects.create_user(username=username, email=email, password=password1, first_name=first_name, last_name=last_name)
                    activation = Activation.objects.create(user=user)
                    subject = 'Activate your account'
                    message = render_to_string('registration/activation_email.html', {
                        'user': user,
                        'domain': request.get_host(),
                        'uid': urlsafe_base64_encode(force_bytes(user.pk)),
                        'token': str(activation.token),
                    })
                    user.email_user(subject, message)
                    return render(request, 'registration/check.html')
                except IntegrityError:
                    return render(request, 'registration/register.html', {'error_message': 'This username already exists.'})
            else:
                return render(request, 'registration/register.html', {'error_message': 'Passwords do not match.'})
        else:
            return HttpResponse('Please provide all required information for registration.')
    else:
        return render(request, 'registration/register.html')
    
    
def activate(request, uidb64, token):
    try:
        uid = urlsafe_base64_decode(uidb64).decode()
        user = User.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, User.DoesNotExist, UnicodeDecodeError):
        user = None
    
    activation = Activation.objects.filter(user=user, token=token).first()
    if user is not None and activation is not None and not activation.is_expired():
        user.is_active = True
        user.save()
        activation.delete()
        return render(request, 'registration/activation_success.html')
    else:
        return render(request, 'registration/activation_failure.html')
    
def delete_confirmation(request, user_id):
    user = User.objects.get(id=user_id)
    return render(request, 'registration/delete_confirmation.html', {'user': user})

def DeleteAccount(request, user_id):
    if request.method == 'POST':
        user = User.objects.get(id=user_id)
        user.delete()
        return redirect('login')  
    else:
        return redirect('myProfile')
    
@login_required
def updateUser(request, user_id):
    userr = User.objects.get(id=user_id)
    profile = Profile.objects.get(user=userr)
    context = {'userr': userr}
    
    if request.method == 'POST':
        # Creating a form instance with the submitted data
        user_form = UserUpdateForm(request.POST, instance=userr)
        profile_form = ProfileUpdateForm(request.POST, request.FILES, instance=profile)
        
        if user_form.is_valid() and profile_form.is_valid():
            user_form.save()
            profile_form.save()
            return HttpResponseRedirect(reverse('user_project'))
    else:
        # Pre-populate the forms with current data
        user_form = UserUpdateForm(instance=userr)
        profile_form = ProfileUpdateForm(instance=profile)
    
    context['user_form'] = user_form
    context['profile_form'] = profile_form
    return render(request, 'registration/update.html', context)



from django.shortcuts import render, redirect
from .forms import AdditionalForm

def additional_info(request):
    try:
        additional_info = request.user.additionalinfo
    except AdditionalInfo.DoesNotExist:
        additional_info = None
    
    if request.method == 'POST':
        form = AdditionalForm(request.POST, instance=additional_info)
        if form.is_valid():
            additional_info = form.save(commit=False)
            additional_info.user = request.user
            additional_info.save()
            messages.success(request, 'Additional information saved successfully.')
            return redirect('user_project')
    else:
        form = AdditionalForm(instance=additional_info)
    
    return render(request, 'registration/additional_info.html', {'form': form})

@login_required
def userImage(request):
    if request.method == 'POST':
        form = ProfileForm(request.POST, request.FILES)
        if form.is_valid():
            profile = form.save(commit=False)
            profile.user = request.user
            profile.save()
            return redirect('projects.list')  # Assuming you have a URL named 'profile_detail' for profile detail view
    else:
        form = ProfileForm()
    return render(request, 'registration/userImage.html', {'form': form})












    



