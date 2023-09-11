import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestRegressor
from sklearn.svm import SVR
from sklearn.neighbors import KNeighborsRegressor
from sklearn.metrics import mean_squared_error
import matplotlib.pyplot as plt
import warnings
from sklearn.exceptions import DataConversionWarning
warnings.filterwarnings(action='ignore', category=UserWarning)


# data collection
def fetch_data(ticker, start_date, end_date=None):
    stock_data = yf.Ticker(ticker)
    return stock_data.history(start=start_date, end=end_date)

def add_features(data):
    data['MA'] = data['Close'].rolling(window=5).mean()
    data['Momentum'] = data['Close'] - data['Close'].shift(4)
    return data.dropna()

def forecast(model, X_last, days=7):
    forecasts = []
    for _ in range(days):
        next_day_prediction = model.predict([X_last])
        forecasts.append(next_day_prediction[0])

        X_last[0] = np.mean([X_last[0] * 5 - X_last[1] + next_day_prediction[0]])  # Update MA
        X_last[1] = next_day_prediction[0] - X_last[1] 
    return forecasts


def train_models(ticker, start_date, end_date=None):
    data = fetch_data(ticker, start_date, end_date)
    data = add_features(data)

    X = data[['MA', 'Momentum']]
    y = data['Close']

    train_size = int(len(X) * 0.8)
    X_train, X_test = X.iloc[:train_size], X.iloc[train_size:]
    y_train, y_test = y.iloc[:train_size], y.iloc[train_size:]

    models = {
        "Random Forest": RandomForestRegressor(n_estimators=100),
        "SVM": SVR(),
        "KNN": KNeighborsRegressor(n_neighbors=10)
    }

    predictions = {}
    forecasts_7 = {}
    forecasts_30 = {}

    for name, model in models.items():
        model.fit(X_train, y_train)
        preds = model.predict(X_test)
        predictions[name] = preds

        # Now compute the forecasts
        forecasts_7[name] = forecast(model, list(X_test.iloc[-1]), 7)
        forecasts_30[name] = forecast(model, list(X_test.iloc[-1]), 30)

        mse = mean_squared_error(y_test, preds)
        print(f"{name} Mean Squared Error: {mse}")

    return y_test, predictions, forecasts_7, forecasts_30

def plot_predictions(y_test, predictions, forecasts_7, forecasts_30):
    colors = ['blue', 'green', 'red']

    # Plotting actual predictions
    plt.figure(figsize=(16, 6))
    for i, (model_name, preds) in enumerate(predictions.items()):
        plt.subplot(1, 3, i+1)
        plt.plot(y_test.index, y_test.values, color='black', linewidth=2, label='True Data')
        plt.plot(y_test.index, preds, color=colors[i], linestyle='--', label=f'{model_name} Predictions')
        plt.xlabel('Date', fontsize=10)
        plt.ylabel('Stock Price', fontsize=10)
        plt.title(f'{model_name} Predictions', fontsize=12)
        plt.legend(loc='upper left')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()


    # Plotting 7-day forecasts
    future_dates_7 = pd.date_range(start=y_test.index[-1], periods=8)[1:]  # Exclude the last known date
    plt.figure(figsize=(16, 6))
    for i, (model_name, forecast) in enumerate(forecasts_7.items()):
        plt.subplot(1, 3, i+1)
        plt.plot(future_dates_7, forecast, color=colors[i], linestyle='--', label=f'{model_name} 7-Day Forecast')
        plt.xlabel('Date', fontsize=10)
        plt.ylabel('Stock Price', fontsize=10)
        plt.title(f'{model_name} 7-Day Forecast', fontsize=12)
        plt.legend(loc='upper left')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()


    # Plotting 30-day forecasts
    future_dates_30 = pd.date_range(start=y_test.index[-1], periods=31)[1:]  # Exclude the last known date
    plt.figure(figsize=(16, 6))
    for i, (model_name, forecast) in enumerate(forecasts_30.items()):
        plt.subplot(1, 3, i+1)
        plt.plot(future_dates_30, forecast, color=colors[i], linestyle='--', label=f'{model_name} 30-Day Forecast')
        plt.xlabel('Date', fontsize=10)
        plt.ylabel('Stock Price', fontsize=10)
        plt.title(f'{model_name} 30-Day Forecast', fontsize=12)
        plt.legend(loc='upper left')
        plt.grid(True, which='both', linestyle='--', linewidth=0.5)
    plt.tight_layout()
    plt.show()

def main(ticker):
    y_test, predictions, forecasts_7, forecasts_30 = train_models(ticker, start_date="2023-01-01")
    plot_predictions(y_test, predictions, forecasts_7, forecasts_30)

if __name__ == '__main__':
    main("GOOGL") 
