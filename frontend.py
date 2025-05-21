from flask import Flask, render_template, request
import requests
from fastapi import HTTPException

app = Flask(__name__)

# FASTAPI_URL = "https://fastapi-transcriber.up.railway.app"
FASTAPI_URL = "https://fastapi-transcriber.onrender.com"


  # Make sure FastAPI is running here

@app.route("/", methods=["GET", "POST"])
def index():
    transcript = ""
    error = ""

    if request.method == "POST":
        video_url = request.form.get("video_url")

        try:
            response = requests.get(f"{FASTAPI_URL}/process", params={"video_url": video_url})

            if response.status_code == 200:
                data = response.json()
                transcript = data.get("transcript", "").strip()

                # If transcript is empty or missing
                if not transcript:
                    error = "Transcript not available."
            else:
                # FastAPI responded with an error
                error = error = f"Error {response.status_code}: {response.text}"
        except Exception as e:
            error = f"Request failed: {str(e)}"
        


    return render_template("index.html", transcript=transcript, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
