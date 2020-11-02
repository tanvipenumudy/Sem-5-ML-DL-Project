from keras.models import model_from_json
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
import os
app_root = os.path.dirname(os.path.abspath(__file__))
def init():
    target1 = os.path.join(app_root, 'schonell.json')
    target2 = os.path.join(app_root, 'schonell.h5')
    json_file = open(target1, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(target2)
    loaded_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return loaded_model