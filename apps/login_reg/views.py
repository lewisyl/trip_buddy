from django.shortcuts import render,redirect
from django.contrib import messages
import bcrypt
from .models import User

def index(request):
    if "userid" in request.session:
        return redirect('/dashboard')
    else:
        return render(request, "login_reg/index.html")

def registering(request):
    errors = User.objects.register_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='register_fail')
        return redirect('/')
    else:
        password = request.POST['password']
        pw_hash = bcrypt.hashpw(password.encode(), bcrypt.gensalt())
        User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], dob=request.POST['dob'],password=pw_hash)
        return redirect('/dashboard')

def logging_in(request):
    errors = User.objects.login_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value, extra_tags='login_fail')
        return redirect('/')
    else:
        user = User.objects.filter(email=request.POST['login_email'])
        if len(user)>0:
            logged_user = user[0]
            if bcrypt.checkpw(request.POST['login_password'].encode(), logged_user.password.encode()):
                request.session['userid'] = logged_user.id
        return redirect('/dashboard')

# def success(request):
#     if "userid" not in request.session:
#         return redirect('/')
#     else:
#         context = {
#             "user": User.objects.filter(id=request.session['userid'])
#         }
#         return render(request, "wall/success.html",context)

# def logout(request):
#     request.session.clear()
#     return redirect('/')