from django.contrib.auth.models import AbstractUser
from django.db import models

# # Create your models here.

# # services and favegenres will need to be strings of lists - views will need to handle this
class User(AbstractUser):
    country = models.CharField(max_length=2, default='gb')    
    services = models.CharField(max_length=64, default='netflix')
    genres = models.CharField(max_length=64, default='404')

# class List(models.Model):
#     user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="owner")
#     listname = models.CharField(max_length=64)
#     # movies = models.

# # class Hidden(models.Model):
# #     user
# #     tmdb_id

# # class Movie(models.Model):
# #     user 
# #     tmdb_id
# #     rating
# #     review
# #     date
# #     timestamp

# # class Show(models.Model):
# #     user 
# #     tmdb_id
# #     rating
# #     review
# #     dates
# #     current_ep
# #     timestamp