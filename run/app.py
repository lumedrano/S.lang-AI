from fastapi import FastAPI
from main import gesture_to_text

app = FastAPI()
sentence = gesture_to_text()
@app.get("/")
async def root():
    return {"message": sentence} #works

# @app.get("/test")
# async def root():
#     return {"message": "this is a test and it worked!"}

