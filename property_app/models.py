from django.db import models
from django.db import models
from user_auth_app.models import User
import base64
import io
from PIL import Image as PILImage

TENANT_CHOICES = (
    ('EVERYONE', 'Everyone'),
    ('STUDENT', 'Student'),
    ('EMPLOYED', 'Employed'),
    ('FAMILY', 'Family'),
    ('UNMARRIED_MAN', 'Unmarried Man'),
    ('ONLY_FEMALES', 'Only Females'),
)
PROPERTY_TYPE_CHOICES=(
    ('FLAT','flat'),
    ('FLAT_SHARING','flat sharing'),
    ('ROOM','room'),
    ('HOSTEL','hostel'),
    ("HOUSE",'house')
)


class Property(models.Model):
    property_id = models.AutoField(primary_key=True)
    owner = models.ForeignKey(User,related_name='prop', on_delete=models.CASCADE)
    property_type = models.CharField(max_length=255,choices=PROPERTY_TYPE_CHOICES, blank=True)
    title = models.CharField(max_length=255, blank=True)
    description = models.TextField(blank=True)
    location = models.CharField(max_length=255,blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2,blank=True)
    num_rooms = models.IntegerField(blank=True)
    num_bathrooms = models.IntegerField(blank=True)
    amenities = models.TextField(blank=True)
    rules = models.TextField(blank=True)
    is_available = models.BooleanField(blank=True)
    tenant_include = models.CharField(max_length=255,choices=TENANT_CHOICES, blank=True)
    tenant_exclude= models.CharField(max_length=255,choices=TENANT_CHOICES, blank=True)
    # Add coordinate fields
    latitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)
    longitude = models.DecimalField(max_digits=9, decimal_places=6, blank=True, null=True)

    def __str__(self):
        return self.title


class Image(models.Model):
    image_id = models.AutoField(primary_key=True)
    property = models.ForeignKey('Property',related_name='images', on_delete=models.CASCADE)
    image = models.TextField()  # Changed from CharField to TextField

    def save_base64_image(self, base64_string, quality=60):
        try:
            # Decode base64 string
            img_data = base64.b64decode(base64_string)
            
            # Open image using PIL
            img = PILImage.open(io.BytesIO(img_data))
            
            # Compress image
            img = img.convert("RGB")  # Ensure the image is in RGB mode for compression
            img_io = io.BytesIO()
            img.save(img_io, format='JPEG', quality=quality)
            
            # Encode compressed image as base64
            compressed_base64_string = base64.b64encode(img_io.getvalue()).decode('utf-8')
            
            # Save compressed base64 image
            self.image = compressed_base64_string
        except Exception as e:
            # Handle exceptions such as invalid base64 strings or image processing errors
            raise ValueError("Failed to process image: {}".format(str(e)))

    def get_base64_image(self):
        return self.url

class View(models.Model):
    property_id = models.ForeignKey(Property, on_delete=models.CASCADE)
    viewer_count = models.PositiveIntegerField(default=0)
    

