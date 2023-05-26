import os
import tempfile
import cv2
from django.shortcuts import render, redirect
import numpy as np
from picApp.models import MissingChild
from picApp.forms import MissingChildForm
from deepface import DeepFace
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.shortcuts import render, redirect
from django.core.files.images import ImageFile


# from picSearch import settings

from django.conf import settings
import os

from django.core.files.storage import default_storage

#from django.core.files.storage import default_storage

def submit_child(request):
    if request.method == 'POST':
        form = MissingChildForm(request.POST, request.FILES)
        if form.is_valid():
            child = form.save(commit=False)
            image_name = request.FILES['image'].name
            image_path = os.path.join('missing_children', image_name)
            image = os.path.join(settings.MEDIA_ROOT, image_path)

            # Create the missing_children directory if it doesn't exist
            if not os.path.exists(os.path.dirname(image)):
                os.makedirs(os.path.dirname(image))

            # Save the image file using default_storage
            image_file = request.FILES['image']
            default_storage.save(image_path, image_file)

            child.image.name = image_path
            child.image._committed = True  # Mark the image as committed

            # Generate the image encoding
            image_encoding = DeepFace.represent(img_path=image, model_name='Facenet', enforce_detection=False)
            child.image_encoding = np.array(image_encoding).tobytes()
            child.save()
            return redirect('search_child')
    else:
        form = MissingChildForm()

    return render(request, 'submit_child.html', {'form': form})

def search_child(request):
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

            return render(request, 'search_child.html', {'error': 'No face detected. Please upload an image with a face.'})

        missing_children = MissingChild.objects.all()
        similar_children = []

        for child in missing_children:
            child_image_path = os.path.join(settings.MEDIA_ROOT, child.image.name)

            # Perform similarity verification only if a face is detected
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

        # Sort the similar children by similarity percentage in reverse order
        similar_children.sort(key=lambda x: x[1], reverse=True)

        context = {'similar_children': similar_children}
        return render(request, 'search_results.html', context)

    return render(request, 'search_child.html')

