from fastapi import FastAPI
from pydantic import BaseModel
import pickle
import numpy as np

app = FastAPI()

# Load the trained model
with open("classifier.pkl", "rb") as f:
    model = pickle.load(f)
    
@app.get("/")
def read_root():
    return {"message": "Fetal Health API is Running"}

# Input schema
class FetalInput(BaseModel):
    baseline_value: float
    accelerations: float
    fetal_movement: float
    uterine_contractions: float
    light_decelerations: float
    severe_decelerations: float
    prolongued_decelerations: float
    abnormal_short_term_variability: float
    mean_value_of_short_term_variability: float
    percentage_of_time_with_abnormal_long_term_variability: float
    mean_value_of_long_term_variability: float
    histogram_width: float
    histogram_min: float
    histogram_max: float
    histogram_number_of_peaks: float
    histogram_number_of_zeroes: float
    histogram_mode: float
    histogram_mean: float
    histogram_median: float
    histogram_variance: float
    histogram_tendency: float

# Predict endpoint
@app.post("/predict")
def predict(data: FetalInput):
    input_data = np.array([[value for value in data.dict().values()]])
    prediction = model.predict(input_data)[0]
    mapping = {1: "Normal", 2: "Suspect", 3: "Pathologic"}
    return {"prediction": mapping[int(prediction)]}