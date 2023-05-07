from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.conf import settings
from .models import MissingChild
from deepface import DeepFace
import os
import tempfile

@api_view(['POST'])
def search_child_api(request):
    if request.method == 'POST':
        image = request.FILES['image']

        # Save the uploaded image to a temporary file
        temp_image = tempfile.NamedTemporaryFile(delete=False)
        temp_image.write(image.read())
        temp_image.flush()

        img_encoding = DeepFace.represent(img_path=temp_image.name, model_name='Facenet', enforce_detection=False)

        missing_children = MissingChild.objects.all()
        similar_children = []

        for child in missing_children:
            child_image_path = os.path.join(settings.MEDIA_ROOT, child.image.name)
            similarity = DeepFace.verify(temp_image.name, child_image_path, model_name='Facenet', distance_metric='euclidean_l2', enforce_detection=False)
            if similarity['verified']:
                similar_children.append(child)

        # Clean up the temporary file
        temp_image.close()
        os.unlink(temp_image.name)

        # Serialize the similar_children queryset
        results = []
        for child in similar_children:
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
            })

        return Response(results, status=status.HTTP_200_OK)

    return Response(status=status.HTTP_400_BAD_REQUEST)
