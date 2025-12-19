import streamlit as st
import requests
import toml
import pandas as pd
from lib.setup_background import setup_header_sidebar
from views_data_download.data_stock import data_stock
from views_data_download.data_master_filter import data_master_filter
from views_data_download.data_index import data_index
from views_data_download.data_industry_q import data_financial_report_industry_q
from views_data_download.data_industry_y import data_financial_report_industry_y
from views_data_download.data_market import data_market
from views_data_download.data_macro import data_macro
from views_data_download.data_macro_detail import data_macro_detail
from views_data_download.data_monetary import data_monetary
from views_data_download.data_commodities_consumer import data_commodities_consumer
from views_data_download.data_commodities_chemicals import data_commodities_chemicals
from views_data_download.data_commodities_metal import data_commodities_metal
from views_data_download.data_commodities_energy import data_commodities_energy
from views_data_download.data_commodities_plastic import data_commodities_plastic
from views_data_download.data_commodities_materials import data_commodities_materials
# local_path = local_path()

setup_header_sidebar()
# Change CSS styles
with open("styles.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)




url_cus = st.secrets["api"]["url_cus"] # server version

# @st.cache_resource
def get_data_cus(url_cus):
    df = pd.read_csv(url_cus)
    return df

col1, col2  = st.columns([2,5])
with col1:
    
    email = st.text_input(label="Email đăng nhập")
    

if email:
    try:
        email_lower = email.strip().lower()
        df_cus = get_data_cus(url_cus)
        n_days = list(df_cus[df_cus["email_lower"]==email_lower]["n_days"])[0]
        customer_type = list(df_cus[df_cus["email_lower"]==email_lower]["note"])[0]

        if n_days <= 0:
            st.markdown(f"Vui lòng gia hạn gói dịch vụ tại: " + f'<a href="https://www.facebook.com/datahuk68"> @datahuk68</a>',unsafe_allow_html=True)
            st.divider()    
        elif n_days > 0:
            st.text(body=f"Hạn sử dụng: {str(n_days)} ngày")
            if customer_type == "test":
                st.markdown("Khách hàng: test")
            elif customer_type == "customer":
                st.markdown("Khách hàng: ✅")
            st.divider()    
            l_options_download_type = ["1_Dữ liệu cổ phiếu", "1_Dữ liệu cổ phiếu_Toàn bộ mã_Bộ lọc",
                                        "2.1_Dữ liệu VNINDEX", "2.2_Dữ liệu Ngành_Báo cáo tài chính",
                                        "2_Dữ liệu Thị trường",
                                        "3_Dữ liệu Vĩ mô",
                                        "3_Dữ liệu Vĩ mô_Chi tiết",
                                        "4_Dữ liệu Lãi suất tiền tệ",
                                        "5_Dữ liệu Hàng hóa_Hàng tiêu dùng",
                                        "5_Dữ liệu Hàng hóa_Hóa chất", "5_Dữ liệu Hàng hóa_Kim loại",
                                        "5_Dữ liệu Hàng hóa_Năng lượng",
                                        "5_Dữ liệu Hàng hóa_Nhựa và cao su",
                                        "5_Dữ liệu Hàng hóa_Vật liệu xây dựng"
                                        ]
            sl_download_typpe = st.selectbox(label="Chọn dữ liệu muốn tải", options=l_options_download_type)

            if sl_download_typpe == "1_Dữ liệu cổ phiếu":
                data_stock(customer_type)
            if sl_download_typpe == "1_Dữ liệu cổ phiếu_Toàn bộ mã_Bộ lọc":
                data_master_filter(customer_type)  
            elif sl_download_typpe == "2.1_Dữ liệu VNINDEX":
                data_index(customer_type)
            elif sl_download_typpe == "2.2_Dữ liệu Ngành_Báo cáo tài chính":
                sl_period_type = st.selectbox(label="Chọn Thời gian báo cáo", options=["Quý", "Năm"])
                if sl_period_type == "Quý":
                    data_financial_report_industry_q(customer_type)
                elif sl_period_type == "Năm":
                    data_financial_report_industry_y(customer_type)
            elif sl_download_typpe == "2_Dữ liệu Thị trường":
                data_market(customer_type)
            elif sl_download_typpe == "3_Dữ liệu Vĩ mô":
                data_macro(customer_type)
            elif sl_download_typpe == "3_Dữ liệu Vĩ mô_Chi tiết":
                data_macro_detail(customer_type)
            elif sl_download_typpe == "4_Dữ liệu Lãi suất tiền tệ":
                data_monetary(customer_type)
            elif sl_download_typpe == "5_Dữ liệu Hàng hóa_Hàng tiêu dùng":
                data_commodities_consumer(customer_type)
            elif sl_download_typpe == "5_Dữ liệu Hàng hóa_Hóa chất":
                data_commodities_chemicals(customer_type)
            elif sl_download_typpe == "5_Dữ liệu Hàng hóa_Kim loại":
                data_commodities_metal(customer_type)
            elif sl_download_typpe == "5_Dữ liệu Hàng hóa_Năng lượng":
                data_commodities_energy(customer_type)
            elif sl_download_typpe == "5_Dữ liệu Hàng hóa_Nhựa và cao su":
                data_commodities_plastic(customer_type)
            elif sl_download_typpe == "5_Dữ liệu Hàng hóa_Vật liệu xây dựng":
                data_commodities_materials(customer_type)
    except:
        st.markdown("Vui lòng kiểm tra lại email!")

