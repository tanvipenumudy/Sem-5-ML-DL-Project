from keras.models import model_from_json
from tensorflow.keras import Sequential
from tensorflow.keras.layers import Dense
import os
app_root = os.path.dirname(os.path.abspath(__file__))
def init1():
    target1 = os.path.join(app_root, 'burt.json')
    target2 = os.path.join(app_root, 'burt.h5')
    target3 = os.path.join(app_root, 'burt1.json')
    target4 = os.path.join(app_root, 'burt1.h5')
    json_file = open(target1, 'r')
    loaded_model_json = json_file.read()
    json_file.close()
    loaded_model = model_from_json(loaded_model_json)
    loaded_model.load_weights(target2)
    loaded_model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    json_file = open(target3, 'r')
    loaded_model1_json = json_file.read()
    json_file.close()
    loaded_model1 = model_from_json(loaded_model1_json)
    loaded_model1.load_weights(target4)
    loaded_model1.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
    return loaded_model, loaded_model1