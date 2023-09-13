# Stock Price Predictor

This project leverages machine learning models to predict stock prices based on historical data, aiming to provide insights and future forecasts. By default, the tool is set to predict Google's stock ("GOOGL") from the start of 2023. The main goal is to compare the efficacy of different models in stock prediction.

## Features

- **Data Retrieval**: Uses `yfinance` to fetch historical stock data.
- **Feature Engineering**: Adds features like Moving Average and Momentum to the dataset to improve predictions.
- **Multiple Model Predictions**: Implements and compares predictions from Random Forest, Support Vector Machine (SVM), and K-Nearest Neighbors (KNN) models.
- **Forecasts**: Provides short-term (7-day) and medium-term (30-day) forecasts for the selected stock.

- **Visual Representation**: Offers plotted graphs to visualize actual vs predicted values, helping in better assessment.

## Requirements

- `yfinance`
- `pandas`
- `numpy`
- `sklearn`
- `matplotlib`

## Setup

1. **Clone/Download**:

   - Clone the repository or download the script to your local machine.

2. **Dependencies**:

   - Install all required libraries using pip:

   ```bash
   pip install yfinance pandas numpy sklearn matplotlib
   ```

## Usage

1. Run the script:
   ```bash
   python your_script_name.py
   ```

## How it Works

1. **Data Collection**: The script initiates by fetching the historical stock data of the specified ticker (default is "GOOGL") from `yfinance`.

2. **Feature Engineering**: It then computes essential features such as Moving Average and Momentum to the data, which aids in enhancing the prediction quality.

3. **Model Training & Prediction**: The historical data serves as input to train three distinct models - Random Forest, SVM, and KNN. Their predictions on a separated test set are then computed, compared, and evaluated for accuracy using Mean Squared Error.

4. **Forecasting**: Leveraging the trained models, the script generates both short-term (7-day) and medium-term (30-day) forecasts.

5. **Visualization**: The results, encompassing the actual versus predicted values for the test set and the forecasts, are visually represented using `matplotlib` for a more intuitive comparison and understanding.

## Notes

- **Customization**: The stock ticker and the date range can be easily modified in the main function, allowing for flexibility in which stock data you want to predict.

- **Prediction Limitation**: It's pivotal to understand that while machine learning models offer educated guesses based on historical data, stock market investments come with their inherent risks. Always prioritize conducting independent research or seek advice from financial experts before making investment choices.

- **Performance Metrics**: Each model's effectiveness is measured using the Mean Squared Error (MSE), offering a quantifiable metric to evaluate prediction accuracy.

- **Dependencies**: Ensure all required libraries are installed before execution. Missing libraries can lead to script failure.
