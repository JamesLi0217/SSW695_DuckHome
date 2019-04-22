import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from sklearn.preprocessing import MinMaxScaler
from keras.layers import LSTM
from keras.models import Sequential
from keras.layers import Dense
import random


def get_data(path):
    df = pd.read_csv(path)
    data = df.set_index('date')
    data.index = pd.DatetimeIndex(data.index)
    return data


# frame a sequence as a supervised learning problem
def timeseries_to_supervised(data, lag=1):
    df = pd.DataFrame(data)
    columns = [df.shift(i) for i in range(1, lag + 1)]
    columns.append(df)
    df = pd.concat(columns, axis=1)
    df.fillna(0, inplace=True)
    return df


# Create a differenced series
def difference(dataset, interval=1):
    diff = list()
    for i in range(interval, len(dataset)):
        value = dataset[i] - dataset[i - interval]
        diff.append(value)
    return pd.Series(diff)


# invert differenced value
def inverse_difference(history, yhat, interval=1):
    return yhat + history[-interval]


# inverse scaling for a forecasted value
def invert_scale(scaler, X, value):
    new_row = [x for x in X] + [value]
    array = np.array(new_row)
    array = array.reshape(1, len(array))
    inverted = scaler.inverse_transform(array)
    return inverted[0, -1]


# fit an LSTM network to training data
def fit_lstm(train, batch_size, nb_epoch, neurons):
    X, y = train[:, 0:-1], train[:, -1]
    X = X.reshape(X.shape[0], 1, X.shape[1])
    model = Sequential()
    model.add(LSTM(neurons, batch_input_shape=(batch_size, X.shape[1], X.shape[2]), stateful=True))
    model.add(Dense(1))
    model.compile(loss='mean_squared_error', optimizer='adam')
    for i in range(nb_epoch):
        model.reset_states()
    return model


# make a one-step forecast
def forecast_lstm(model, batch_size, X):
    X = X.reshape(1, 1, len(X))
    yhat = model.predict(X, batch_size=batch_size)
    return yhat[0, 0]


# Build model
def build_model(data):
    # transform data to be stationary
    raw_values = data.values
    diff_values = difference(raw_values, 1)

    # transform data to be supervised learning
    supervised = timeseries_to_supervised(diff_values, 1)
    supervised_values = supervised.values

    # transform the scale of the data
    # fit scaler
    scaler = MinMaxScaler(feature_range=(-1, 1))
    scaler = scaler.fit(supervised_values)
    # transform data
    data_scaled = scaler.transform(supervised_values)

    # fit the model
    out_lstm_model = fit_lstm(data_scaled, 1, 3000, 4)

    return out_lstm_model, data_scaled, scaler


# Make prediction
def prediction(model, data_scaled, scaler, data, step):
    raw_values = data.values
    result = list()
    for i in range(step):
        # make one-step forecast
        X, y = data_scaled[i, 0:-1], data_scaled[i, -1]
        yhat = forecast_lstm(model, 1, X)
        # invert scaling
        yhat = invert_scale(scaler, X, yhat)
        # invert differencing
        yhat = inverse_difference(raw_values, yhat, step + 1 - i)
        # store forecast
        result.append(yhat[0])

    pred_long = np.array(result)
    d = np.ones(step) * 256
    pred_long = pred_long - d
    time_long = pd.date_range('20190201', periods=step, freq='MS')
    pred_long_df = pd.DataFrame(np.round(pred_long, 1), index=time_long, columns=['price'])
    result_long = pd.concat([data, pred_long_df], axis=0)
    result_long = result_long.reset_index()

    return result_long


def draw(result_long, city):
    x2 = result_long['index'].tail(24)
    y2 = result_long['price'].tail(24)

    fig = plt.figure(figsize=(20, 10))
    plt.plot(x2, y2, linewidth=3, color='blue', marker='o', markerfacecolor='red', markersize=8)

    plt.title('{} Rental Price Prediction by LSTM'.format(city), fontsize=30)
    plt.ylabel('Average Rental Price ($/month)', fontsize=18)
    plt.tick_params(labelsize=12)
    plt.xticks(rotation=45)
    for i, j in zip(x2, y2):
        plt.text(i, j + 3, j, ha='center', va='bottom', fontsize=12)
    plt.legend()

    return fig


def main():
    step = 26
    city = random.choice(['Hoboken', 'Jersey City', 'Union City'])
    path_dic = {'Hoboken': '../pre_data/Hoboken_price.csv',
                'Jersey City': '../pre_data/JerseyCity_price.csv',
                'Union City': '../pre_data/UnionCity_price.csv'}

    path = path_dic[city]
    data = get_data(path)
    out_lstm_model, data_scaled, scaler = build_model(data)
    result_long = prediction(out_lstm_model, data_scaled, scaler, data, step)
    fig = draw(result_long, city)
    fig.show()


if __name__ == '__main__':
    main()
