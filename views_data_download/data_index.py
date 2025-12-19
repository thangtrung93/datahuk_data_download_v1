import streamlit as st
import requests
import pandas as pd
import io
from lib_download.index import get_index


def data_index(customer_type):
    col1, col2, col3 = st.columns([5,5,5])
    with col1:
        n_days = st.number_input(label="Số ngày cần lấy dữ liệu", min_value=365)

    btn_refresh = st.button(label="Cập nhật dữ liệu")
    if btn_refresh:
        df_vnindex, df_hnxindex, df_upcomindex = get_index(n_days)
        st.warning("Cập nhật xong!")

        if customer_type == "customer":
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_vnindex.to_excel(writer, sheet_name='VNINDEX', index=False)
                df_hnxindex.to_excel(writer, sheet_name='HNX_INDEX', index=False)
                df_upcomindex.to_excel(writer, sheet_name='UPCOM_INDEX', index=False)

                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu VNINDEX",
                    data=buffer,
                    file_name="2.1_Dữ liệu VNINDEX.xlsx",
                    mime="application/vnd.ms-excel"
                    # use_container_width=True
                )
        else:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_vnindex.head(25).to_excel(writer, sheet_name='VNINDEX', index=False)
                df_hnxindex.head(25).to_excel(writer, sheet_name='HNX_INDEX', index=False)
                df_upcomindex.head(25).to_excel(writer, sheet_name='UPCOM_INDEX', index=False)

                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu VNINDEX",
                    data=buffer,
                    file_name="2.1_Dữ liệu VNINDEX.xlsx",
                    mime="application/vnd.ms-excel"
                    # use_container_width=True
                )