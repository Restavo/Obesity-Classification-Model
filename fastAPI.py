import uvicorn
import pickle
import pandas as pd
from fastapi import FastAPI
from pydantic import BaseModel

# 1. Inisialisasi Aplikasi FastAPI
app = FastAPI(
    title="Obesity Level Prediction API",
    description="An API to predict obesity levels based on lifestyle and health data.",
    version="1.0.0"
)

# 2. Muat Model dan Label Encoder
try:
    with open("obesity_classification_pipeline.pkl", "rb") as f:
        model_pipeline = pickle.load(f)
    with open("obesity_label_encoder.pkl", "rb") as f:
        label_encoder = pickle.load(f)
    print("Model and Label Encoder loaded successfully.")
except FileNotFoundError:
    print("Error: Model or Label Encoder file not found. Please ensure they are in the correct directory.")
    model_pipeline = None
    label_encoder = None

# 3. Definisikan Model Input menggunakan Pydantic
class PatientData(BaseModel):
    Gender: str
    Age: int
    Height: float
    Weight: float
    family_history_with_overweight: str
    FAVC: str
    FCVC: float
    NCP: float
    CAEC: str
    SMOKE: str
    CH2O: float
    SCC: str
    FAF: float
    TUE: float
    CALC: str
    MTRANS: str
    
    class Config:
        schema_extra = {
            "example": {
                "Gender": "Male",
                "Age": 25,
                "Height": 1.80,
                "Weight": 80,
                "family_history_with_overweight": "yes",
                "FAVC": "yes",
                "FCVC": 2,
                "NCP": 3,
                "CAEC": "Sometimes",
                "SMOKE": "no",
                "CH2O": 2,
                "SCC": "no",
                "FAF": 1,
                "TUE": 1,
                "CALC": "no",
                "MTRANS": "Public_Transportation"
            }
        }

# 4. Buat Endpoint
@app.get("/")
def read_root():
    return {"message": "Welcome to the Obesity Prediction API!"}

@app.post("/predict")
def predict_obesity(data: PatientData):

# Endpoint untuk memprediksi tingkat obesitas.
# Menerima data pasien dan mengembalikan prediksi tingkat obesitas.
    
    if not model_pipeline or not label_encoder:
        return {"error": "Model not loaded. Cannot make predictions."}

    input_data = data.dict()
    input_df = pd.DataFrame([input_data])

    prediction_encoded = model_pipeline.predict(input_df)
    prediction_label = label_encoder.inverse_transform(prediction_encoded)

    return {
        "prediction_code": int(prediction_encoded[0]),
        "predicted_level": prediction_label[0]
    }
if __name__ == "__main__":
    uvicorn.run(app, host="127.0.0.1", port=8000)