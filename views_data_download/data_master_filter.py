import streamlit as st
import requests
import pandas as pd
import io
from lib_download.master_filter import get_master_filter


def data_master_filter(customer_type):
    btn_refresh = st.button(label="Cập nhật dữ liệu")
    if btn_refresh:
        df_stock, df_master_filter = get_master_filter()
        st.warning("Cập nhật xong!")

        if customer_type == "customer":
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_stock.to_excel(writer, sheet_name='Danh sách mã', index=False)
                df_master_filter.to_excel(writer, sheet_name='Dữ liệu bộ lọc', index=False)

                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu cổ phiếu_Toàn bộ mã_Bộ lọc",
                    data=buffer,
                    file_name="1_Dữ liệu cổ phiếu_Toàn bộ mã_Bộ lọc.xlsx",
                    mime="application/vnd.ms-excel"
                )
        else:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_stock.head(25).to_excel(writer, sheet_name='Danh sách mã', index=False)
                df_master_filter.head(25).to_excel(writer, sheet_name='Dữ liệu bộ lọc', index=False)

                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu cổ phiếu_Toàn bộ mã_Bộ lọc",
                    data=buffer,
                    file_name="1_Dữ liệu cổ phiếu_Toàn bộ mã_Bộ lọc.xlsx",
                    mime="application/vnd.ms-excel"
                )