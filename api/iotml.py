from flask import Flask, jsonify, request, render_template
import time, datetime
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense

app = Flask(__name__,static_folder='/home/lhmqk/mysite/static/', template_folder='/home/lhmqk/mysite/templates/')
app.config['SERVER_NAME'] = 'lhmqk.pythonanywhere.com'

def get_ctl_text(mean, median, std_d, data_type):
    if abs(mean - median) < 0.1 * std_d:
        return f"{data_type} data is normally distributed"
    elif mean > median:
        return f"{data_type} data is positively skewed"
    else:
        return f"{data_type} data is negatively skewed"

class Temp:
    def __init__(self):
        self.temperature = pd.read_json(
            "https://io.adafruit.com/api/v2/quang_cao2002/feeds/sensor1/data"
        ).value
        self.temperature_created = pd.read_json(
            "https://io.adafruit.com/api/v2/quang_cao2002/feeds/sensor1/data"
        ).created_at
class Humi:
    def __init__(self):
        self.humidity = pd.read_json(
            "https://io.adafruit.com/api/v2/quang_cao2002/feeds/sensor2/data"
        ).value
        self.humidity_created = pd.read_json(
            "https://io.adafruit.com/api/v2/quang_cao2002/feeds/sensor2/data"
        ).created_at

class Btn1:
    def __init__(self):
        self.button1 = pd.read_json(
            "https://io.adafruit.com/api/v2/quang_cao2002/feeds/button1/data"
        ).value
        self.btn1_created = pd.read_json(
            "https://io.adafruit.com/api/v2/quang_cao2002/feeds/button1/data"
        ).created_at
class Btn2:
    def __init__(self):
        self.button2 = pd.read_json(
            "https://io.adafruit.com/api/v2/quang_cao2002/feeds/button2/data"
        ).value
        self.btn2_created = pd.read_json(
            "https://io.adafruit.com/api/v2/quang_cao2002/feeds/button2/data"
        ).created_at
class Erro:
    def __init__(self):
        self.error = pd.read_json(
            "https://io.adafruit.com/api/v2/quang_cao2002/feeds/error-detect/data"
        ).value
        self.erro_created = pd.read_json(
            "https://io.adafruit.com/api/v2/quang_cao2002/feeds/error-detect/data"
        ).created_at
class Freq:
    def __init__(self):
        self.frequency = pd.read_json(
            "https://io.adafruit.com/api/v2/quang_cao2002/feeds/sending-freq/data"
        ).value
        self.freq_created = pd.read_json(
            "https://io.adafruit.com/api/v2/quang_cao2002/feeds/sending-freq/data"
        ).created_at

@app.route("/")
def landing():
    #Render html index file
    return render_template('index.html')

@app.route("/temp")
def temp():
    temp = Temp()
    return jsonify({
        "temperature": temp.temperature.tolist(),
        "temperature_created": temp.temperature_created.tolist(),
        "last_temp": temp.temperature[0].astype(float),
        "mean_temp": temp.temperature.mean().astype(float),
        "median_temp": temp.temperature.median().astype(float),
        "std_d_temp": temp.temperature.std().astype(float),
        "ctl_t_temp": get_ctl_text(temp.temperature.mean().astype(float), temp.temperature.median().astype(float), temp.temperature.std().astype(float), "Temperature"),
        # "plt_line_temp": create_plot(
        #     (pd.to_datetime(temp.temperature_created)).dt.strftime("%H:%M:%S"), temp.temperature.astype(float), "red", "Temperature over Time", "Time", "Temperature", "plt_line_temp.png")
    })

@app.route("/humi")
def humi():
    humi = Humi()
    return jsonify({
        "humidity": humi.humidity.tolist(),
        "humidity_created": humi.humidity_created.tolist(),
        "last_humi": humi.humidity[0].astype(float),
        "mean_humi": humi.humidity.mean().astype(float),
        "median_humi": humi.humidity.median().astype(float),
        "std_d_humi": humi.humidity.std().astype(float),
        "ctl_t_humi": get_ctl_text(humi.humidity.mean().astype(float), humi.humidity.median().astype(float), humi.humidity.std().astype(float), "Humidity"),
        # "plt_line_humi": create_plot(
        #     (pd.to_datetime(humi.humidity_created)).dt.strftime("%H:%M:%S"), humi.humidity.astype(float), "blue", "Humidity over Time", "Time", "Humidity", "plt_line_humi.png")
    })

