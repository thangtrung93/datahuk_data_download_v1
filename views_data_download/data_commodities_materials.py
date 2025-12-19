import streamlit as st
import requests
import pandas as pd
import io
from lib_download.commodities_materials import get_commodities_materials


def data_commodities_materials(customer_type):

    btn_refresh = st.button(label="Cập nhật dữ liệu")
    if btn_refresh:
        df_thep_day_trung_quoc,df_thep,df_thep_thanh_anh,df_hrc_trung_quoc,df_ton_lanh_hoa_sen_045mm,df_xi_mang,df_nhom,df_da_hoc,df_nhua_duong_60_70,df_ong_nhua_90x29mm,df_day_cap_dien,df_be_tong_mac_300 = get_commodities_materials()

        st.warning("Cập nhật xong!")
        if customer_type == "customer":
            
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_thep.to_excel(writer, sheet_name='Thép cuộn trong nước', index=False)
                df_thep_day_trung_quoc.to_excel(writer, sheet_name='Thép dây Trung Quốc', index=False)
                df_thep_thanh_anh.to_excel(writer, sheet_name='Thép thanh Anh', index=False)
                df_hrc_trung_quoc.to_excel(writer, sheet_name='HRC Trung Quốc', index=False)
                df_ton_lanh_hoa_sen_045mm.to_excel(writer, sheet_name='Tôn lạnh Hoa Sen', index=False)
                df_xi_mang.to_excel(writer, sheet_name='Xi măng Trung Quốc', index=False)
                df_nhua_duong_60_70.to_excel(writer, sheet_name='Nhựa đường', index=False)
                df_be_tong_mac_300.to_excel(writer, sheet_name='Bê tông', index=False)
                df_da_hoc.to_excel(writer, sheet_name='Đá hộc', index=False)
                df_ong_nhua_90x29mm.to_excel(writer, sheet_name='Ống nhựa', index=False)
                df_day_cap_dien.to_excel(writer, sheet_name='Cáp điện', index=False)
                
                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Hàng hóa_Vật liệu xây dựng",
                    data=buffer,
                    file_name="5_Dữ liệu Hàng hóa_Vật liệu xây dựng.xlsx",
                    mime="application/vnd.ms-excel"
                )
        else:
            
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_thep.head(25).to_excel(writer, sheet_name='Thép cuộn trong nước', index=False)
                df_thep_day_trung_quoc.head(25).to_excel(writer, sheet_name='Thép dây Trung Quốc', index=False)
                df_thep_thanh_anh.head(25).to_excel(writer, sheet_name='Thép thanh Anh', index=False)
                df_hrc_trung_quoc.head(25).to_excel(writer, sheet_name='HRC Trung Quốc', index=False)
                df_ton_lanh_hoa_sen_045mm.head(25).to_excel(writer, sheet_name='Tôn lạnh Hoa Sen', index=False)
                df_xi_mang.head(25).to_excel(writer, sheet_name='Xi măng Trung Quốc', index=False)
                df_nhua_duong_60_70.head(25).to_excel(writer, sheet_name='Nhựa đường', index=False)
                df_be_tong_mac_300.head(25).to_excel(writer, sheet_name='Bê tông', index=False)
                df_da_hoc.head(25).to_excel(writer, sheet_name='Đá hộc', index=False)
                df_ong_nhua_90x29mm.head(25).to_excel(writer, sheet_name='Ống nhựa', index=False)
                df_day_cap_dien.head(25).to_excel(writer, sheet_name='Cáp điện', index=False)
                
                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Hàng hóa_Vật liệu xây dựng",
                    data=buffer,
                    file_name="5_Dữ liệu Hàng hóa_Vật liệu xây dựng.xlsx",
                    mime="application/vnd.ms-excel"
                )