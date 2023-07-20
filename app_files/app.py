from fastapi import FastAPI

app = FastAPI()

@app.get("/")
async def root():
    return {"message": "Hello World!"}

@app.get("/test")
async def root():
    return {"message": "this is a test and it worked!"}