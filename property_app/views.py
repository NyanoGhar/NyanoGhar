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

#was working here - need to fix multiple image upload at a time

class ImageViewSet(APIView):
    permission_classes = [IsAuthenticated]
    parser_classes = [MultiPartParser, FormParser]

    def post(self, request):
        # Check if property id in request belongs to the authenticated user
        data = dict(request.data)
        print(data)
        property_id=data.get('property')
        # print(data,property_id)
        if not Property.objects.filter(owner=request.user, property_id=property_id).exists():
            return Response({'error': 'Property not found or does not be long to the user'}, status=status.HTTP_403_FORBIDDEN)

        if 'images' in request.FILES:
            images = request.FILES.getlist('images')
            image_data = []
            for image in images:
                data = {'property': property_id, 'image': image}
                serializer = ImageSerializer(data=data)
                if serializer.is_valid():
                    serializer.save()
                    image_data.append(serializer.data)
                else:
                    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
            return Response(image_data, status=status.HTTP_201_CREATED)
        else:
            return Response({'error': 'No images found in request'}, status=status.HTTP_400_BAD_REQUEST)


