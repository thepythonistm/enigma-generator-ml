from django.db import models
class Riddle(models.Model):
    riddle = models.TextField()
    answer = models.TextField()
    difficulty = models.CharField(max_length=20)
    created_at = models.DateTimeField(auto_now_add=True)


