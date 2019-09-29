import pandas as pd
from fbprophet import Prophet
from matplotlib import pyplot as plt

df = pd.read_csv('../reportgen/time_data.csv')

m = Prophet()
m.fit(df)

future = m.make_future_dataframe(periods=5)
# print(future.tail())

forecast = m.predict(future)
print(forecast[['ds', 'yhat', 'yhat_lower', 'yhat_upper']].tail())

fig1 = m.plot(forecast)

plt.savefig('Forecast.png')