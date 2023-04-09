import random
import time
from flask import Flask

app = Flask(__name__)

@app.route('/')
def get_random_number():
    return str(random.randint(1, 100))