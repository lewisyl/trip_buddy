from django.shortcuts import render,redirect
from django.contrib import messages
import bcrypt
from .models import User, Trip

### User Dashboard Page ###
def dashboard(request):
    if "userid" not in request.session:
        return redirect('/')
    else:
        context = {
            "user": User.objects.get(id=request.session['userid']),
            "my_trips": Trip.objects.filter(created_by=request.session['userid']),
            "other_trips": Trip.objects.exclude(created_by=request.session['userid']),
            "userid": request.session['userid'],
            "joined_trips": Trip.objects.exclude(users__isnull=True),
        }
        return render(request, "dashboard/dashboard.html",context)

def logout(request):
    request.session.clear()
    return redirect('/')

### Add New Trip Page ###
def add_trip(request):
    if "userid" not in request.session:
        return redirect('/')
    else:
        context= {
            "user": User.objects.get(id=request.session['userid']),
        }
        return render(request,'dashboard/add_trip.html',context)

def add_trip_process(request):
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/dashboard/add_trip')
    else:
        this_user = User.objects.get(id=request.session['userid'])
        Trip.objects.create(destination=request.POST['destination'], start_date=request.POST['start_date'], end_date=request.POST['end_date'], plan=request.POST['plan'], created_by=request.session['userid'])
        this_trip = Trip.objects.last().id
        this_user.trips.add(this_trip)
        
        return redirect("/dashboard")

### Edit Trip Page ###
def edit_trip(request, trip_id):
    if "userid" not in request.session:
        return redirect('/')
    else:
        context= {
            "user": User.objects.get(id=request.session['userid']),
            "edit_trip": Trip.objects.get(id=trip_id)
        }
        return render(request,'dashboard/edit_trip.html',context)

def edit_trip_process(request, trip_id):
    errors = Trip.objects.trip_validator(request.POST)
    if len(errors) > 0:
        for key, value in errors.items():
            messages.error(request, value)
        return redirect('/dashboard/'+trip_id+'/edit_trip')
    elif Trip.objects.get(id=trip_id).created_by != request.session['userid']:
        return redirect('/dashboard')
    else:
        this_trip = Trip.objects.get(id=trip_id)
        if request.POST['destination'] != "":
            this_trip.destination = request.POST['destination']
        if request.POST['start_date'] != "":
            this_trip.start_date = request.POST['start_date']
        if request.POST['end_date'] != "":
            this_trip.end_date = request.POST['end_date']
        if request.POST['plan'] != "":
            this_trip.plan = request.POST['plan']
        this_trip.save()
        return redirect("/dashboard")

### Trip Detail Page ###
def detail(request, trip_id):
    context= {
        "user": User.objects.get(id=request.session['userid']),
        "trip": Trip.objects.get(id=trip_id),
        "creater": User.objects.get(id=Trip.objects.get(id=trip_id).created_by),
        "joined_users": Trip.objects.exclude(users__isnull=True),
    }
    return render(request,'dashboard/trip_detail.html',context)

### Remove Trip ###
def remove(request, trip_id):
    if Trip.objects.get(id=trip_id).created_by != request.session['userid']:
        return redirect("/dashboard")
    else:
        Trip.objects.get(id=trip_id).delete()
        return redirect("/dashboard")


### Join Trip ###
def join(request, trip_id):
    this_user = User.objects.get(id=request.session['userid'])
    this_trip = Trip.objects.get(id=trip_id)
    if this_user.id == request.session['userid']:
        this_user.trips.add(this_trip)
    return redirect("/dashboard")

### Cancel Trip ###
def cancel(request, trip_id):
    this_user = User.objects.get(id=request.session['userid'])
    this_trip = Trip.objects.get(id=trip_id)
    if this_user.id == request.session['userid']:
        this_user.trips.remove(this_trip)
    return redirect("/dashboard")
