import os
from flask import Flask
from dotenv import load_dotenv
# Load .env file using:
load_dotenv()
app = Flask(__name__)
 
@app.route("/")
def hello():
  return "Hello World!"
 
app.run()