import pandas as pd
from fbprophet import Prophet
from matplotlib import pyplot as plt
import matplotlib as mpl

def main():
    df = pd.read_csv('../ramhacks19/time_data.csv')

    m = Prophet()
    m.fit(df)

    future = m.make_future_dataframe(periods=4)
    # print(future.tail())

    forecast = m.predict(future)
    # print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

    mpl.use('WebAgg')
    fig1 = m.plot(forecast)

    # plt.show()
    # print(forecast.tail())
    plt.savefig('Forecast.png')
