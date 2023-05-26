from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from .models import MissingChild
from deepface import DeepFace
import os
import tempfile

from rest_framework.views import exception_handler
import logging

logger = logging.getLogger(__name__)

@api_view(['POST'])
def search_child_api(request):
    try:
        if request.method == 'POST':
            image = request.FILES['image']

            # Save the uploaded image to a temporary file
            temp_image = tempfile.NamedTemporaryFile(delete=False)
            temp_image.write(image.read())
            temp_image.flush()

            # Perform face detection on the image
            try:
                detected_faces = DeepFace.extract_faces(temp_image.name, enforce_detection=True)
            except ValueError as e:
                # Clean up the temporary file
                temp_image.close()
                os.unlink(temp_image.name)

                return Response({'detail': 'No face detected. Please upload an image with a face.'}, status=status.HTTP_400_BAD_REQUEST)

            missing_children = MissingChild.objects.all()
            similar_children = []

            for child in missing_children:
                child_image_path = os.path.join(settings.MEDIA_ROOT, child.image.name)
                similarity = DeepFace.verify(temp_image.name, child_image_path, model_name='Facenet', distance_metric='euclidean_l2', enforce_detection=False)
                if similarity['verified']:
                    distance = similarity['distance']
                    distance = float(distance)
                    similarity_percentage = round(1 / (1 + distance) * 100, 2)
                    if similarity_percentage > 60:
                        similar_children.append((child, similarity_percentage))

            # Clean up the temporary file
            temp_image.close()
            os.unlink(temp_image.name)

            # Sort by similarity distance (from smallest to largest)
            similar_children.sort(key=lambda x: x[1])

            # Serialize the similar_children queryset
            results = []
            for child, similarity_percentage in similar_children:
                results.append({
                    'id': child.id,
                    'name': child.name,
                    'age': child.age,
                    'image_url': child.image.url,
                    'date_missing': child.date_missing,
                    'place_of_birth': child.place_of_birth,
                    'last_seen': child.last_seen,
                    'guardian_name': child.guardian_name,
                    'guardian_contact': child.guardian_contact,
                    'similarity_distance': similarity_percentage,
                })

            return Response(results, status=status.HTTP_200_OK)

    except Exception as e:
        # Log the error
        logger.error('An error occurred when searching for the child', exc_info=True)

        # Return a 500 response with a helpful error message
        return Response({'detail': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
