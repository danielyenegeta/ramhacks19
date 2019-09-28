
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime


# import numpy as np

def stock_scrape(symbol):
    """
    scrapes a website that has all stock prices for every stock symbol there is to get the price index for stock symbol
    requested

    :param symbol: ticker symbol for the stock
    :return: data frame that has information on the price indexes for the symbol passed in
    """

    # url that has the information on the symbol. scrape the entire site as is.
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=" + symbol + "&apikey=MV0AQTRW52L538UY"
    r = requests.get(url)

    # split on ":" then split on ','. This gives us a list of the data separated enough for further clean up
    data = r.text.split(":")
    data = str(data).split(',')

    # deletes the meta data that is present
    try:
        del data[:13]
    except IndexError:
        del data[:13]

    # Below code groups the price index per month and adds it to a another list
    # This code is confusing to understand. If you cannot understand what is happening here, move on because it is not
    # crucial to understand.
    temp_str = []
    final_str = []
    counter = 0
    while len(data) > 5:
        if counter % 11 != 0 or counter == 0:
            temp_str.append(data[counter])
            counter += 1
            del data[0]
        else:
            counter = 0
            final_str.append(temp_str)
            temp_str = []
    final_str.append(temp_str)

    # Create the data frame for the prices
    # The number columns are there to match the length of the lists that are generated from the while loop above.
    # They are dropped once the data from the lists is passed in.
    stock_data = pd.DataFrame(final_str, columns=['Date', 'Open', 'High', 'Low', 'Close', 'Volume', 6, 7, 8, 9, 10])
    stock_data = stock_data.drop(columns=[6, 7, 8, 9, 10])

    # Clean up the messyness of the data frame by extracting just the data in the column
    stock_data['Date'] = stock_data['Date'].str.extract(r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))')

    # Convert the date column to a date time variable from a string
    stock_data['Date'] = pd.to_datetime(stock_data['Date'])

    # Grab just the numbers from the data and ignore all extra pieces
    categories = ['Open', 'High', 'Low', 'Close', 'Volume']
    for item in categories:
        stock_data[item] = stock_data[item].str.extract(r'([-+]?\d*\.\d+|\d+)')

    # Add a column that has the symbol
    stock_data['Symbol'] = symbol

    # Create columns with the months and years for each entry
    stock_data['Month'] = stock_data['Date'].dt.month
    stock_data['Year'] = stock_data['Date'].dt.year

    return stock_data


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)


def inflation_scrape(min_year=None):
    """
    Scrapes a website that has inflation data.
    :param min_year:
    :return: column that has monthly inflation data
    """
    inflation_url = "https://inflationdata.com/Inflation/Inflation_Rate/Monthly_Inflation.aspx"
    page_response = requests.get(inflation_url, timeout=5)
    soup = BeautifulSoup(page_response.content, "html.parser")
    inflation_data = soup.find("table", attrs={'class': 'border'}).text
    inflation_data = inflation_data.strip().split()
    del inflation_data[:1117]
    del inflation_data[279::]
    years = []
    for year in range(1998, 2020):
        for month in range(1, 13):
            years.append(datetime.date(year, month, 1))

    del years[257::]
    content_series = pd.Series(inflation_data)
    strip_syms = ['(', ')', '%']
    for sym in strip_syms:
        content_series = content_series.str.strip(sym)
    content_series = pd.to_numeric(content_series)

    content = list(content_series)

    for year in range(1998, 2020):
        for index in content:
            if index == year:
                content.remove(index)

    del years[0]
    del content[0]
    inflation_data = pd.DataFrame(columns=['Date', 'Inflation Rate'])
    inflation_data['Date'] = pd.to_datetime(years)
    inflation_data['Month'] = inflation_data['Date'].dt.month
    inflation_data['Year'] = inflation_data['Date'].dt.year
    inflation_data['Inflation Rate'] = content
    if min_year is not None:
        inflation_data = inflation_data[inflation_data['Year'] >= min_year]
    return inflation_data['Inflation Rate']


def unemployment_rate_scrape(length=None):
    """
    Scrapes a website to get unemployment rate data
    :return: unemployment data column
    """
    unemploy_url = "https://www.multpl.com/unemployment/table/by-month"
    page_response = requests.get(unemploy_url, timeout=5)
    soup = BeautifulSoup(page_response.content, "html.parser")
    unemployment_data = soup.find("table", attrs={'id': 'datatable'}).text
    unemployment_data = unemployment_data.strip().split()

    unemployment_list = []

    for i in range(len(unemployment_data)):
        if '%' in unemployment_data[i]:
            unemployment_list.append(unemployment_data[i])
    unemployment_list = pd.Series(unemployment_list)

    unemployment_list = unemployment_list.str.strip('%')
    unemployment_list = unemployment_list[:length]

    return unemployment_list


def cpi_data_clean_up(length=None):
    cpi_data = pd.read_csv("/Users/zabih/Documents/ramhacks19/data/cpi_data.csv")
    cpi_data = cpi_data.sort_values(by='DATE', ascending=False)
    cpi_data = pd.Series(cpi_data['CPALTT01USM661S'])
    cpi_data = cpi_data[:length-2]
    return list(cpi_data)


def make_df(symbol):
    # pass in the data to the clean up methods
    stock_df = stock_scrape(symbol)
    # print(stock_df)
    len_of_dataframe = len(stock_df)
    size = float('inf')
    if len_of_dataframe > 55:
        size = 55
    else:
        size = len_of_dataframe
    stock_df = stock_df.drop(stock_df.index[size::])
    stock_df = stock_df.drop(stock_df.index[:2])

    in_scr = list(inflation_scrape(min_year=stock_df['Year'].min()))
    ur_rate = unemployment_rate_scrape(length=size)

    stock_df['Inflation Rate'] = in_scr[::-1]
    stock_df['Unemployment Rate'] = ur_rate
    stock_df['CPI'] = cpi_data_clean_up(length=size)
    return stock_df


def main(symbol=None):
    return make_df(symbol)