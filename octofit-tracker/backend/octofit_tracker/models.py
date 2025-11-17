from django.db import models
from djongo import models as djongo_models

class User(models.Model):
    id = djongo_models.ObjectIdField(primary_key=True, editable=False)
    username = models.CharField(max_length=150, unique=True)
    email = models.EmailField(unique=True)
    first_name = models.CharField(max_length=30)
    last_name = models.CharField(max_length=30)
    date_joined = models.DateTimeField(auto_now_add=True)
    team = models.ForeignKey('Team', null=True, blank=True, on_delete=models.SET_NULL)

class Team(models.Model):
    id = djongo_models.ObjectIdField(primary_key=True, editable=False)
    name = models.CharField(max_length=100, unique=True)
    created_at = models.DateTimeField(auto_now_add=True)
    members = models.ManyToManyField(User, related_name='teams', blank=True)

class Activity(models.Model):
    id = djongo_models.ObjectIdField(primary_key=True, editable=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    activity_type = models.CharField(max_length=50)
    duration = models.IntegerField(help_text='Duration in minutes')
    calories_burned = models.IntegerField()
    date = models.DateField()

class Workout(models.Model):
    id = djongo_models.ObjectIdField(primary_key=True, editable=False)
    name = models.CharField(max_length=100)
    description = models.TextField()
    difficulty = models.CharField(max_length=20)
    suggested_for = models.ManyToManyField(User, blank=True)

class Leaderboard(models.Model):
    id = djongo_models.ObjectIdField(primary_key=True, editable=False)
    team = models.ForeignKey(Team, on_delete=models.CASCADE)
    total_calories = models.IntegerField(default=0)
    total_duration = models.IntegerField(default=0)
    updated_at = models.DateTimeField(auto_now=True)
