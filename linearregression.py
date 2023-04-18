from Adafruit_IO import Client
import pandas as pd
from statsmodels.tsa.arima.model import ARIMA
import numpy as np

# for plotting
import matplotlib.pyplot as plt

# extract day and month from timestamps
from datetime import datetime

# ml
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeRegressor
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler

# Set your Adafruit IO credentials
ADAFRUIT_IO_USERNAME = "quang_cao2002"
ADAFRUIT_IO_KEY = "aio_OjGd13T3YszewBSyOnk6VadobQvp"

# Create an instance of the Adafruit IO client
aio = Client(ADAFRUIT_IO_USERNAME, ADAFRUIT_IO_KEY)

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

# Data visualization

# Line
# Dual-axis chart
fig, ax1 = plt.subplots(figsize=(32, 16))

color = "tab:blue"
ax1.set_xlabel("Time")
ax1.set_ylabel("Humidity", color=color)
ax1.plot(humidity_created, humidity, color=color)
ax1.tick_params(axis="y", labelcolor=color)
plt.xticks(rotation=90)

ax2 = ax1.twinx()

color = "tab:red"
ax2.set_ylabel("Temperature", color=color)
ax2.plot(humidity_created, temperature, color=color)
ax2.tick_params(axis="y", labelcolor=color)
plt.title("Temperature And Humimidy Data Over Time")
fig.legend(["Humidity", "Temperature"], loc="upper right")
plt.xticks(rotation=90)
plt.grid(True)
plt.show()

plt.fill_between(humidity_created, temperature, color="red", alpha=0.2)
plt.plot(humidity_created, temperature, color="red")
plt.ylim(min(temperature) - 1, max(temperature) + 1)
# set chart title and axis labels
plt.title("Temperature over Time")
plt.xlabel("Time")
plt.ylabel("Temperature")
plt.xticks(range(0, len(humidity_created), 4), rotation=90, fontsize=8)
plt.show()
# ------------
plt.fill_between(humidity_created, humidity, color="blue", alpha=0.2)
plt.plot(humidity_created, humidity, color="blue")
plt.ylim(min(humidity) - 1, max(humidity) + 1)
# set chart title and axis labels
plt.title("Humidity over Time")
plt.xlabel("Time")
plt.ylabel("Humidity")
plt.xticks(range(0, len(humidity_created), 4), rotation=90, fontsize=8)
plt.show()

# Scatter
plt.figure()
plt.scatter(humidity, temperature, color="red")
plt.xlabel("Humidity")
plt.ylabel("Temperature")
plt.title("Temp and Humid against each other")
plt.xticks(rotation=90)
plt.yticks(fontsize=24)
plt.plot(humidity, temperature, color="blue", ls="--")
plt.show()

# Statistical analysis
# Mean
mean_temperature = temperature.mean()
mean_humidity = humidity.mean()
print("mean_temperature: ", mean_temperature)
print("mean_humidity: ", mean_humidity)
# Median
median_temperature = temperature.median()
median_humidity = humidity.median()
print("median_temperature: ", median_temperature)
print("median_humidity: ", median_humidity)
# Standard Deviation
temperature_std = temperature.std()
humidity_std = humidity.std()
print("temperature_std: ", temperature_std)
print("humidity_std: ", humidity_std)
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

print("central_tendency_temp: ", central_tendency_temp)
print("central_tendency_humi: ", central_tendency_humi)

# Correlation
# 1 indicates a perfect positive correlation, 0 indicates no correlation, and -1 indicates a perfect negative correlation
correlation = temperature.corr(humidity)
print("correlation: ", correlation)

# Machine learning
# Linear regression
lrData = pd.DataFrame({"temperature": temperature, "humidity": humidity})
# Normalize the data
scaler = MinMaxScaler()
data_norm = scaler.fit_transform(lrData)

# Add lag features
data_lag = pd.DataFrame(data_norm, columns=["temperature", "humidity"])
for i in range(1, 4):
    data_lag[f"temperature_lag{i}"] = data_lag["temperature"].shift(i)
    data_lag[f"humidity_lag{i}"] = data_lag["humidity"].shift(i)
data_lag.dropna(inplace=True)

# Split the data into training and testing sets
X_train, X_test, y_train, y_test = train_test_split(
    data_lag.drop(["temperature", "humidity"], axis=1),
    data_lag[["temperature", "humidity"]],
    test_size=0.2,
    random_state=42,
)

# Train the model
model = LinearRegression()
model.fit(X_train, y_train)

# Evaluate the model
y_pred = model.predict(X_test)
mse = mean_squared_error(y_test, y_pred)
print(f"MSE: {mse}")

# Predict the values
X_pred = data_lag.drop(["temperature", "humidity"], axis=1).tail(1)
y_pred = model.predict(X_pred)

# Inverse transform the predicted values
y_pred_inv = scaler.inverse_transform(y_pred)

# Print the predicted values
print(f"Predicted temperature: {y_pred_inv[0][0]}")
print(f"Predicted humidity: {y_pred_inv[0][1]}")


# # Define the ARIMA model for humidity
# humidity_model = ARIMA(humidity, order=(1, 1, 1))
# humidity_results = humidity_model.fit()

# # Make a one-step prediction for humidity
# humidity_forecast = humidity_results.forecast()

# # Define the ARIMA model for temperature
# temperature_model = ARIMA(temperature, order=(1, 1, 1))
# temperature_results = temperature_model.fit()

# # Make a one-step prediction for temperature
# temperature_forecast = temperature_results.forecast()

# print(humidity_forecast.values[0])
# print(temperature_forecast.values[0])
