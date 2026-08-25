import joblib
import pandas as pd
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, Field
from typing import Literal

model = joblib.load('model/mental_health_pipeline.pkl')

app = FastAPI()

app.add_middleware(
     CORSMiddleware,
     allow_origins=["*"],
     allow_methods=["*"],
     allow_headers=["*"]
)


# A first Pydantic Model
class StudentData(BaseModel):
        Age                           :int = Field(..., ge=10, le=100)
        Gender                        :Literal['Male','Female']
        Country                       :str
        Academic_Level                :Literal['Undergraduate', 'Graduate', 'High School']
        Most_Used_Platform            :Literal['Facebook', 'LinkedIn', 'Instagram', 'Snapchat', 'Twitter',
       'YouTube', 'TikTok', 'LINE', 'KakaoTalk', 'VKontakte', 'WhatsApp',
       'WeChat']
        Purpose_Of_Use                :Literal['Networking', 'Education', 'Entertainment', 'News']
        Avg_Daily_Usage_Hours         :float = Field(..., ge=0, le=24)
        Daily_Unlocks                 :int = Field(...,ge=0)
        Study_Hours                   :float = Field(...,ge=0,le=24)
        Physical_Activity_Hours       :float = Field(...,ge=0,le=24)
        Sleep_Hours_Per_Night         :float = Field(...,ge=0,le=24)
        Stress_Level                  :Literal['Medium', 'Low', 'Very High', 'High']


# Describe what we send back
class predictionResponse(BaseModel):
     predicted_mental_health_score:float
     

@app.get('/')
def greet():
    return {'Welcome to my app'}

top_countries = [
        'Other','India','USA','Canada','Australia','UK','Germany','Mexico','Turkey','France'
         ]

@app.post('/predict', response_model=predictionResponse)
def predict(data: StudentData):

    country_group = data.Country if data.Country in top_countries else 'Other'
    input_row = pd.DataFrame([{
        'Age': data.Age,
        'Gender': data.Gender,
        'Country': data.Country,
        'Academic_Level': data.Academic_Level,
        'Most_Used_Platform': data.Most_Used_Platform,
        'Purpose_Of_Use': data.Purpose_Of_Use,
        'Avg_Daily_Usage_Hours': data.Avg_Daily_Usage_Hours,
        'Daily_Unlocks': data.Daily_Unlocks,
        'Study_Hours': data.Study_Hours,
        'Physical_Activity_Hours': data.Physical_Activity_Hours,
        'Sleep_Hours_Per_Night': data.Sleep_Hours_Per_Night,
        'Stress_Level': data.Stress_Level,
        'Grouped_Country': country_group,
    }])

    prediction : float = model.predict(input_row)[0]   #....we passing 0th dict in input_row to model for prediction
    return predictionResponse(predicted_mental_health_score=round(prediction,2))