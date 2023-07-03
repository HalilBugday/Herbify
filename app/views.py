from flask import Blueprint, render_template, request, current_app
from keras.utils.image_utils import load_img, img_to_array
from keras.models import load_model
from flask_login import current_user
from .models import User ,db

import numpy as np
import os

views = Blueprint('views', __name__)

@views.route('/classification')
def classification():
    return render_template('identification-page.html')

@views.route('/predict', methods=['POST', 'GET'])
def predict():
    if request.method == 'POST':
        # Gelen görüntüyü kaydet
        image_file = request.files['image']
        if image_file:
            image_path = os.path.join(current_app.config['UPLOAD_FOLDER'], image_file.filename)
            print("IMAGE PATH IS AS FOLLOWS!!:", image_path)
            image_file.save(image_path)

            # Görüntüyü yükle ve yeniden boyutlandır
            img = load_img(image_path, target_size=(224, 224))
            img_array = img_to_array(img)
            img_array = np.expand_dims(img_array, axis=0)

            # Modeli yükle
            model_path = os.path.join(current_app.root_path, 'modelVersion1.h5')
            model = load_model(model_path)

            class_names = ['daisy-papatya.', 'dandelion-karahindiba.', 'rose-gül.', 'sunflower-ayçiçeği.']
            

            

            # Tahmin yap
            prediction = model.predict(img_array)
            predicted_class = class_names[np.argmax(prediction)]

            if predicted_class == 'daisy-papatya.':
                    photo = 'static/daisy.jpeg'
            elif predicted_class == 'dandelion-karahindiba.':
                    photo = 'static/dandelion.jpeg'
            elif predicted_class == 'rose-gül.':
                    photo = 'static/rose.jpeg'
            elif predicted_class == 'sunflower-ayçiçeği.':
                    photo = 'static/sunflower.jpeg'



            print(predicted_class)

           #for achievements
            if current_user.is_authenticated:
                user = User.query.get(current_user.id)
                if user:
                    user.identification_count += 1
                    db.session.commit()

            return render_template('prediction_results.html', photo=photo, predicted_class=predicted_class)
