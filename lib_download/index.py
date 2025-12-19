import streamlit as st
import requests
import toml
import pandas as pd
from datetime import datetime, timedelta

api_base_tcbs = st.secrets["api"]["api_base_tcbs"]
auth_tcbs = st.secrets["headers"]["auth_tcbs"]

def get_index_content(index_type, n_days):
    date_to = datetime.today()
    date_from = date_to -  timedelta(n_days)

    date_from_epoch = str(int(date_from.timestamp()))
    date_to_epoch = str(int(date_to.timestamp()))

    
    headers_tcbs = {"Authorization":auth_tcbs}
    url = f'{api_base_tcbs}stock-insight/v1/stock/bars-long-term?ticker={index_type}&type=index&resolution=D&from={date_from_epoch}&to={date_to_epoch}'
    req=requests.get(url, headers=headers_tcbs).json()
    df = pd.json_normalize(req["data"])
    df["tradingDate"] = df["tradingDate"].apply(lambda x: x.replace("T00:00:00.000Z",""))
    df.rename(columns={"tradingDate": "Ngày", "open": "Mở cửa", "high": "Cao nhất", "low": "Thấp nhất", "close": "Đóng cửa", "volume": "Khối lượng"}, inplace=True)
    df = df[["Ngày", "Mở cửa", "Cao nhất", "Thấp nhất", "Đóng cửa", "Khối lượng"]]
    df["Chỉ số"] = req["ticker"]
    df.sort_values(["Ngày"], ascending=False, inplace=True)
    return df

def get_index(n_days):
    try:
        df_vnindex = get_index_content("VNINDEX", n_days)
        df_hnxindex = get_index_content("HNXINDEX", n_days)
        df_upcomindex = get_index_content("UPCOM", n_days)
    except:
        df_vnindex, df_hnxindex, df_upcomindex = pd.DataFrame()
    return df_vnindex, df_hnxindex, df_upcomindex