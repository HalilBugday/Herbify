from flask import Blueprint, render_template, request, current_app
from keras.utils.image_utils import load_img, img_to_array
from keras.models import load_model
import numpy as np
import os

views = Blueprint('views', __name__)

@views.route('/classification')
def classification():
    return render_template('identification-page.html')

@views.route('/predict', methods=['POST'])
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

            class_names = ['Daisy-papatya. Bu bir papatyadır ve familyası...', 'dandelion-karahindiba. bu bir karahindibadır ve familyası..', 
                           'rose-gül. Bu bir güldü ve familyası...', 'sunflower-ayçiçeği. Bu bir ayçiçeğidir ve familyası...']

            # Tahmin yap
            prediction = model.predict(img_array)
            predicted_class = class_names[np.argmax(prediction)]

            return render_template('prediction_results.html', image_path=image_path, predicted_class=predicted_class)
