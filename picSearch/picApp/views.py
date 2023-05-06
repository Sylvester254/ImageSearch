from django.shortcuts import render, redirect
import numpy as np
from picApp.models import MissingChild
from picApp.forms import MissingChildForm
from deepface import DeepFace

def submit_child(request):
    if request.method == 'POST':
        form = MissingChildForm(request.POST, request.FILES)
        if form.is_valid():
            child = form.save(commit=False)
            image = child.image.path
            image_encoding = DeepFace.represent(img_path=image, model_name='Facenet', enforce_detection=False)
            child.image_encoding = image_encoding.tobytes()
            child.save()
            return redirect('search_child')
    else:
        form = MissingChildForm()

    return render(request, 'submit_child.html', {'form': form})

def search_child(request):
    if request.method == 'POST':
        image = request.FILES['image']
        img_encoding = DeepFace.represent(img_path=image, model_name='Facenet', enforce_detection=False)
        
        missing_children = MissingChild.objects.all()
        similar_children = []

        for child in missing_children:
            stored_encoding = np.frombuffer(child.image_encoding, dtype=np.float64)
            similarity = DeepFace.verify(img_encoding, stored_encoding, model_name='Facenet', distance_metric='euclidean_l2', enforce_detection=False)
            if similarity['verified']:
                similar_children.append(child)

        return render(request, 'search_results.html', {'similar_children': similar_children})

    return render(request, 'search_child.html')
