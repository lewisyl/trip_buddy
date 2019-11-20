from __future__ import unicode_literals
from django.db import models
import re
import datetime
from dateutil import parser
import bcrypt

class RegManager(models.Manager):
    def register_validator(self, postData):
        errors = {}
        NAME_REGEX = re.compile(r'[a-zA-Z]+( [a-zA-Z]+)*$')
        EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9._-]+\.[a-zA-Z]+$')
        DATE_REGEX = re.compile(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$')
        if len(postData['first_name'])<2 or len(postData['last_name'])<2:
            errors['name']="Both First Name and Last Name should contain at least 2 characters."
        elif not NAME_REGEX.match(postData['first_name']) or not NAME_REGEX.match(postData['last_name']):
            errors['name'] = "Both First Name and Last Name can ONLY contain letters and whitespace"
        
        if len(postData['email']) < 5:
            errors['email'] = "Email is required"
        elif not EMAIL_REGEX.match(postData['email']):
            errors['email'] = "Invalid Email Address, Please Try Again"
        else:
            for email in User.objects.all():
                if postData['email'] == email.email:
                    errors['email'] = "Email Address Has Already Existed"
        
        if len(postData['dob']) < 9 or not DATE_REGEX.match(postData['dob']):
            errors['dob'] = "Invalid Date of Birth. Make sure you follow the YYYY-MM-DD format."
        else:
            dob = parser.parse(postData['dob']).date()
            future = (datetime.date.today() - dob).days
            age = (datetime.date.today() - dob).days/365
            if age <13:
                errors['dob'] = "You must be over 13-year-old to register"
            elif future < 0:
                errors['dob'] = "Don't tell me you are from the future"
        if len(postData['password']) < 8:
            errors['password'] = "Password should contain at least 8 characters"
        elif postData['password'] != postData['confirm_pw']:
            errors['password'] = "The Password You Entered Is Not Matching, Please confirm and try again"

        return errors
    
    def login_validator(self, postData):
        errors = {}
        user = User.objects.filter(email=postData['login_email'])
        if len(user)==0:
            errors['login'] = "Invalid username/password"
        else:
            logged_user = user[0]
            if not bcrypt.checkpw(postData['login_password'].encode(), logged_user.password.encode()):
                errors['login'] = "Invalid username/password"
        return errors


class User(models.Model):
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    email = models.CharField(max_length=255)
    dob = models.DateField()
    password = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = RegManager()

