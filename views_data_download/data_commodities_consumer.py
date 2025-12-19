import streamlit as st
import requests
import pandas as pd
import io
from lib_download.commodities_consumer import get_commodities_consumer


def data_commodities_consumer(customer_type):

    btn_refresh = st.button(label="Cập nhật dữ liệu")
    if btn_refresh:
        df_lon_hoi_trung_quoc,df_heo_hoi,df_bot_giay,df_vai_coton,df_soi_coton,df_dau_co_malaysia,df_giay_gon_song_trung_quoc,df_dau_nanh_my,df_duong,df_ca_phe,df_tieu,df_vai_cotton_my,df_gao_tpxk,df_tom_su,df_tom_the = get_commodities_consumer()

        st.warning("Cập nhật xong!")

        if customer_type =="customer":
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_gao_tpxk.to_excel(writer, sheet_name='Gạo xuất khẩu', index=False)
                df_soi_coton.to_excel(writer, sheet_name='Sợi cotton Trung Quốc', index=False)
                df_vai_coton.to_excel(writer, sheet_name='Vải cotton Trung Quốc', index=False)
                df_vai_cotton_my.to_excel(writer, sheet_name='Vải cotton Mỹ', index=False)
                df_tieu.to_excel(writer, sheet_name='Hồ tiêu', index=False)
                df_ca_phe.to_excel(writer, sheet_name='Cà phê trong nước', index=False)
                df_duong.to_excel(writer, sheet_name='Đường', index=False)
                df_dau_nanh_my.to_excel(writer, sheet_name='Đậu nành Mỹ', index=False)
                df_lon_hoi_trung_quoc.to_excel(writer, sheet_name='Lợn hơi Trung Quốc', index=False)
                df_heo_hoi.to_excel(writer, sheet_name='Heo nội địa', index=False)
                df_bot_giay.to_excel(writer, sheet_name='Bột giấy Trung Quốc', index=False)
                df_giay_gon_song_trung_quoc.to_excel(writer, sheet_name='Giấy gợn sóng Trung Quốc', index=False)
                df_dau_co_malaysia.to_excel(writer, sheet_name='Dầu cọ Malaysia', index=False)
                df_tom_the.to_excel(writer, sheet_name='Tôm thẻ', index=False)
                df_tom_su.to_excel(writer, sheet_name='Tôm sú', index=False)

                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Hàng hóa_Hàng tiêu dùng",
                    data=buffer,
                    file_name="5_Dữ liệu Hàng hóa_Hàng tiêu dùng.xlsx",
                    mime="application/vnd.ms-excel"
                )
        else:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_gao_tpxk.head(25).to_excel(writer, sheet_name='Gạo xuất khẩu', index=False)
                df_soi_coton.head(25).to_excel(writer, sheet_name='Sợi cotton Trung Quốc', index=False)
                df_vai_coton.head(25).to_excel(writer, sheet_name='Vải cotton Trung Quốc', index=False)
                df_vai_cotton_my.head(25).to_excel(writer, sheet_name='Vải cotton Mỹ', index=False)
                df_tieu.head(25).to_excel(writer, sheet_name='Hồ tiêu', index=False)
                df_ca_phe.head(25).to_excel(writer, sheet_name='Cà phê trong nước', index=False)
                df_duong.head(25).to_excel(writer, sheet_name='Đường', index=False)
                df_dau_nanh_my.head(25).to_excel(writer, sheet_name='Đậu nành Mỹ', index=False)
                df_lon_hoi_trung_quoc.head(25).to_excel(writer, sheet_name='Lợn hơi Trung Quốc', index=False)
                df_heo_hoi.head(25).to_excel(writer, sheet_name='Heo nội địa', index=False)
                df_bot_giay.head(25).to_excel(writer, sheet_name='Bột giấy Trung Quốc', index=False)
                df_giay_gon_song_trung_quoc.head(25).to_excel(writer, sheet_name='Giấy gợn sóng Trung Quốc', index=False)
                df_dau_co_malaysia.head(25).to_excel(writer, sheet_name='Dầu cọ Malaysia', index=False)
                df_tom_the.head(25).to_excel(writer, sheet_name='Tôm thẻ', index=False)
                df_tom_su.head(25).to_excel(writer, sheet_name='Tôm sú', index=False)

                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Hàng hóa_Hàng tiêu dùng",
                    data=buffer,
                    file_name="5_Dữ liệu Hàng hóa_Hàng tiêu dùng.xlsx",
                    mime="application/vnd.ms-excel"
                )
            