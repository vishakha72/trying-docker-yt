from flask import Flask, render_template, request
import requests

app = Flask(__name__)

# Change this to your actual backend URL on Render
FASTAPI_URL = "https://your-backend-service-name.onrender.com"

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
                if not transcript:
                    error = "Transcript not available."
            else:
                error = f"Error {response.status_code}: {response.text}"
        except Exception as e:
            error = f"Request failed: {str(e)}"

    return render_template("index.html", transcript=transcript, error=error)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
