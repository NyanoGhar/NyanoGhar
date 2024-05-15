from django.db import models
from django.db import models
from user_auth_app.models import User

class Property(models.Model):
    property_id = models.IntegerField(primary_key=True)
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    property_type = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    description = models.TextField()
    location = models.CharField(max_length=255)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    num_rooms = models.IntegerField()
    num_bathrooms = models.IntegerField()
    amenities = models.TextField()
    rules = models.TextField()
    is_available = models.BooleanField()
    tenant_type = models.CharField(max_length=255)

    def __str__(self):
        return self.title

class Image(models.Model):
    image_id = models.IntegerField(primary_key=True)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    url = models.CharField(max_length=255)

class View(models.Model):
    view_id = models.IntegerField(primary_key=True)
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    viewer_id = models.ForeignKey(User, on_delete=models.CASCADE)
    viewed_at = models.DateTimeField()
    

