import toml
import streamlit as st
import requests
import toml
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time

d_url = {
    "gdp_q":st.secrets["api"]["url_gdp_q"],
    "gdp_y":st.secrets["api"]["url_gdp_y"],
    "cpi_m":st.secrets["api"]["url_cpi_m"],
    "cpi_y":st.secrets["api"]["url_cpi_y"],
    "import_export_m":st.secrets["api"]["url_import_export_m"],
    "import_export_y":st.secrets["api"]["url_import_export_y"],
    "industry_index_m":st.secrets["api"]["url_industry_index_m"],
    "industry_index_y":st.secrets["api"]["url_industry_index_y"],
    "retail_index_m":st.secrets["api"]["url_retail_index_m"],
    "retail_index_y":st.secrets["api"]["url_retail_index_y"]}

d_l_col_rename = {
    "gdp_q":{"name_":"Chỉ tiêu", "report_time_":"Thời gian", "year_":"Năm", "quarter_":"Quý"},
    "gdp_y":{"name_":"Chỉ tiêu", "report_time_":"Thời gian", "year_":"Năm"},
    "cpi_m":{"report_time": "Thời gian", "year": "Năm", "group": "Phân loại", "name": "Chỉ tiêu", "unit": "Đơn vị", "value": "Giá trị", "month": "Tháng"},
    "cpi_y":{"report_time": "Thời gian", "year": "Năm", "group": "Phân loại", "name": "Chỉ tiêu", "unit": "Đơn vị", "value": "Giá trị"},
    "import_export_m":{"report_time": "Thời gian", "year": "Năm", "type": "XNK", "group": "Phân loại", "name": "Chỉ tiêu", "unit": "Đơn vị", "value": "Giá trị", "month": "Tháng"},
    "import_export_y":{"report_time": "Thời gian", "year": "Năm", "type": "XNK", "group": "Phân loại", "name": "Chỉ tiêu", "unit": "Đơn vị", "value": "Giá trị"},
    "industry_index_m":{"report_time": "Thời gian", "year": "Năm", "group": "Phân loại", "name": "Chỉ tiêu", "unit": "Đơn vị", "value": "Giá trị", "month": "Tháng"},
    "industry_index_y":{"report_time": "Thời gian", "year": "Năm", "group": "Phân loại", "name": "Chỉ tiêu", "unit": "Đơn vị", "value": "Giá trị"},
    "retail_index_m":{"report_time": "Thời gian", "year": "Năm", "group": "Phân loại", "name": "Chỉ tiêu", "unit": "Đơn vị", "value": "Giá trị", "month": "Tháng"},
    "retail_index_y":{"report_time": "Thời gian", "year": "Năm", "group": "Phân loại", "name": "Chỉ tiêu", "unit": "Đơn vị", "value": "Giá trị"}
}

def get_macro_detail():

    # function: get df from csv
    def get_df(macro_type):
        url = d_url[macro_type]
        df = pd.read_csv(url)
        try:
            if macro_type == "gdp_q":
                df = df[~df["name"].isin(["GDP theo giá cố định (2010)"])]
                df = df[~df["group"].isin(["Giá trị GDP (2010)"])]
                df_pivot = df.pivot_table(index=["name", "report_time", "year", "quarter"], columns=["group","unit"], values="value", aggfunc="median").reset_index()
                df_pivot.columns = ['_'.join(col) for col in df_pivot.columns]
                df_pivot.rename(columns=d_l_col_rename[macro_type], inplace=True)
                df_result = df_pivot[df_pivot["Quý"].isin(["Quý 1", "Quý 2", "Quý 3", "Quý 4"])].copy()
            elif macro_type == "gdp_y":
                df = df[df["name"].isin(["Công nghiệp","Dịch vụ","GDP bình quân","GDP bình quân (USD)","GNI theo giá hiện tại","Nông nghiệp","Tổng GDP"])]
                df_pivot = df.pivot_table(index=["name", "report_time", "year"], columns=["group","unit"], values="value", aggfunc="median").reset_index()
                df_pivot.columns = ['_'.join(col) for col in df_pivot.columns]
                df_pivot.rename(columns=d_l_col_rename[macro_type], inplace=True)
                df_pivot["Thu nhập bình quân_Nghìn đồng"]=(df_pivot["Thu nhập bình quân_Nghìn đồng"].astype(float))/pow(10,3)
                df_pivot.rename(columns={"Thu nhập bình quân_Nghìn đồng":"Thu nhập bình quân_Triệu đồng"}, inplace=True)
                df_result = df_pivot.copy()
            elif macro_type == "cpi_y":
                df.rename(columns=d_l_col_rename[macro_type], inplace=True)
                df["Chỉ tiêu"] = df["Chỉ tiêu"].replace("Tháng 12 năm báo cáo so với tháng 12 năm trước", "Cả năm")
                df_result = df.copy()
            elif macro_type == "import_export_y":
                df.rename(columns=d_l_col_rename[macro_type], inplace=True)
                df["Phân loại"] = df["Phân loại"].replace("", "Tổng Giá trị XNK")
                df_result = df.copy()
            else:
                df.rename(columns=d_l_col_rename[macro_type], inplace=True)
                df_result = df.copy()
            
        except:
            df_result = pd.DataFrame()
        return df_result
    
    df_gdp_q=get_df("gdp_q")
    df_gdp_y=get_df("gdp_y")
    df_cpi_m=get_df("cpi_m")
    df_cpi_y=get_df("cpi_y")
    df_import_export_m=get_df("import_export_m")
    df_import_export_y=get_df("import_export_y")
    df_industry_index_m=get_df("industry_index_m")
    df_industry_index_y=get_df("industry_index_y")
    df_retail_index_m=get_df("retail_index_m")
    df_retail_index_y=get_df("retail_index_y")

    return df_gdp_q,df_gdp_y,df_cpi_m,df_cpi_y,df_import_export_m,df_import_export_y,df_industry_index_m,df_industry_index_y,df_retail_index_m,df_retail_index_y

