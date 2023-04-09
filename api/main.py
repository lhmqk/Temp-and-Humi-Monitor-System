from flask import Flask
import random
import time
app = Flask(__name__)

@app.route('/')
def get_random_number():
    return str(random.randint(1, 100))

if __name__ == '__main__':
    while True:
        app.run(debug=True)
        time.sleep(60)