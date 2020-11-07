import pickle 
import joblib 
from sklearn.svm import SVC
import os
app_root = os.path.dirname(os.path.abspath(__file__))
def init2():
    target = os.path.join(app_root, 'wepman.pkl')
    loaded_model = joblib.load(target)
    return loaded_model