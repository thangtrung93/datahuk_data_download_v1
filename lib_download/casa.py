import streamlit as st
import pandas as pd
import requests

api_base_dnse = st.secrets["api"]["api_base_dnse"]

def get_casa(ticker):
    def get_casa_content(ticker, period_type):
        url = f'{api_base_dnse}business-result?symbol={ticker}&code=CASA_RATIO&cycleType={period_type}&cycleNumber=10'
        req = requests.get(url).json()
        df = pd.DataFrame(req["data"][0]["y"], columns=["Tỷ lệ Casa"])
        df["Mã"] = ticker
        df["Năm"] = list(map(lambda x: x[-4:], req["x"]))
        if period_type == "quy":
            df["Quý"] = list(map(lambda x: x[:2], req["x"]))
            df = df[["Mã", "Năm", "Quý", "Tỷ lệ Casa"]]
        else:
            df = df[["Mã", "Năm", "Tỷ lệ Casa"]]
        df["Năm"] = df["Năm"].astype(int)
        return df
    try:
        df_q_casa =  get_casa_content(ticker, "quy")
        df_y_casa =  get_casa_content(ticker, "nam")
    except:
        df_q_casa,df_y_casa  = pd.DataFrame()
    return df_q_casa,df_y_casa