from django.shortcuts import render,redirect
from rental_app.forms import*
from django.views.generic import *
from django.views import View
from django.urls import reverse_lazy,reverse
from django.contrib.auth import authenticate,login,logout
from django.contrib import messages
from rental_app.models import *
from django.views.generic import ListView

# Create your views here.

class SignupView(CreateView):
    template_name="signup.html"
    form_class=SignupForm
    success_url=reverse_lazy("signin")

class SigninView(FormView):
    template_name="signin.html"
    form_class=SigninForm
    def post(self, request):
        form_data=SigninForm(data=request.POST)
        if form_data.is_valid():
            uname=form_data.cleaned_data.get('username')
            pswd=form_data.cleaned_data.get('password')
            user=authenticate(request,username=uname,password=pswd)
            if user:
                login(request,user)
                if user.is_superuser==False:
                    return redirect('homepage')
                elif user.is_superuser:
                    return redirect(reverse('admin:index'))
                else:
                    messages.error(request,"Invalid Username or Password")
                    return redirect('signin')
            return render(request,"signin.html",{"form":form_data})

class HomePageView(ListView):
    model = Vehicle                 
    template_name = "home.html"
    context_object_name = "vehicles"
    
