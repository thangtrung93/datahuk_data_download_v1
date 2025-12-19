import toml
import streamlit as st
import requests
import toml
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time
from datetime import timedelta


api_base_vnbiz = st.secrets["api"]["api_base_vnbiz"]

l_monetary = ["ctt","hd", "td", "dtnh", "dhtg", "lslnh", "lshd"]

def get_monetary():
    # get urls
    def get_url(l_monetary):
        d_url = {}
        for monetary in l_monetary:
            d_url[monetary] =  f'{api_base_vnbiz}vi-mo?name={monetary}'
        return d_url
    
    d_url = get_url(l_monetary)

    # function: get json
    def get_json(url):
        req = requests.get(url).json()
        time.sleep(2)
        return req

    # enable excecutor
    def get_json_all(d_url):
        executor = ThreadPoolExecutor(100)

        d_json = {key: [] for key in list(d_url.keys())}
        for key_x, url in d_url.items():
            try:        
                future = executor.submit(get_json, (url))
                d_json[key_x] = future
            except:
                pass
        return d_json
    
    d_json_all = get_json_all(d_url)

    # function: get df
    def get_df(d_json, monetary):
        json_by_monetary = d_json[monetary].result()
        l_serie = json_by_monetary['chart']['series']
        try:
            formatted_data = []
            for serie in l_serie:
                for data_x in serie['data']:
                    formatted_data.append(
                        {
                            'Ngày': data_x[0],
                            f'{serie['name']}_{serie['unit']}': data_x[1],
                        }
                    )
            df = pd.DataFrame(formatted_data)

            df_group = df.groupby("Ngày").sum().reset_index()
            df_group["Ngày"] = pd.to_datetime(df_group["Ngày"], unit='ms')+timedelta(hours=7)
            df_group["Năm"] = df_group['Ngày'].dt.year
            df_group["Tháng"] = df_group["Ngày"].dt.month
            df_group.sort_values(["Ngày"], ascending=False, inplace=True)
        except:
            df_group = pd.DataFrame()
        return df_group

    df_ctt = get_df(d_json_all, "ctt")
    df_hd = get_df(d_json_all, "hd")
    df_hd.rename(columns={"Tổng tiền gửi_tỷ VNĐ": "Tổng Huy động_tỷ VNĐ"}, inplace=True)

    df_td = get_df(d_json_all, "td")
    df_td.rename(columns={"Tổng tiền gửi_tỷ VNĐ": "Tổng Tín dụng_tỷ VNĐ"}, inplace=True)
    df_td_pre= df_td.copy()
    df_td_pre['Năm']+=1
    df_td_merge=df_td.merge(df_td_pre[['Năm', 'Tháng', 'Tổng Tín dụng_tỷ VNĐ']], on=["Năm","Tháng"], suffixes=('', '_pre'), how="left")
    df_td_merge["Tăng trưởng_%"]=round(100*(df_td_merge["Tổng Tín dụng_tỷ VNĐ"]/df_td_merge['Tổng Tín dụng_tỷ VNĐ_pre']-1),2)
    df_td_result = df_td_merge[["Ngày", "Tổng Tín dụng_tỷ VNĐ", "Tăng trưởng_%", "Năm", "Tháng"]].copy() 
    df_td_result.fillna(0, inplace=True)

    df_dtnh = get_df(d_json_all, "dtnh")
    df_dhtg = get_df(d_json_all, "dhtg")
    df_lslnh = get_df(d_json_all, "lslnh")
    df_lshd = get_df(d_json_all, "lshd")
    return df_ctt, df_hd, df_td_result, df_dtnh, df_dhtg, df_lslnh, df_lshd