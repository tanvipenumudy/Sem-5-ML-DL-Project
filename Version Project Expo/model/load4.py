import pickle 
import joblib 
from sklearn.tree import DecisionTreeClassifier
from sklearn.tree import DecisionTreeRegressor
import os
app_root = os.path.dirname(os.path.abspath(__file__))
def init4():
    target1 = os.path.join(app_root, 'memory.pkl')
    target2 = os.path.join(app_root, 'memory_mm.pkl')
    target3 = os.path.join(app_root, 'memory1.pkl')
    target4 = os.path.join(app_root, 'memory_mm1.pkl')
    loaded_model = joblib.load(target1)
    mm = joblib.load(target2)
    loaded_model1 = joblib.load(target3)
    mm1 = joblib.load(target4)
    return loaded_model, loaded_model1, mm, mm1