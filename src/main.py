from flask import Flask, send_from_directory
from flasgger import Swagger
from api.routes import api
import os

app = Flask(__name__, static_folder='static')
swagger = Swagger(app)
app.register_blueprint(api)

@app.route('/')
def index():
    return send_from_directory(app.static_folder, 'index.html')

if __name__ == "__main__":
    app.run(debug=True)