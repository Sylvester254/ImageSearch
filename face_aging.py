import os
import cv2
import numpy as np
from keras.preprocessing import image as kp_image
from FaceAging_IPCGAN.models import FaceAging

def age_face_image(image_path, target_age, base_dir='Face-Aging-with-Identity-Preserved-Conditional-Generative-Adversarial-Networks'):
    face_aging = FaceAging()

    # Load the input image
    img = cv2.imread(image_path)
    img = cv2.resize(img, (256, 256))[:, :, ::-1]

    # Predict the age of the input image
    age_img = kp_image.array_to_img(img)
    age_img.save('temp_age_img.jpg')
    input_age = face_aging.test_age('temp_age_img.jpg')
    os.remove('temp_age_img.jpg')

    # Age the input image to the target age
    ages = [1, 10, 20, 30, 40, 50, 60, 70]
    age_index = ages.index(target_age)
    condition = np.zeros((1, 8))
    condition[0, age_index] = 1

    if input_age != target_age:
        img = face_aging.age_one_image(img, condition)
    img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

    return img
