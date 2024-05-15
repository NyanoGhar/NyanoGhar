from django.db import models

class User(models.Model):
    user_id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=255)
    email = models.EmailField()
    password_hash = models.CharField(max_length=255)
    is_owner = models.BooleanField()

    def __str__(self):
        return self.username
