import requests
from fastapi import FastAPI

app = FastAPI()

@app.post("/trigger")
def trigger_upload():
    try:
        with open("photo.jpg", "rb") as file:
            response = requests.post("http://api:8000/upload", files={"file": file})
            
        return response.json()
        
    except Exception as e:
        return {"error": str(e)}