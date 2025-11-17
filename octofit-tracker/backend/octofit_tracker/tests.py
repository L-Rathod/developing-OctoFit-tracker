from django.test import TestCase
from .models import User, Team, Activity, Workout, Leaderboard

class ModelTests(TestCase):
    def test_user_creation(self):
        team = Team.objects.create(name='Test Team')
        user = User.objects.create(username='testuser', email='test@example.com', first_name='Test', last_name='User', team=team)
        self.assertEqual(user.username, 'testuser')
        self.assertEqual(user.team.name, 'Test Team')

    def test_activity_creation(self):
        team = Team.objects.create(name='Test Team')
        user = User.objects.create(username='testuser', email='test@example.com', first_name='Test', last_name='User', team=team)
        activity = Activity.objects.create(user=user, activity_type='Running', duration=30, calories_burned=300, date='2025-11-17')
        self.assertEqual(activity.activity_type, 'Running')
        self.assertEqual(activity.user.username, 'testuser')

    def test_workout_creation(self):
        workout = Workout.objects.create(name='Test Workout', description='Test Desc', difficulty='Easy')
        self.assertEqual(workout.name, 'Test Workout')

    def test_leaderboard_creation(self):
        team = Team.objects.create(name='Test Team')
        leaderboard = Leaderboard.objects.create(team=team, total_calories=100, total_duration=60)
        self.assertEqual(leaderboard.team.name, 'Test Team')
        self.assertEqual(leaderboard.total_calories, 100)
