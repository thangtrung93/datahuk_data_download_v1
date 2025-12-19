import streamlit as st
import requests
import pandas as pd
import io
from lib_download.commodities_energy import get_commodities_energy


def data_commodities_energy(customer_type):

    btn_refresh = st.button(label="Cập nhật dữ liệu")
    if btn_refresh:
        df_than_coc,df_khi_lpg_trung_quoc,df_khi_thien_nhien,df_xang_dau,df_dau_wti = get_commodities_energy()

        st.warning("Cập nhật xong!")
        if customer_type == "customer":
            
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_than_coc.to_excel(writer, sheet_name='Than cốc Trung Quốc', index=False)
                df_dau_wti.to_excel(writer, sheet_name='Dầu WTI', index=False)
                df_khi_lpg_trung_quoc.to_excel(writer, sheet_name='Khí LPG Trung Quốc', index=False)
                df_khi_thien_nhien.to_excel(writer, sheet_name='Khí thiên nhiên', index=False)
                df_xang_dau.to_excel(writer, sheet_name='Xăng dầu', index=False)

                
                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Hàng hóa_Năng lượng",
                    data=buffer,
                    file_name="5_Dữ liệu Hàng hóa_Năng lượng.xlsx",
                    mime="application/vnd.ms-excel"
                )
        else:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_than_coc.head(25).to_excel(writer, sheet_name='Than cốc Trung Quốc', index=False)
                df_dau_wti.head(25).to_excel(writer, sheet_name='Dầu WTI', index=False)
                df_khi_lpg_trung_quoc.head(25).to_excel(writer, sheet_name='Khí LPG Trung Quốc', index=False)
                df_khi_thien_nhien.head(25).to_excel(writer, sheet_name='Khí thiên nhiên', index=False)
                df_xang_dau.head(25).to_excel(writer, sheet_name='Xăng dầu', index=False)

                
                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Hàng hóa_Năng lượng",
                    data=buffer,
                    file_name="5_Dữ liệu Hàng hóa_Năng lượng.xlsx",
                    mime="application/vnd.ms-excel"
                )