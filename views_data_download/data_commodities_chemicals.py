import streamlit as st
import requests
import pandas as pd
import io
from lib_download.commodities_chemicals import get_commodities_chemicals


def data_commodities_chemicals(customer_type):

    btn_refresh = st.button(label="Cập nhật dữ liệu")
    if btn_refresh:
        df_ure_trung_dong,df_luu_huynh,df_phot_pho,df_xut_naoh_trung_quoc,df_phan_dap_trung_quoc,df_phan_urea_trung_quoc = get_commodities_chemicals()

        st.warning("Cập nhật xong!")
        if customer_type == "customer":
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_ure_trung_dong.to_excel(writer, sheet_name='Ure Trung Đông', index=False)
                df_luu_huynh.to_excel(writer, sheet_name='Lưu huỳnh Trung Quốc', index=False)
                df_phot_pho.to_excel(writer, sheet_name='Phốt pho Trung Quốc', index=False)
                df_xut_naoh_trung_quoc.to_excel(writer, sheet_name='Xút NaOH Trung Quốc', index=False)
                df_phan_dap_trung_quoc.to_excel(writer, sheet_name='Phân DAP Trung Quốc', index=False)
                df_phan_urea_trung_quoc.to_excel(writer, sheet_name='Phân Ure Trung Quốc', index=False)
                
                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Hàng hóa_Hóa chất",
                    data=buffer,
                    file_name="5_Dữ liệu Hàng hóa_Hóa chất.xlsx",
                    mime="application/vnd.ms-excel"
                )
        else:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_ure_trung_dong.head(25).to_excel(writer, sheet_name='Ure Trung Đông', index=False)
                df_luu_huynh.head(25).to_excel(writer, sheet_name='Lưu huỳnh Trung Quốc', index=False)
                df_phot_pho.head(25).to_excel(writer, sheet_name='Phốt pho Trung Quốc', index=False)
                df_xut_naoh_trung_quoc.head(25).to_excel(writer, sheet_name='Xút NaOH Trung Quốc', index=False)
                df_phan_dap_trung_quoc.head(25).to_excel(writer, sheet_name='Phân DAP Trung Quốc', index=False)
                df_phan_urea_trung_quoc.head(25).to_excel(writer, sheet_name='Phân Ure Trung Quốc', index=False)
                
                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Hàng hóa_Hóa chất",
                    data=buffer,
                    file_name="5_Dữ liệu Hàng hóa_Hóa chất.xlsx",
                    mime="application/vnd.ms-excel"
                )