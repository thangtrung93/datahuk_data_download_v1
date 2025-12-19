import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta
from concurrent.futures import ThreadPoolExecutor
import time

d_industry_code = {"5300":"Bán lẻ", "8500":"Bảo hiểm", "8600":"Bất động sản",
                   "9500":"Công nghệ Thông tin", "0500":"Dầu khí",
                   "8700":"Dịch vụ tài chính", "7500":"Điện, nước & xăng dầu khí đốt",
                   "5700":"Du lịch và Giải trí", "2700":"Hàng & Dịch vụ Công nghiệp",
                   "3700":"Hàng cá nhân & Gia dụng", "1300":"Hóa chất", 
                   "3300":"Ô tô và phụ tùng", "8300": "Ngân hàng",
                   "1700":"Tài nguyên Cơ bản", "3500":"Thực phẩm và đồ uống","5500":"Truyền thông",
                   "6500":"Viễn thông", "2300":"Xây dựng và Vật liệu", "4500":"Y tế"}

api_base_tcbs = st.secrets["api"]["api_base_tcbs"]
auth_tcbs = st.secrets["headers"]["auth_tcbs"]

def get_market_index():
    def get_url(index_type, d_industry_code):
        l_url = [f'{api_base_tcbs}stock-insight/v1/intraday/{index_type}?exchange=ALL&industry={industry_code}&type=1M' for industry_code in list(d_industry_code.keys())]
        return l_url
    l_url_flow_breadth = get_url("flow-breadth", d_industry_code)
    l_url_flow_market_foreign_value = get_url("flow-market-foreign-val", d_industry_code)
    l_url_flow_market_value_percent_trading = get_url("flow-market-value-percent-trading", d_industry_code)
    l_url_flow_industry_index = get_url("flow-industry-index", d_industry_code)
    l_url_flow_supply_demand = get_url("flow-supply-demand", d_industry_code)

    d_url_flow_breadth = {"flow_breadth":l_url_flow_breadth}
    d_url_flow_market_foreign_value = {"flow_market_foreign_val":l_url_flow_market_foreign_value}
    d_url_flow_market_value_percent_trading = {"flow_market_value_percent_trading":l_url_flow_market_value_percent_trading}
    d_url_flow_industry_index = {"flow_industry_index":l_url_flow_industry_index}
    d_url_flow_supply_demand = {"flow_supply_demand":l_url_flow_supply_demand} 

    # function: get json
    def get_json(url, headers):
        req = requests.get(url, headers=headers).json()
        time.sleep(2)
        return req

    # enable excecutor
    def get_json_all(d_url, headers):
        executor = ThreadPoolExecutor(100)

        d_json = {key: [] for key in list(d_url.keys())}
        for key_x, l_url in d_url.items():
            futures = []
            for url in l_url:
                try:        
                    future = executor.submit(get_json, url, headers)
                    futures.append(future)
                except:
                    pass
            d_json[key_x] = futures
        return d_json

    headers_tcbs = {"Authorization":auth_tcbs}
    d_json_flow_breadth = get_json_all(d_url_flow_breadth, headers_tcbs)
    d_json_flow_market_foreign_value = get_json_all(d_url_flow_market_foreign_value, headers_tcbs)
    d_json_flow_market_value_percent_trading = get_json_all(d_url_flow_market_value_percent_trading, headers_tcbs)
    d_json_flow_industry_index = get_json_all(d_url_flow_industry_index, headers_tcbs)
    d_json_flow_supply_demand = get_json_all(d_url_flow_supply_demand, headers_tcbs)
    # st.write(d_json_flow_market_value_percent_trading["flow_market_value_percent_trading"][0].result())



    # function: get df from json
    def get_df(d_json, report_type, target_body, d_industry_code, d_col, l_col):
        # try:
        l_result = [i.result() for i in d_json[report_type]]
        result_flat = []
        for sublist in l_result:
            if report_type == "flow_market_value_percent_trading":
                sublist_body = sublist["body"]
            else:
                sublist_body = sublist["body"][target_body]
            for i in sublist_body:
                i["industry"]=sublist["industry"]
                result_flat.append(i)
        
        df_result = pd.json_normalize(result_flat)
        df_result["industry"] = df_result["industry"].apply(lambda x: d_industry_code[x])

        # convert unit
        if report_type == "flow_market_foreign_val":
            df_result[["av", "v"]] = df_result[["av", "v"]].astype(float)
            df_result[["av", "v"]] = df_result[["av", "v"]].apply(lambda x: round(x/pow(10,9),0))
        elif report_type == "flow_market_value_percent_trading":
            df_result[["accValue", "marketCap"]] = df_result[["accValue", "marketCap"]].astype(float)
            df_result[["accValue", "marketCap"]] = df_result[["accValue", "marketCap"]].apply(lambda x: round(x/pow(10,9),0))

        df_result.rename(columns=d_col, inplace=True)
        df_result = df_result[l_col]
        df_result["Ngày"] =  df_result["Ngày"].apply(lambda x: datetime.strptime(x[0:8], "%d/%m/%y"))

        # except:
        #     df_result = pd.DataFrame()
        return df_result
    
    d_col_flow_breadth = {"t": "Ngày", "a": "Số mã tăng giá", "d": "Số mã giảm giá", "s": "Số mã đứng giá", "industry":"Ngành"}
    l_col_flow_breadth = ["Ngành", "Ngày", "Số mã tăng giá", "Số mã giảm giá", "Số mã đứng giá"]

    d_col_flow_market_foreign_value = {"t":"Ngày", "v":"GTGD Nước ngoài ròng_tỷ đồng", "av": "GTGD NN ròng tích lũy_tỷ đồng",  "industry":"Ngành"}
    l_col_flow_market_foreign_value= ["Ngành", "Ngày", "GTGD NN ròng tích lũy_tỷ đồng", "GTGD Nước ngoài ròng_tỷ đồng"]

    d_col_flow_market_value_trading = {"industry":"Ngành","seqTime": "Ngày", "accValue": "Giá trị giao dịch_ngành", "marketCap": "Vốn hóa_ngành", "marketCapPercent": "Vốn hóa_%", "accValuePercent":"Giá trị giao dịch_ngành_%"}
    l_col_flow_market_value_trading = ["Ngành", "Ngày", "Giá trị giao dịch_ngành", "Vốn hóa_ngành", "Vốn hóa_%", "Giá trị giao dịch_ngành_%"]

    d_col_flow_industry_index = {"industry":"Ngành","s":"Ngày", "v": "KLGD", "i": "Chỉ số"}
    l_col_flow_industry_index = ["Ngành", "Ngày", "KLGD", "Chỉ số"]

    d_col_flow_supply_demand = {"industry":"Ngành","t": "Ngày", "bms": "KL_Mua chủ động", "sms": "KL_Bán chủ động", "bup":"Tỷ lệ_Mua chủ động", "sdp":"Tỷ lệ_Bán chủ động", "bsr":"Tỷ lệ M/B chủ động"}
    l_col_flow_supply_demand= ["Ngành", "Ngày", "KL_Mua chủ động", "Tỷ lệ_Mua chủ động", "KL_Bán chủ động", "Tỷ lệ_Bán chủ động", "Tỷ lệ M/B chủ động"]

    # get all df
    df_flow_breadth = get_df(d_json_flow_breadth, "flow_breadth", "b",
                              d_industry_code, d_col_flow_breadth, l_col_flow_breadth)
    df_flow_market_foreign_value = get_df(d_json_flow_market_foreign_value, "flow_market_foreign_val",
                                           "data", d_industry_code, d_col_flow_market_foreign_value, l_col_flow_market_foreign_value)
    df_flow_market_value_trading = get_df(d_json_flow_market_value_percent_trading, "flow_market_value_percent_trading", "", d_industry_code, d_col_flow_market_value_trading, l_col_flow_market_value_trading)
    df_flow_industry_index = get_df(d_json_flow_industry_index, "flow_industry_index", "data", d_industry_code, d_col_flow_industry_index, l_col_flow_industry_index)
    df_flow_supply_demand = get_df(d_json_flow_supply_demand, "flow_supply_demand","data", d_industry_code, d_col_flow_supply_demand, l_col_flow_supply_demand)

    return df_flow_breadth, df_flow_market_foreign_value, df_flow_market_value_trading, df_flow_industry_index, df_flow_supply_demand