from flask import Flask, send_from_directory
from flasgger import Swagger
from flask_cors import CORS
from api.routes import api
import os

app = Flask(__name__, static_folder='static')
CORS(app)  # <-- Add this line
swagger = Swagger(app)
app.register_blueprint(api)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
