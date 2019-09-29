
import requests
from bs4 import BeautifulSoup
import pandas as pd
import datetime
# import scraper as sc


# import numpy as np

def stock_scrape(symbol):
    url = "https://www.alphavantage.co/query?function=TIME_SERIES_MONTHLY&symbol=" + symbol + "&apikey=MV0AQTRW52L538UY"
    r = requests.get(url)
    data = r.text.split(":")
    data = str(data).split(',')
    # print(data)
    try:
        del data[:13]
    except IndexError:
        del data[:13]
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
    stock_data = pd.DataFrame(final_str, columns=['ds', 'Openprice', 'Highprice', 'Lowprice', 'y', 'Volume', 6, 7, 8, 9, 10])
    stock_data = stock_data.drop(columns=[6, 7, 8, 9, 10])
    stock_data['ds'] = stock_data['ds'].str.extract(r'([12]\d{3}-(0[1-9]|1[0-2])-(0[1-9]|[12]\d|3[01]))')
    stock_data['ds'] = pd.to_datetime(stock_data['ds'])
    categories = ['Openprice', 'Highprice', 'Lowprice', 'y', 'Volume']
    for item in categories:
        stock_data[item] = stock_data[item].str.extract(r'([-+]?\d*\.\d+|\d+)')
    stock_data['item_id'] = 1
    stock_data['Symbol'] = symbol
    stock_data['Monthvalue'] = stock_data['ds'].dt.month
    stock_data['Yearvalue'] = stock_data['ds'].dt.year
    return stock_data


def last_day_of_month(any_day):
    next_month = any_day.replace(day=28) + datetime.timedelta(days=4)  # this will never fail
    return next_month - datetime.timedelta(days=next_month.day)


def inflation_scrape(min_year=None):
    inflation_url = "https://inflationdata.com/Inflation/Inflation_Rate/Monthly_Inflation.aspx"
    page_response = requests.get(inflation_url, timeout=5)
    soup = BeautifulSoup(page_response.content, "html.parser")
    inflation_data = soup.find("table", attrs={'class': 'border'}).text
    inflation_data = inflation_data.strip().split()
    del inflation_data[:1117]
    del inflation_data[282::]
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
    # print(content)

    for year in range(1998, 2020):
        for index in content:
            if index == year:
                content.remove(index)
    del years[0]
    del content[0]
    inflation_data = pd.DataFrame(columns=['Inflation Rate'])
    # inflation_data['Date'] = pd.to_datetime(years)
    # inflation_data['Month'] = inflation_data['Date'].dt.month
    # inflation_data['Year'] = inflation_data['Date'].dt.year
    inflation_data['Inflation Rate'] = content

    # if min_year is not None:
    #     inflation_data = inflation_data[inflation_data['Year'] >= min_year]
    # print(inflation_data)
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


# def cpi_data_clean_up(length=None):
#     cpi_data = pd.read_csv("/Users/zabih/Documents/ramhacks19/data/cpi_data.csv")
#     cpi_data = cpi_data.sort_values(by='DATE', ascending=False)
#     cpi_data = pd.Series(cpi_data['CPALTT01USM661S'])
#     # cpi_data = cpi_data[:length-2]
#     print(cpi_data)
#     return list(cpi_data)


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
    time_series = stock_df[['ds', 'y']]
    time_series = time_series.drop(time_series.index[size+2::])
    stock_df = stock_df.drop(stock_df.index[size::])
    stock_df = stock_df.drop(stock_df.index[:1])
    # print(stock_df)
    in_scr = list(inflation_scrape())
    in_scr.reverse()
    del in_scr[54::]
    ur_rate = unemployment_rate_scrape(length=size-1)

    stock_df['Inflation Rate'] = in_scr
    stock_df['Unemployment Rate'] = ur_rate
    # stock_df['CPI'] = cpi_data_clean_up(length=size)
    stock_df = stock_df[['ds','y','item_id','Inflation Rate','Unemployment Rate']]
    return stock_df,time_series


def main(symbol=None):

    related_time_series = make_df(symbol)[0]
    time_data = make_df(symbol)[1]
    related_time_series.to_csv("training.csv", index=False)
    time_data.to_csv('time_data.csv',index=False)

main('amzn')