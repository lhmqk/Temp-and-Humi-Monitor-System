import random
import time
from flask import Flask

app = Flask(__name__)

@app.route('/')
def get_random_number():
    return str(random.randint(1, 100))

if __name__ == '__main__':
    while True:
        app.run()
        time.sleep(60)