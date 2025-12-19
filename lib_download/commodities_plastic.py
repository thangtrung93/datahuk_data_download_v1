import toml
import streamlit as st
import requests
import toml
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time
from datetime import timedelta


api_base_vnbiz = st.secrets["api"]["api_base_vnbiz"]

l_commodities_plastic = ["cao_su_nhat_ban","pet_trung_quoc", "nhua_pvc_trung_quoc", "nhua_pp_trung_quoc",
                          "cao_su"]

def get_commodities_plastic():
    # get urls
    def get_url(l_commodities):
        d_url = {}
        for commodities in l_commodities:
            d_url[commodities] =  f'{api_base_vnbiz}vi-mo?key=hang_hoa&name={commodities}'
        return d_url

    d_url = get_url(l_commodities_plastic)

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
    def get_df(d_json, commodities):
        json_by_commodities= d_json[commodities].result()
        l_series = json_by_commodities['chart']['series']
        try:
            formatted_data = []
            for series in l_series:
                for data_x in series['data']:
                    formatted_data.append(
                        {
                            'Ngày': data_x[0],
                            f'{series['name']}_{series['unit']}': data_x[1],
                        }
                    )
            df = pd.DataFrame(formatted_data)
        
            df_group = df.groupby("Ngày").sum().reset_index()
            df_group["Ngày"] = pd.to_datetime(df_group["Ngày"], unit='ms')+timedelta(hours=7)
            df_group["Năm"] = df_group['Ngày'].dt.year
            df_group["Tháng"] = df_group["Ngày"].dt.month
            df_group = df_group[(df_group != 0).all(axis=1)]
            df_group.sort_values(["Ngày"], ascending=False, inplace=True)
            l_col_melt_id = ['Ngày', 'Năm', 'Tháng']
            l_col_melt_value = list(set(list(df_group.columns)) - set(l_col_melt_id))
            df_result = pd.melt(df_group, id_vars=l_col_melt_id, value_vars=l_col_melt_value,var_name='Phân loại', value_name='Giá trị')
            df_result =df_result[df_result['Giá trị'] > 0]
        except:
            df_result = pd.DataFrame()
        return df_result

    df_cao_su_nhat_ban=get_df(d_json_all,"cao_su_nhat_ban")
    df_pet_trung_quoc=get_df(d_json_all,"pet_trung_quoc")
    df_nhua_pvc_trung_quoc=get_df(d_json_all,"nhua_pvc_trung_quoc")
    df_nhua_pp_trung_quoc=get_df(d_json_all,"nhua_pp_trung_quoc")
    df_cao_su=get_df(d_json_all,"cao_su")
    
    return df_cao_su_nhat_ban, df_pet_trung_quoc, df_nhua_pvc_trung_quoc, df_nhua_pp_trung_quoc, df_cao_su
