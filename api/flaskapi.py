from flask import Flask, jsonify, request, render_template
import time, datetime
import numpy as np

app = Flask(__name__,static_folder='/home/lhotter/mysite/static/', template_folder='/home/lhotter/mysite/templates/')
app.config['SERVER_NAME'] = 'lhotter.pythonanywhere.com'

def get_ctl_text(mean, median, std_d, data_type):
    if abs(mean - median) < 0.1 * std_d:
        return f"{data_type} data is normally distributed"
    elif mean > median:
        return f"{data_type} data is positively skewed"
    else:
        return f"{data_type} data is negatively skewed"

@app.route("/")
def landing():
    #Render html index file
    return render_template('index.html')

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

@app.route('/temp', methods=['POST'])
def add_data_temp():
    data = request.get_json()
    tempBuffer.temperature.buffer.append(data)
    tempBuffer.temperature_created.buffer.append((datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
    return jsonify({'message': 'Data added to tempBuffer array'}), 200

@app.route('/temp', methods=['GET'])
def get_data_temp():
    return tempBuffer.get(), 200

class HumiBuffer:
    def __init__(self):
        self.humidity = Buffer()
        self.humidity_created = Buffer()
        self.last_humi = 19.11
        self.mean_humi = 19.11
        self.median_humi = 19.11
        self.std_d_humi = 19.11
        self.ctl_t_humi = "19.11"
        self.plt_line_humi = "/#"
    def get(self):
        return jsonify({
            "humidity": self.humidity.buffer,
            "humidity_created": self.humidity_created.buffer,
            "last_humi": self.humidity.buffer[0] if self.humidity.buffer else None,
            "mean_humi": np.mean(self.humidity.buffer),
            "median_humi": np.median(self.humidity.buffer),
            "std_d_humi": np.std(self.humidity.buffer),
            "ctl_t_humi": get_ctl_text(np.mean(self.humidity.buffer), np.median(self.humidity.buffer), np.std(self.humidity.buffer), "Humidity"),
        })

humiBuffer = HumiBuffer()

@app.route('/humi', methods=['POST'])
def add_data_humi():
    data = request.get_json()
    humiBuffer.humidity.buffer.append(data)
    humiBuffer.humidity_created.buffer.append((datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
    return jsonify({'message': 'Data added to humiBuffer array'}), 200

@app.route('/humi', methods=['GET'])
def get_data_humi():
    return humiBuffer.get(), 200

class Btn1Buffer:
    def __init__(self):
        self.btn1 = Buffer()
        self.btn1_created = Buffer()
        self.last_btn1 = 1
    def get(self):
        return jsonify({
            "btn1": self.btn1.buffer,
            "btn1_created": self.btn1_created.buffer,
            "last_btn1": self.btn1.buffer[0] if self.btn1.buffer else None,
        })

btn1Buffer = Btn1Buffer()

@app.route('/btn1', methods=['POST'])
def add_data_btn1():
    data = request.get_json()
    btn1Buffer.btn1.buffer.append(data)
    btn1Buffer.btn1_created.buffer.append((datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
    return jsonify({'message': 'Data added to btn1Buffer array'}), 200

@app.route('/btn1', methods=['GET'])
def get_data_btn1():
    return btn1Buffer.get(), 200

class Btn2Buffer:
    def __init__(self):
        self.btn2 = Buffer()
        self.btn2_created = Buffer()
        self.last_btn2 = 1
    def get(self):
        return jsonify({
            "btn2": self.btn2.buffer,
            "btn2_created": self.btn2_created.buffer,
            "last_btn2": self.btn2.buffer[0] if self.btn2.buffer else None,
        })

btn2Buffer = Btn2Buffer()

@app.route('/btn2', methods=['POST'])
def add_data_btn2():
    data = request.get_json()
    btn1Buffer.btn1.buffer.append(data)
    btn1Buffer.btn1_created.buffer.append((datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
    return jsonify({'message': 'Data added to btn2Buffer array'}), 200

@app.route('/btn2', methods=['GET'])
def get_data_btn2():
    return btn2Buffer.get(), 200

class ErroBuffer:
    def __init__(self):
        self.erro = Buffer()
        self.erro_created = Buffer()
        self.last_erro = 1
    def get(self):
        return jsonify({
            "erro": self.erro.buffer,
            "erro_created": self.erro_created.buffer,
            "last_erro": self.erro.buffer[0] if self.erro.buffer else None,
        })

erroBuffer = ErroBuffer()

@app.route('/error', methods=['POST'])
def add_data_erro():
    data = request.get_json()
    erroBuffer.erro.buffer.append(data)
    erroBuffer.erro_created.buffer.append((datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
    return jsonify({'message': 'Data added to erroBuffer array'}), 200

@app.route('/error', methods=['GET'])
def get_data_erro():
    return erroBuffer.get(), 200

class FreqBuffer:
    def __init__(self):
        self.freq = Buffer()
        self.freq_created = Buffer()
        self.last_freq = 1
    def get(self):
        return jsonify({
            "freq": self.freq.buffer,
            "freq_created": self.freq_created.buffer,
            "last_freq": self.freq.buffer[0] if self.freq.buffer else None,
        })

freqBuffer = FreqBuffer()

@app.route('/freq', methods=['POST'])
def add_data_freq():
    data = request.get_json()
    freqBuffer.freq.buffer.append(data)
    freqBuffer.freq_created.buffer.append((datetime.datetime.now()).strftime("%Y-%m-%d %H:%M:%S"))
    return jsonify({'message': 'Data added to freqBuffer array'}), 200

@app.route('/freq', methods=['GET'])
def get_data_freq():
    return freqBuffer.get(), 200

if __name__ == "__main__":
    while True:
        app.run(debug=True, threaded=True)
        time.sleep(1)
