import streamlit as st
import requests
import pandas as pd
import io
from lib_download.financial_report import get_financial_ratio, get_financial_report
from lib_download.overview import get_overview
from lib_download.casa import get_casa
from datetime import date

url_cus = st.secrets["api"]["url_cus"]
api_industry = st.secrets["api"]["api_industry"]

def get_file_name_financial_report(industry_type):
    
    # d_industry_type = {"Banks":"Ngân hàng", "Financial Services":"Chứng khoán", "Insurance":"Bảo hiểm"}
    if industry_type in ["Ngân hàng", "Bảo hiểm"]:
        return f"1_Dữ liệu cổ phiếu_{industry_type}.xlsx"
    elif industry_type == "Dịch vụ tài chính":
        return "1_Dữ liệu cổ phiếu_Chứng khoán.xlsx"
    else:
        return "1_Dữ liệu cổ phiếu.xlsx"

def data_stock(customer_type):
    col1, col2, col3 = st.columns([5,5,5])
    with col1:
        ticker = st.text_input(label="Mã").upper()
    # with col2:
    #     year_from = st.number_input(label="Từ năm", min_value=2008)
    # with col3: 
    #     year_to = st.number_input(label="Đến năm", min_value=2008, value=date.today().year)
    btn_refresh = st.button(label="Cập nhật dữ liệu")
    if btn_refresh:
        df_overview, industry_type, df_dividend, df_shareholders, df_sub_companies, df_audit_firm, df_evaluation_history, df_stock_indicator, df_stock_foreign_volume = get_overview(ticker)
        
        df_q_bs, df_q_ic, df_q_cf, df_y_bs, df_y_ic, df_y_cf = get_financial_report(ticker)
        df_q_ratio, df_y_ratio = get_financial_ratio(ticker)
        
        file_name = get_file_name_financial_report(industry_type)
        if industry_type == "Ngân hàng":
            df_q_casa, df_y_casa = get_casa(ticker)

        st.warning("Cập nhật xong!")
        
        if customer_type == "customer":
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_overview.to_excel(writer, sheet_name='Tổng quan', index=False)
                df_dividend.to_excel(writer, sheet_name='Lịch sử cổ tức', index=False)
                df_shareholders.to_excel(writer, sheet_name='Danh sách cổ đông', index=False)
                df_sub_companies.to_excel(writer, sheet_name='Danh sách công ty con', index=False)
                df_audit_firm.to_excel(writer, sheet_name='Danh sách công ty kiểm toán', index=False)
                
                df_y_bs.to_excel(writer, sheet_name='Năm_CĐKT', index=False)
                df_y_ic.to_excel(writer, sheet_name='Năm_KQKD', index=False)
                df_y_cf.to_excel(writer, sheet_name='Năm_LCTT', index=False)
                df_y_ratio.to_excel(writer, sheet_name='Năm_Chỉ số tài chính', index=False)
                df_q_bs.to_excel(writer, sheet_name='Quý_CĐKT', index=False)
                df_q_ic.to_excel(writer, sheet_name='Quý_KQKD', index=False)
                df_q_cf.to_excel(writer, sheet_name='Quý_LCTT', index=False)
                df_q_ratio.to_excel(writer, sheet_name="Quý_Chỉ số tài chính", index=False)
                
                if industry_type == "Ngân hàng":
                    df_y_casa.to_excel(writer, sheet_name='Năm_Tỷ lệ CASA', index=False)
                    df_q_casa.to_excel(writer, sheet_name='Quý_Tỷ lệ CASA', index=False)
                    
                df_evaluation_history.to_excel(writer, sheet_name='Chỉ số PE_PB', index=False)
                df_stock_indicator.to_excel(writer, sheet_name='Chỉ số kĩ thuật', index=False)
                df_stock_foreign_volume.to_excel(writer, sheet_name='KLGD nước ngoài', index=False)
                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Cổ phiếu",
                    data=buffer,
                    file_name=file_name,
                    mime="application/vnd.ms-excel"
                )
        else:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_overview.head(25).to_excel(writer, sheet_name='Tổng quan', index=False)
                df_dividend.head(25).to_excel(writer, sheet_name='Lịch sử cổ tức', index=False)
                df_shareholders.head(25).to_excel(writer, sheet_name='Danh sách cổ đông', index=False)
                df_sub_companies.head(25).to_excel(writer, sheet_name='Danh sách công ty con', index=False)
                df_audit_firm.head(25).to_excel(writer, sheet_name='Danh sách công ty kiểm toán', index=False)


                df_y_bs.head(25).to_excel(writer, sheet_name='Năm_CĐKT', index=False)
                df_y_ic.head(25).to_excel(writer, sheet_name='Năm_KQKD', index=False)
                df_y_cf.head(25).to_excel(writer, sheet_name='Năm_LCTT', index=False)
                df_y_ratio.head(25).to_excel(writer, sheet_name='Năm_Chỉ số tài chính', index=False)
                df_q_bs.head(25).to_excel(writer, sheet_name='Quý_CĐKT', index=False)
                df_q_ic.head(25).to_excel(writer, sheet_name='Quý_KQKD', index=False)
                df_q_cf.head(25).to_excel(writer, sheet_name='Quý_LCTT', index=False)
                df_q_ratio.head(25).to_excel(writer, sheet_name="Quý_Chỉ số tài chính", index=False)
                
                if industry_type == "Ngân hàng":
                    df_y_casa.head(25).to_excel(writer, sheet_name='Năm_Tỷ lệ CASA', index=False)
                    df_q_casa.head(25).to_excel(writer, sheet_name='Quý_Tỷ lệ CASA', index=False)
                    
                df_evaluation_history.head(25).to_excel(writer, sheet_name='Chỉ số PE_PB', index=False)
                df_stock_indicator.head(25).to_excel(writer, sheet_name='Chỉ số kĩ thuật', index=False)
                df_stock_foreign_volume.head(25).to_excel(writer, sheet_name='KLGD nước ngoài', index=False)
                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Cổ phiếu",
                    data=buffer,
                    file_name=file_name,
                    mime="application/vnd.ms-excel"
                )