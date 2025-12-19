import streamlit as st
import requests
import pandas as pd
import io
from lib_download.commodities_metal import get_commodities_metal


def data_commodities_metal(customer_type):

    btn_refresh = st.button(label="Cập nhật dữ liệu")
    if btn_refresh:
        df_quang_sat,df_chi,df_thiec, df_kem,df_nhom,df_niken,df_vang_the_gioi, df_vang, df_bac, df_dong = get_commodities_metal()

        st.warning("Cập nhật xong!")
        if customer_type == "customer":
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_quang_sat.to_excel(writer, sheet_name='Quặng sắt Trung Quốc', index=False)
                df_chi.to_excel(writer, sheet_name='Chì Trung Quốc', index=False)
                df_thiec.to_excel(writer, sheet_name='Thiếc Trung Quốc', index=False)
                df_kem.to_excel(writer, sheet_name='Kẽm Trung Quốc', index=False)
                df_nhom.to_excel(writer, sheet_name='Nhôm Trung Quốc', index=False)
                df_niken.to_excel(writer, sheet_name='Niken Trung Quốc', index=False)
                df_vang_the_gioi.to_excel(writer, sheet_name='Vàng', index=False)
                df_vang.to_excel(writer, sheet_name='Vàng trong nước', index=False)
                df_bac.to_excel(writer, sheet_name='Bạc', index=False)
                df_dong.to_excel(writer, sheet_name='Đồng', index=False)
                
                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Hàng hóa_Kim loại",
                    data=buffer,
                    file_name="5_Dữ liệu Hàng hóa_Kim loại.xlsx",
                    mime="application/vnd.ms-excel"
                )
        else:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_quang_sat.head(25).to_excel(writer, sheet_name='Quặng sắt Trung Quốc', index=False)
                df_chi.head(25).to_excel(writer, sheet_name='Chì Trung Quốc', index=False)
                df_thiec.head(25).to_excel(writer, sheet_name='Thiếc Trung Quốc', index=False)
                df_kem.head(25).to_excel(writer, sheet_name='Kẽm Trung Quốc', index=False)
                df_nhom.head(25).to_excel(writer, sheet_name='Nhôm Trung Quốc', index=False)
                df_niken.head(25).to_excel(writer, sheet_name='Niken Trung Quốc', index=False)
                df_vang_the_gioi.head(25).to_excel(writer, sheet_name='Vàng', index=False)
                df_vang.head(25).to_excel(writer, sheet_name='Vàng trong nước', index=False)
                df_bac.head(25).to_excel(writer, sheet_name='Bạc', index=False)
                df_dong.head(25).to_excel(writer, sheet_name='Đồng', index=False)
                
                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Hàng hóa_Kim loại",
                    data=buffer,
                    file_name="5_Dữ liệu Hàng hóa_Kim loại.xlsx",
                    mime="application/vnd.ms-excel"
                )