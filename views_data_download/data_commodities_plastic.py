import streamlit as st
import requests
import pandas as pd
import io
from lib_download.commodities_plastic import get_commodities_plastic


def data_commodities_plastic(customer_type):

    btn_refresh = st.button(label="Cập nhật dữ liệu")
    if btn_refresh:
        df_cao_su_nhat_ban, df_pet_trung_quoc, df_nhua_pvc_trung_quoc, df_nhua_pp_trung_quoc, df_cao_su = get_commodities_plastic()

        st.warning("Cập nhật xong!")
        if customer_type == "customer":
            
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_cao_su_nhat_ban.to_excel(writer, sheet_name='Cao su Nhật Bản', index=False)
                df_cao_su.to_excel(writer, sheet_name='Cao su trong nước', index=False)
                df_pet_trung_quoc.to_excel(writer, sheet_name='Nhựa PET Trung Quốc', index=False)
                df_nhua_pvc_trung_quoc.to_excel(writer, sheet_name='Nhựa PVC Trung Quốc', index=False)
                df_nhua_pp_trung_quoc.to_excel(writer, sheet_name='Nhựa PP Trung Quốc', index=False)
                
                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Hàng hóa_Nhựa và cao su",
                    data=buffer,
                    file_name="5_Dữ liệu Hàng hóa_Nhựa và cao su.xlsx",
                    mime="application/vnd.ms-excel"
                )
        else:
                
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_cao_su_nhat_ban.head(25).to_excel(writer, sheet_name='Cao su Nhật Bản', index=False)
                df_cao_su.head(25).to_excel(writer, sheet_name='Cao su trong nước', index=False)
                df_pet_trung_quoc.head(25).to_excel(writer, sheet_name='Nhựa PET Trung Quốc', index=False)
                df_nhua_pvc_trung_quoc.head(25).to_excel(writer, sheet_name='Nhựa PVC Trung Quốc', index=False)
                df_nhua_pp_trung_quoc.head(25).to_excel(writer, sheet_name='Nhựa PP Trung Quốc', index=False)
                
                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Hàng hóa_Nhựa và cao su",
                    data=buffer,
                    file_name="5_Dữ liệu Hàng hóa_Nhựa và cao su.xlsx",
                    mime="application/vnd.ms-excel"
                )