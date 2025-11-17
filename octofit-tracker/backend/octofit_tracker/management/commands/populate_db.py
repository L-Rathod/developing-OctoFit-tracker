from django.core.management.base import BaseCommand
from octofit_tracker.models import User, Team, Activity, Workout, Leaderboard
from django.db import connection

class Command(BaseCommand):
    help = 'Populate the octofit_db database with test data'

    def handle(self, *args, **options):
        # Clear all collections using raw MongoDB for Djongo compatibility
        from django.conf import settings
        from pymongo import MongoClient
        client = MongoClient(settings.DATABASES['default']['CLIENT']['host'])
        db = client[settings.DATABASES['default']['NAME']]
        db.user.delete_many({})
        db.team.delete_many({})
        db.activity.delete_many({})
        db.workout.delete_many({})
        db.leaderboard.delete_many({})

        # Create teams
        marvel = Team.objects.create(name='Marvel')
        dc = Team.objects.create(name='DC')

        # Create users
        users = [
            User(username='ironman', email='ironman@marvel.com', first_name='Tony', last_name='Stark', team=marvel),
            User(username='captainamerica', email='cap@marvel.com', first_name='Steve', last_name='Rogers', team=marvel),
            User(username='batman', email='batman@dc.com', first_name='Bruce', last_name='Wayne', team=dc),
            User(username='wonderwoman', email='wonderwoman@dc.com', first_name='Diana', last_name='Prince', team=dc),
        ]
        for user in users:
            user.save()
        marvel.members.set(users[:2])
        dc.members.set(users[2:])

        # Create workouts
        workout1 = Workout.objects.create(name='Super Strength', description='Strength training for heroes', difficulty='Hard')
        workout2 = Workout.objects.create(name='Agility Boost', description='Agility drills for speedsters', difficulty='Medium')
        workout1.suggested_for.set(users)
        workout2.suggested_for.set(users)

        # Create activities
        Activity.objects.create(user=users[0], activity_type='Running', duration=30, calories_burned=300, date='2025-11-17')
        Activity.objects.create(user=users[1], activity_type='Cycling', duration=45, calories_burned=400, date='2025-11-17')
        Activity.objects.create(user=users[2], activity_type='Swimming', duration=60, calories_burned=500, date='2025-11-17')
        Activity.objects.create(user=users[3], activity_type='Yoga', duration=40, calories_burned=200, date='2025-11-17')

        # Create leaderboard
        Leaderboard.objects.create(team=marvel, total_calories=700, total_duration=75)
        Leaderboard.objects.create(team=dc, total_calories=700, total_duration=100)

        # Ensure unique index on email using PyMongo
        db.user.create_index('email', unique=True)

        self.stdout.write(self.style.SUCCESS('octofit_db populated with test data.'))
