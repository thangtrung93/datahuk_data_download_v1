import streamlit as st
import requests
import pandas as pd
import io
from lib_download.financial_report_industry_q import get_financial_report_industry_q
from lib_download.financial_report_industry_q_banking import get_financial_report_industry_q_banking
# from lib_download.financial_report_industry_y import get_financial_report_industry_y

def data_financial_report_industry_q(customer_type):
    btn_refresh = st.button(label="Cập nhật dữ liệu")
    if btn_refresh:
        df_q_bs, df_q_ic, df_q_cf, df_q_ratio = get_financial_report_industry_q()
        # df_y_bs, df_y_ic, df_y_cf, df_y_ratio = get_financial_report_industry_y()
        df_q_bs_banking, df_q_ic_banking, df_q_ratio_banking = get_financial_report_industry_q_banking()
        # df_y_bs_banking, df_y_ic_banking, df_y_ratio_banking 

        st.warning("Cập nhật xong!")
        
        if customer_type == "customer":
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_q_bs.to_excel(writer, sheet_name='Quý_CĐKT_Ngành', index=False)
                df_q_ic.to_excel(writer, sheet_name='Quý_KQKD_Ngành', index=False)
                df_q_cf.to_excel(writer, sheet_name='Quý_LCTT_Ngành', index=False)
                df_q_ratio.to_excel(writer, sheet_name='Quý_Chỉ số_Ngành', index=False)

                df_q_bs_banking.to_excel(writer, sheet_name='Quý_CĐKT_Ngân hàng', index=False)
                df_q_ic_banking.to_excel(writer, sheet_name='Quý_KQKD_Ngân hàng', index=False)
                df_q_ratio_banking.to_excel(writer, sheet_name='Quý_Chỉ số_Ngân hàng', index=False)

                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Ngành_Báo cáo tài chính_Quý",
                    data=buffer,
                    file_name="2.2_Dữ liệu Ngành_Báo cáo tài chính_Quý.xlsx",
                    mime="application/vnd.ms-excel"
                )
        else:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_q_bs.head(25).to_excel(writer, sheet_name='Quý_CĐKT_Ngành', index=False)
                df_q_ic.head(25).to_excel(writer, sheet_name='Quý_KQKD_Ngành', index=False)
                df_q_cf.head(25).to_excel(writer, sheet_name='Quý_LCTT_Ngành', index=False)
                df_q_ratio.head(25).to_excel(writer, sheet_name='Quý_Chỉ số_Ngành', index=False)

                df_q_bs_banking.head(25).to_excel(writer, sheet_name='Quý_CĐKT_Ngân hàng', index=False)
                df_q_ic_banking.head(25).to_excel(writer, sheet_name='Quý_KQKD_Ngân hàng', index=False)
                df_q_ratio_banking.head(25).to_excel(writer, sheet_name='Quý_Chỉ số_Ngân hàng', index=False)

                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Ngành_Báo cáo tài chính_Quý",
                    data=buffer,
                    file_name="2.2_Dữ liệu Ngành_Báo cáo tài chính_Quý.xlsx",
                    mime="application/vnd.ms-excel"
                )