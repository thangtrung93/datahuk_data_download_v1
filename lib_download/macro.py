import toml
import streamlit as st
import requests
import toml
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time
from datetime import timedelta

api_base_vnbiz = st.secrets["api"]["api_base_vnbiz"]

def get_macro():
    l_macro_type = ["gdp","gdpbinhquan", "cpi", "iip", "pmi", "hhdv", "vdtptxh", "vdtnsnn", "fdi","cctm", "cctt", "vt", "kqt", "ds", "tn", "ld", "tcns", "ncp"]
    
    # get urls
    def get_url(l_macro_type):
        d_url = {}
        for macro_type in l_macro_type:
            if macro_type == "gdp":
                d_url["gdp_q"] =  f'{api_base_vnbiz}vi-mo?type=q&name=gdp'
                d_url["gdp_y"] =  f'{api_base_vnbiz}vi-mo?type=y&name=gdp'
            elif macro_type == "ld":
                d_url["ld"] =  f'{api_base_vnbiz}vi-mo?type=q&name=ld'
            else:
                d_url[macro_type] =  f'{api_base_vnbiz}vi-mo?name={macro_type}'
        return d_url
    
    d_url_macro = get_url(l_macro_type)

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
    
    d_json_all = get_json_all(d_url_macro)

    # function: get df from json
    def get_df(d_json, macro_type, period_type):
        try:
            json_by_macro_type = d_json[macro_type].result()
            l_serie = json_by_macro_type['chart']['series']
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
            df_group["Ngày"] = pd.to_datetime(df_group["Ngày"], unit='ms') + timedelta(hours=7)
            df_group["Năm"] = df_group['Ngày'].dt.year
            if period_type == "quarter":
                df_group["Quý"] = df_group['Ngày'].dt.quarter
            elif period_type == "month":
                df_group["Tháng"] = df_group["Ngày"].dt.month
            else:
                pass
            df_group.sort_values(["Ngày"], ascending=False, inplace=True)
        except:
            df_group = pd.DataFrame()
        return df_group
    
    df_gdp_q =  get_df(d_json_all, 'gdp_q',"quarter")
    df_gdp_y =  get_df(d_json_all, 'gdp_y',"year")
    df_gdpbinhquan = get_df(d_json_all, 'gdpbinhquan', "year")
    df_cpi =  get_df(d_json_all, 'cpi',"month")
    df_iip =  get_df(d_json_all, 'iip',"month")
    df_pmi =  get_df(d_json_all, 'pmi',"month")
    df_hhdv =  get_df(d_json_all, 'hhdv',"month")
    df_vdtptxh =  get_df(d_json_all, 'vdtptxh',"quarter")
    df_vdtnsnn =  get_df(d_json_all, 'vdtnsnn',"month")
    df_fdi =  get_df(d_json_all, 'fdi',"month")
    df_cctm =  get_df(d_json_all, 'cctm',"month")
    df_cctt =  get_df(d_json_all, 'cctt',"quarter")
    df_vt =  get_df(d_json_all, 'vt',"month")
    df_kqt =  get_df(d_json_all, 'kqt',"month")
    df_ds =  get_df(d_json_all, 'ds',"year")
    df_tn =  get_df(d_json_all, 'tn',"quarter")
    df_ld =  get_df(d_json_all, 'ld',"quarter")
    df_tcns =  get_df(d_json_all, 'tcns',"quarter")
    df_ncp =  get_df(d_json_all, 'ncp',"year")
    return df_gdp_q, df_gdp_y, df_gdpbinhquan, df_cpi, df_iip, df_pmi, df_hhdv, df_vdtptxh, df_vdtnsnn, df_fdi, df_cctm, df_cctt, df_vt, df_kqt, df_ds, df_tn, df_ld, df_tcns, df_ncp

