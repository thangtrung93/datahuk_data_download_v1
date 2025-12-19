import streamlit as st
import requests
import pandas as pd
import io
from lib_download.monetary import get_monetary


def data_monetary(customer_type):

    btn_refresh = st.button(label="Cập nhật dữ liệu")
    if btn_refresh:
        df_ctt, df_hd, df_td, df_dtnh, df_dhtg, df_lslnh, df_lshd = get_monetary()

        st.warning("Cập nhật xong!")
        
        if customer_type == "customer":
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_ctt.to_excel(writer, sheet_name='Cung tiền M2', index=False)
                df_hd.to_excel(writer, sheet_name='Huy động', index=False)
                df_td.to_excel(writer, sheet_name='Tín dụng', index=False)
                df_dtnh.to_excel(writer, sheet_name='Dự trữ ngoại hối', index=False)
                df_dhtg.to_excel(writer, sheet_name='Tỷ giá trung tâm', index=False)
                df_lslnh.to_excel(writer, sheet_name='Lãi suất liên ngân hàng', index=False)
                df_lshd.to_excel(writer, sheet_name='Lãi suất huy động nhóm NH lớn', index=False)

                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Lãi suất tiền tệ",
                    data=buffer,
                    file_name="4_Dữ liệu Lãi suất tiền tệ.xlsx",
                    mime="application/vnd.ms-excel"
                )
        else:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_ctt.head(25).to_excel(writer, sheet_name='Cung tiền M2', index=False)
                df_hd.head(25).to_excel(writer, sheet_name='Huy động', index=False)
                df_td.head(25).to_excel(writer, sheet_name='Tín dụng', index=False)
                df_dtnh.head(25).to_excel(writer, sheet_name='Dự trữ ngoại hối', index=False)
                df_dhtg.head(25).to_excel(writer, sheet_name='Tỷ giá trung tâm', index=False)
                df_lslnh.head(25).to_excel(writer, sheet_name='Lãi suất liên ngân hàng', index=False)
                df_lshd.head(25).to_excel(writer, sheet_name='Lãi suất huy động nhóm NH lớn', index=False)

                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Lãi suất tiền tệ",
                    data=buffer,
                    file_name="4_Dữ liệu Lãi suất tiền tệ.xlsx",
                    mime="application/vnd.ms-excel"
                )