import streamlit as st
import requests
import pandas as pd
import io
from lib_download.macro_detail import get_macro_detail


def data_macro_detail(customer_type):

    btn_refresh = st.button(label="Cập nhật dữ liệu")
    if btn_refresh:
        df_gdp_q,df_gdp_y,df_cpi_m,df_cpi_y,df_import_export_m,df_import_export_y,df_industry_index_m,df_industry_index_y,df_retail_index_m,df_retail_index_y = get_macro_detail()

        st.warning("Cập nhật xong!")
        
        if customer_type == "customer":
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_gdp_q.to_excel(writer, sheet_name='GDP_Quý', index=False)
                df_gdp_y.to_excel(writer, sheet_name='GDP_Năm', index=False)
                df_cpi_m.to_excel(writer, sheet_name='CPI_Tháng', index=False)
                df_cpi_y.to_excel(writer, sheet_name='CPI_Năm', index=False)
                df_industry_index_m.to_excel(writer, sheet_name='SX Công nghiệp_Tháng', index=False)
                df_industry_index_y.to_excel(writer, sheet_name='SX Công nghiệp_Năm', index=False)
                df_retail_index_m.to_excel(writer, sheet_name='Bán lẻ_Tháng', index=False)
                df_retail_index_y.to_excel(writer, sheet_name='Bán lẻ_Năm', index=False)
                df_import_export_m.to_excel(writer, sheet_name='XNK_Tháng', index=False)
                df_import_export_y.to_excel(writer, sheet_name='XNK_Năm', index=False)

                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Vĩ mô_Chi tiết",
                    data=buffer,
                    file_name="3_Dữ liệu Vĩ mô_Chi tiết.xlsx",
                    mime="application/vnd.ms-excel"
                )
        else:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_gdp_q.head(25).to_excel(writer, sheet_name='GDP_Quý', index=False)
                df_gdp_y.head(25).to_excel(writer, sheet_name='GDP_Năm', index=False)
                df_cpi_m.head(25).to_excel(writer, sheet_name='CPI_Tháng', index=False)
                df_cpi_y.head(25).to_excel(writer, sheet_name='CPI_Năm', index=False)
                df_industry_index_m.head(25).to_excel(writer, sheet_name='SX Công nghiệp_Tháng', index=False)
                df_industry_index_y.head(25).to_excel(writer, sheet_name='SX Công nghiệp_Năm', index=False)
                df_retail_index_m.head(25).to_excel(writer, sheet_name='Bán lẻ_Tháng', index=False)
                df_retail_index_y.head(25).to_excel(writer, sheet_name='Bán lẻ_Năm', index=False)
                df_import_export_m.head(25).to_excel(writer, sheet_name='XNK_Tháng', index=False)
                df_import_export_y.head(25).to_excel(writer, sheet_name='XNK_Năm', index=False)
                
                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Vĩ mô_Chi tiết",
                    data=buffer,
                    file_name="3_Dữ liệu Vĩ mô_Chi tiết.xlsx",
                    mime="application/vnd.ms-excel"
                )