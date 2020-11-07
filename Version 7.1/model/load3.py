import pickle 
import joblib 
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.ensemble import VotingClassifier
import os
app_root = os.path.dirname(os.path.abspath(__file__))
def init3():
    target1 = os.path.join(app_root, 'passage.pkl')
    target2 = os.path.join(app_root, 'passage_mm.pkl')
    loaded_model = joblib.load(target1)
    mm = joblib.load(target2)
    return loaded_model, mm