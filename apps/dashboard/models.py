from __future__ import unicode_literals
from django.db import models
from apps.login_reg.models import User
import re

class TripManager(models.Manager):
    def trip_validator(self,postData):
        errors = {}
        STR_REGEX = re.compile(r'[a-zA-Z0-9_]+( [a-zA-Z0-9_]+)*$')
        PLAN_REGEX = re.compile(r'^(.|\s)*[a-zA-Z]+(.|\s)*$')
        DATE_REGEX = re.compile(r'^\d{4}\-(0[1-9]|1[012])\-(0[1-9]|[12][0-9]|3[01])$')
        
        if len(postData['destination']) < 3:
            errors['destination'] = "Destination should contain at least 3 characters"
        elif not STR_REGEX.match(postData['destination']):
            errors['destination'] = "Destination should not contain special characters"

        if len(postData['start_date']) < 10 or not DATE_REGEX.match(postData['start_date']):
            errors['start_date'] = "Invalid Start Date. Please make sure you follow the YYYY-MM-DD format."

        if len(postData['end_date']) < 10 or not DATE_REGEX.match(postData['end_date']):
            errors['end_date'] = "Invalid End Date. Please make sure you follow the YYYY-MM-DD format."

        if len(postData['plan']) < 10:
            errors['plan'] = "Plan description should contain at least 10 characters"
        elif not PLAN_REGEX.match(postData['plan']):
            errors['plan'] = "Please enter a valid plan description"

        return errors

    

class Trip(models.Model):
    destination = models.CharField(max_length=255)
    start_date = models.DateField()
    end_date = models.DateField()
    plan = models.TextField()
    created_by = models.IntegerField()
    users = models.ManyToManyField(User, related_name="trips")
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    objects = TripManager()
