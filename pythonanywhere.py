from flask import Flask, jsonify
import time
import pandas as pd
import numpy as np
from keras.models import Sequential
from keras.layers import LSTM, Dense

# for plotting
import matplotlib.pyplot as plt

# for export img/png
import io
import base64

app = Flask(__name__)


@app.route("/")
def landing():
    # Get the data from the feeds
    temperature = pd.read_json(
        "https://io.adafruit.com/api/v2/quang_cao2002/feeds/sensor1/data"
    ).value
    humidity = pd.read_json(
        "https://io.adafruit.com/api/v2/quang_cao2002/feeds/sensor2/data"
    ).value
    humidity_created = pd.read_json(
        "https://io.adafruit.com/api/v2/quang_cao2002/feeds/sensor1/data"
    ).created_at
    humidity_created = pd.to_datetime(humidity_created)
    humidity_created = humidity_created.dt.strftime("%M:%S")
    temperature_created = pd.read_json(
        "https://io.adafruit.com/api/v2/quang_cao2002/feeds/sensor2/data"
    ).created_at

    # Get last value of each data
    last_temp = temperature[len(temperature) - 1]
    last_humid = humidity[len(humidity) - 1]
    last_temp = f'<p>{last_temp}°C</p>'
    last_humid = f'<p>{last_humid}g/m<sup>3</sup></p>'

    # Data visualization
    # Line
    # Temp
    plt.clf()
    plt.fill_between(humidity_created, temperature, color="red", alpha=0.2)
    plt.plot(humidity_created, temperature, color="red")
    plt.ylim(min(temperature) - 1, max(temperature) + 1)
    plt.title("Temperature over Time")
    plt.xlabel("Time")
    plt.ylabel("Temperature")
    plt.xticks(range(0, len(humidity_created), 4), rotation=90, fontsize=8)

    # Save the plot as a PNG image
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    # Encode the image in base64
    line_temp = base64.b64encode(buffer.getvalue()).decode()
    # Create the HTML code with the image
    line_temp_html = f'<img src="data:image/png;base64,{line_temp}">'
    buffer.truncate(0)

    # Humid
    plt.clf()
    plt.fill_between(humidity_created, humidity, color="blue", alpha=0.2)
    plt.plot(humidity_created, humidity, color="blue")
    plt.ylim(min(humidity) - 1, max(humidity) + 1)
    plt.title("Humidity over Time")
    plt.xlabel("Time")
    plt.ylabel("Humidity")
    plt.xticks(range(0, len(humidity_created), 4), rotation=90, fontsize=8)
    # Save the plot as a PNG image
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    # Encode the image in base64
    line_humid = base64.b64encode(buffer.getvalue()).decode()
    # Create the HTML code with the image
    line_humid_html = f'<img src="data:image/png;base64,{line_humid}">'
    buffer.truncate(0)

    # Scatter
    plt.clf()
    plt.figure()
    plt.scatter(humidity, temperature, color="red")
    plt.xlabel("Humidity")
    plt.ylabel("Temperature")
    plt.title("Temp and Humid against each other")
    plt.xticks(rotation=90)
    plt.yticks(fontsize=24)
    plt.plot(humidity, temperature, color="blue", ls="--")
    # Save the plot as a PNG image
    buffer = io.BytesIO()
    plt.savefig(buffer, format="png")
    buffer.seek(0)
    # Encode the image in base64
    scatter = base64.b64encode(buffer.getvalue()).decode()
    # Create the HTML code with the image
    scatter_html = f'<img src="data:image/png;base64,{scatter}">'
    buffer.truncate(0)

    # Statistical analysis
    # Mean
    mean_temperature = temperature.mean()
    mean_humidity = humidity.mean()

    # Median
    median_temperature = temperature.median()
    median_humidity = humidity.median()

    # Standard Deviation
    temperature_std = temperature.std()
    humidity_std = humidity.std()

    # Central tendency
    if abs(mean_temperature - median_temperature) < 0.1 * temperature_std:
        central_tendency_temp = "Temperature data is normally distributed"
    elif mean_temperature > median_temperature:
        central_tendency_temp = "Temperature data is positively skewed"
    else:
        central_tendency_temp = "Temperature data is negatively skewed"

    if abs(mean_humidity - median_humidity) < 0.1 * humidity_std:
        central_tendency_humi = "Humidity data is normally distributed"
    elif mean_humidity > median_humidity:
        central_tendency_humi = "Humidity data is positively skewed"
    else:
        central_tendency_humi = "Humidity data is negatively skewed"

    mean_temperature = f'<p>{mean_temperature}</p>'
    mean_humidity = f'<p>{mean_humidity}</p>'
    median_temperature = f'<p>{median_temperature}</p>'
    median_humidity = f'<p>{median_humidity}</p>'
    temperature_std = f'<p>{temperature_std}</p>'
    humidity_std = f'<p>{humidity_std}</p>'
    central_tendency_temp = '<p>Temperature data is negatively skewed</p>'
    central_tendency_humi = '<p>Humidity data is negatively skewed</p>'

    # Combine the data into a single dataframe
    data = pd.concat([temperature, humidity], axis=1)
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
    best_predict_temperature = str(best_predict[0])
    best_predict_humidity = str(best_predict[1])
    best_predict_temperature = f'<p style="color: darkred">{best_predict_temperature}</p>'
    best_predict_humidity = f'<p style="color: darkblue">{best_predict_humidity}</p>'

    html = (
        """
    <html lang="en">
      <head>
        <meta charset="UTF-8" />
        <meta http-equiv="X-UA-Compatible" content="IE=edge" />
        <meta name="viewport" content="width=device-width, initial-scale=1.0" />
        <title>WinnerX District10 Brother Club</title>
        <style>
          .button {
            background-color: #8a8a8a;
            width: fit-content;
            padding: 8px 16px;
            border-radius: 8px;
            color: #f9f9f9;
            font-weight: bold;
            font-size: 18px;
          }

          p {
            margin: 8px 0px;
          }

          h4 {
            margin: 16px 0px 8px 0px;
          }

          body {
            background-color: #121212;
            margin: 0px;
            display: grid;
            grid-template-columns: 1fr 2fr 1fr;
            grid-template-rows: 1fr;
            grid-column-gap: 0px;
            grid-row-gap: 0px;
          }
          body > div:nth-child(2) {
            margin: 0px;
            display: grid;
            grid-template-columns: 1fr;
            grid-template-rows: auto auto auto;
            grid-column-gap: 0px;
            grid-row-gap: 0px;
            font-family: "Ubuntu", sans-serif;
          }
          @media only screen and (max-width: 767px) {
            body {
              grid-template-columns: 0 1fr 0;
            }
          }
          header {
            background-color: #ffffff;
            width: calc(50% - 64px);
            padding: 16px 32px;
            display: grid;
            grid-template-columns: auto auto;
            grid-template-rows: 1fr;
            grid-column-gap: 16px;
            grid-row-gap: 0px;
            align-items: center;
            border-bottom: 1px solid black;
            position: fixed;
          }

          @media only screen and (max-width: 767px) {
            header {
              width: calc(100% - 64px);
            }
          }

          header > img {
            height: 32px;
            filter: opacity(50%);
          }
          header > div:nth-child(2) {
            display: grid;
            grid-template-columns: repeat(2, auto);
            grid-template-rows: 1fr;
            grid-column-gap: 8px;
            grid-row-gap: 0px;
            align-items: center;
          }

          header > div:nth-child(2) > img {
            height: 48px;
          }

          header > div:nth-child(2) > h2 {
            margin: 0px;
          }

          main {
            background-color: #f9f9f9;
            margin-top: calc(48px + 32px);
          }

          main > #intro {
            width: calc(100% - 64px);
            padding: 16px 32px;
          }

          main > #intro > p {
            color: #8a8a8a;
          }

          main > .mainBox {
            background-color: #ffffff;
            width: calc(100% - 24px - 64px);
            margin: 12px;
            padding: 16px 32px;
            box-shadow: 0px 0px 4px 1px rgba(0, 0, 0, 0.1);
            border-radius: 8px;
          }

          main > .mainBox > img {
            width: 100%;
          }

          main > .mainBox > h3,
          main > .mainBox > p:last-child {
            text-align: center;
            margin: 8px 0px;
            font-weight: bold;
          }

          footer {
            background-color: #ffffff;
            width: calc(100% - 64px);
            padding: 8px 32px;
            border-top: 1px solid black;
          }

          footer > div {
            display: grid;
            grid-template-columns: 1fr 2fr;
            grid-template-rows: 1fr;
            grid-column-gap: 16px;
            grid-row-gap: 0px;
            align-items: center;
          }
        </style>
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link rel="preconnect" href="https://fonts.googleapis.com" />
        <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin />
        <link
          href="https://fonts.googleapis.com/css2?family=Ubuntu:ital,wght@0,300;0,400;0,500;0,700;1,300;1,400;1,500;1,700&display=swap"
          rel="stylesheet"
        />
      </head>
      <body>
        <div></div>
        <div>
            <header>
          <img src="https://freesvg.org/img/menu-icon.png" alt="" />
          <div>
            <h2>WinnerX D10</h2>
            <img
              src="https://scontent.fhan3-3.fna.fbcdn.net/v/t1.15752-9/341262637_609432384429819_8258653605093456312_n.png?_nc_cat=108&ccb=1-7&_nc_sid=ae9488&_nc_ohc=C_ep2h8jqAoAX-sP07W&_nc_ht=scontent.fhan3-3.fna&oh=03_AdRA0eYYzgzVniTty47gqAYwax7HiG8WqtD_JrjJhVDhSw&oe=6462FD34"
              alt="winnerx-district10-brother-club"
            />
          </div>
        </header>
        <main>
          <div id="intro">
            <h1>Hi, Devs</h1>
            <p>Here's what's going on with our system!</p>
            <div id="refresh_button" class="button">Refresh</div>
            <script>
              document
                .getElementById("refresh_button")
                .addEventListener("click", function () {
                  location.reload();
                });
            </script>
          </div>
          <div id="ada_info" class="mainBox">
            <h2>Your AdaFruit Info</h2>
            <h5>ADAFRUIT_IO_USERNAME</h5>
            <p>quang_cao2002</p>
            <h5>ADAFRUIT_IO_KEY</h5>
            <p id="ADAFRUIT_IO_KEY">aio_OjGd13T3YszewBSyOnk6VadobQvp</p>
            <div id="ADAFRUIT_IO_KEY_show" class="button">Reveal</div>
            <script>
              document.getElementById("ADAFRUIT_IO_KEY").innerHTML = "...";
              document
                .getElementById("ADAFRUIT_IO_KEY_show")
                .addEventListener("click", function () {
                  var ada_key = document.getElementById("ADAFRUIT_IO_KEY");
                  if (ada_key.innerHTML === "...") {
                    ada_key.innerHTML = "aio_OjGd13T3YszewBSyOnk6VadobQvp";
                  } else {
                    ada_key.innerHTML = "...";
                  }
                });
            </script>
          </div>
          <div id="ada_temp" class="mainBox">
            <h2>Temperature</h2>
            <h4>Most recent value</h4>
            """+last_temp+"""
            <h4>Line Plot</h4>
            """+line_temp_html+"""
            <h4>Scatter Plot</h4>
            """+scatter_html+"""
            <h4>Mean value</h4>
            """+mean_temperature+"""
            <h4>Median value</h4>
            """+median_temperature+"""
            <h4>Standard Deviation value</h4>
            """+temperature_std+"""
            <h4>Central Tendency</h4>
            """+central_tendency_temp+"""
            <hr />
            <h3>Predicted Future value</h3>
            """+best_predict_temperature+"""
          </div>
          <div id="ada_humid" class="mainBox">
            <h2>Humidity</h2>
            <h4>Most recent value</h4>
            <p>"""+last_humid+"""</p>
            <h4>Line Plot</h4>
            """+line_humid_html+"""
            <h4>Scatter Plot</h4>
            """+scatter_html+"""
            <h4>Mean value</h4>
            """+mean_humidity+"""
            <h4>Median value</h4>
            """+median_humidity+"""
            <h4>Standard Deviation value</h4>
            """+humidity_std+"""
            <h4>Central Tendency</h4>
            """+central_tendency_humi+"""
            <hr />
            <h3>Predicted Future value</h3>
            """+best_predict_humidity+"""
          </div>
        </main>
        <footer>
          <div>
            <h4>Developer(s)</h4>
            <p>
              <a
                href="https://scontent.fhan4-2.fna.fbcdn.net/v/t1.15752-9/313218348_3264297373813206_5850094739383157825_n.jpg?_nc_cat=111&ccb=1-7&_nc_sid=ae9488&_nc_ohc=Xf_kvlF2rZMAX86f9Q7&_nc_ht=scontent.fhan4-2.fna&oh=03_AdTzhvm0f6_XpDyruPBXf56-2NAJiMgyLXWlJcb2Xd10EA&oe=646316E5"
                >Winner X District 10 Brother Libre Club</a
              >
            </p>
          </div>
          <div>
            <h4>Initial release</h4>
            <p>16 - 04 - 2023</p>
          </div>
          <div>
            <h4>Repository</h4>
            <p>
              <a
                href="https://scontent.fhan3-5.fna.fbcdn.net/v/t1.15752-9/318084426_5663633393733229_8341961371307645842_n.jpg?_nc_cat=110&ccb=1-7&_nc_sid=ae9488&_nc_ohc=EqfzyLqi0OsAX9WhLKU&_nc_ht=scontent.fhan3-5.fna&oh=03_AdT_3RTZ9JsJXrJ6Eiru1G1mLLuvcjoqEAvC_WWKJqKCeQ&oe=64634B10"
                >iot_ml</a
              >
              on Github
            </p>
          </div>
          <div>
            <h4>Written in</h4>
            <p>Python - HTML5 - CSS3 - ES2022</p>
          </div>
          <div>
            <h4>Server</h4>
            <p><a href="https://www.pythonanywhere.com/">PythonAnywhere</a></p>
          </div>
          <div>
            <h4>Available in</h4>
            <p>English</p>
          </div>
          <div>
            <h4>License</h4>
            <p>© Ông Đặng 2023</p>
          </div>

        </footer>
        </div>
        <div></div>
      </body>
    </html>
    """
    )
    return html


@app.route("/iot-ml-api")
def predict():
    # Load the data
    temperature = pd.read_json(
        "https://io.adafruit.com/api/v2/quang_cao2002/feeds/sensor1/data"
    ).value
    humidity = pd.read_json(
        "https://io.adafruit.com/api/v2/quang_cao2002/feeds/sensor2/data"
    ).value

    # Combine the data into a single dataframe
    data = pd.concat([temperature, humidity], axis=1)
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
    best_predict_temperature = str(best_predict[0])
    best_predict_humidity = str(best_predict[1])

    return jsonify({"temp": best_predict_temperature, "humid": best_predict_humidity})


if __name__ == "__main__":
    while True:
        app.run(debug=True)
        time.sleep(60)
