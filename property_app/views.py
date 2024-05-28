# views.py

from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Property, Image, View
from .serializers import PropertySerializer, ImageSerializer, ViewSerializer
from rest_framework.permissions import IsAuthenticated
from rest_framework.parsers import MultiPartParser, FormParser

class PropertyListAPIView(APIView):
    def get(self, request):
        properties = Property.objects.all()
        # Serialize properties along with associated images
        serialized_properties = []
        for prop in properties:
            prop_data = PropertySerializer(prop).data
            images = prop.images.all()  # Assuming you have a related name 'images' in the Property model
            image_data = ImageSerializer(images, many=True).data
            prop_data['images'] = image_data
            serialized_properties.append(prop_data)
        return Response(serialized_properties)


class PropertyCreateAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Associate authenticated user as owner of the house
        request.data['owner'] = request.user.id
        
        serializer = PropertySerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ImageViewSet(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        # Check if property id in request belongs to the authenticated user
        property_id = request.data.get('property')
        if not Property.objects.filter(owner=request.user, property_id=property_id).exists():
            return Response({'error': 'Property not found or does not belong to the user'}, status=status.HTTP_403_FORBIDDEN)

        images_data = request.data.get('images')
        if images_data:
            image_data = []
            for img_data in images_data:
                try:
                    # Save base64 image to the Image model
                    image_instance = Image(property_id=property_id)
                    image_instance.save_base64_image(img_data)
                    image_instance.save()
                    image_data.append({'image_id': image_instance.image_id})
                except Exception as e:
                    return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)
            return Response(image_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'No images found in request'}, status=status.HTTP_400_BAD_REQUEST)


class OwnerPropertyListAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        properties = Property.objects.filter(owner=request.user)
        serialized_properties = []
        for prop in properties:
            prop_data = PropertySerializer(prop).data
            images = prop.images.all() 
            image_data = ImageSerializer(images, many=True).data
            prop_data['images'] = image_data
            serialized_properties.append(prop_data)
        return Response(serialized_properties, status=status.HTTP_200_OK)