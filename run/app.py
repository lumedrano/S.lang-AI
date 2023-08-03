from flask import Flask, jsonify
from flask_cors import CORS
from gesture2text import gesture_to_text

app = Flask(__name__)
CORS(app)

@app.route('/api/gesture-to-text', methods=['GET'])
def api_gesture_to_text():
    sentence = gesture_to_text()
    return jsonify({'sentence': sentence})


if __name__ == '__main__':
    app.run(debug=True)






















# import threading
# from fastapi import FastAPI, Request
# from fastapi.templating import Jinja2Templates
# from fastapi.logger import logger
# import logging
# from gesture2text import gesture_to_text
# import asyncio

# app = FastAPI()

# # Set up templates directory
# templates = Jinja2Templates(directory="templates")

# # Global variable to keep track of the gesture recognition state
# is_gesture_mode_enabled = False
# translated_sentence = ""

# # Asynchronous function to start the gesture recognition loop
# async def start_gesture_recognition():
#     global is_gesture_mode_enabled, translated_sentence
#     is_gesture_mode_enabled = True
#     translated_sentence = gesture_to_text()
#     is_gesture_mode_enabled = False

# @app.get("/start_gesture")
# async def start_gesture():
#     # Check if gesture recognition is already running
#     global is_gesture_mode_enabled
#     if not is_gesture_mode_enabled:
#         # Start gesture recognition loop in a separate thread
#         threading.Thread(target=asyncio.run, args=(start_gesture_recognition(),), daemon=True).start()
#     return {"message": "Gesture recognition started."}

# @app.post("/gesture_to_text")
# async def convert_gesture_to_text():
#     # Process the gesture data here using the gesture_to_text function
#     global translated_sentence
#     return {"sentence": translated_sentence}

# @app.get("/")
# async def root(request: Request):
#     global translated_sentence
#     sentence = translated_sentence if translated_sentence else "Press 'Start Gesture' to begin."
#     return templates.TemplateResponse("index.html", {"request": request, "sentence": sentence})

# if __name__ == "__main__":
#     import uvicorn
#     logger.setLevel(logging.WARNING)
#     uvicorn.run(app, host="0.0.0.0", port=8000)