@app.route("/btn1")
def btn1():
    btn1 = Btn1()
    return jsonify({
        "btn1": btn1.button1.tolist(),
        "btn1_created": btn1.btn1_created.tolist(),
        "last_btn1": btn1.button1[0].astype(float),
    })

@app.route("/btn2")
def btn2():
    btn2 = Btn2()
    return jsonify({
        "btn2": btn2.button2.tolist(),
        "btn2_created": btn2.btn2_created.tolist(),
        "last_btn2": btn2.button2[0].astype(float),
    })

@app.route("/erro")
def erro():
    erro = Erro()
    return jsonify({
        "erro": erro.error.tolist(),
        "erro_created": erro.erro_created.tolist(),
        "last_erro": erro.error[0],
    })

@app.route("/freq")
def freq():
    freq = Freq()
    return jsonify({
        "freq": freq.frequency.tolist(),
        "freq_created": freq.freq_created.tolist(),
        "last_freq": freq.frequency[0].astype(float),
    })

@app.route("/predict")
def predict():
    temp = Temp().temperature
    humi = Humi().humidity
    # Combine the data into a single dataframe
    data = pd.concat([temp, humi], axis=1)
    data.columns = ["temperature", "humidity"]

    # Split the data into training and testing sets
    train_size = int(len(data) * 0.8)
    train_data = data.iloc[:train_size, :]
    test_data = data.iloc[train_size:, :]

    # Normalize the data
    mean = train_data.mean()
    std = train_data.std()
    train_data = (train_data - mean) / std
    test_data = (test_data - mean) / std

    # Prepare the data for LSTM
    def prepare_data(data, look_back=1):
        X, y = [], []
        for i in range(len(data) - look_back - 1):
            X.append(data[i : (i + look_back), :])
            y.append(data[i + look_back, :])
        return np.array(X), np.array(y)

    look_back = 10
    train_X, train_y = prepare_data(train_data.values, look_back)
    test_X, test_y = prepare_data(test_data.values, look_back)

    # Build the LSTM model
    model = Sequential()
    model.add(LSTM(50, input_shape=(look_back, 2)))
    model.add(Dense(2))
    model.compile(loss="mean_squared_error", optimizer="adam")

    # Train the model
    model.fit(train_X, train_y, epochs=100, batch_size=32, verbose=2)

    # Make predictions on the test data
    test_predict = model.predict(test_X)

    # Inverse transform the predictions and actual values
    test_predict = (test_predict * std.values) + mean.values
    test_y = (test_y * std.values) + mean.values

    # Select the best predicted value for temperature and humidity
    best_predict = test_predict[-1, :]
    return jsonify({
        "prdt_temp": str(best_predict[0]),
        "prdt_humi": str(best_predict[1])
    })

class Buffer:
    def __init__(self):
        self.buffer = []
        self.size = 100
    def append(self, data):
        if len(self.buffer) < self.size:
            self.buffer.append(data)
        else:
            self.buffer.pop(0)
            self.buffer.append(data)
    def get(self):
        return self.buffer

class TempBuffer:
    def __init__(self):
        self.temperature = Buffer()
        self.temperature_created = Buffer()
        self.last_temp = 19.11
        self.mean_temp = 19.11
        self.median_temp = 19.11
        self.std_d_temp = 19.11
        self.ctl_t_temp = "19.11"
        self.plt_line_temp = "/#"
    def get(self):
        return jsonify({
            "temperature": self.temperature.buffer,
            "temperature_created": self.temperature_created.buffer,
            "last_temp": self.temperature.buffer[0] if self.temperature.buffer else None,
            "mean_temp": np.mean(self.temperature.buffer),
            "median_temp": np.median(self.temperature.buffer),
            "std_d_temp": np.std(self.temperature.buffer),
            "ctl_t_temp": get_ctl_text(np.mean(self.temperature.buffer), np.median(self.temperature.buffer), np.std(self.temperature.buffer), "Temperature"),
            # "plt_line_temp": create_plot(
            #     self.temperature_created.buffer, self.temperature.buffer, "red", "Temperature over Time", "Time", "Temperature", "plt_line_temp.png") if self.temperature.buffer else None
        })

tempBuffer = TempBuffer()

@app.route('/addTemp', methods=['POST'])
def add_data():
    data = request.get_json()
    tempBuffer.temperature.buffer.append(data)
    tempBuffer.temperature_created.buffer.append((datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
    return jsonify({'message': 'Data added to tempBuffer array'}), 200

@app.route('/addTemp', methods=['GET'])
def get_data():
    return tempBuffer.get(), 200

if __name__ == "__main__":
    while True:
        app.run(debug=True, threaded=True)
        time.sleep(1)
