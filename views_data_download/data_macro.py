import streamlit as st
import requests
import pandas as pd
import io
from lib_download.macro import get_macro


def data_macro(customer_type):

    btn_refresh = st.button(label="Cập nhật dữ liệu")
    if btn_refresh:
        df_gdp_q, df_gdp_y, df_gdpbinhquan, df_cpi, df_iip, df_pmi, df_hhdv, df_vdtptxh, df_vdtnsnn, df_fdi, df_cctm, df_cctt, df_vt, df_kqt, df_ds, df_tn, df_ld, df_tcns, df_ncp = get_macro()

        st.warning("Cập nhật xong!")
        
        if customer_type == "customer":
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_gdp_q.to_excel(writer, sheet_name='GDP_Quý', index=False)
                df_gdp_y.to_excel(writer, sheet_name='GDP_Năm', index=False)
                df_gdpbinhquan.to_excel(writer, sheet_name='GDP_Bình quân', index=False)
                df_cpi.to_excel(writer, sheet_name='CPI_Tháng', index=False)
                df_iip.to_excel(writer, sheet_name='SX Công nghiệp_Tháng', index=False)
                df_pmi.to_excel(writer, sheet_name='PMI_Tháng', index=False)
                df_hhdv.to_excel(writer, sheet_name='Hàng hóa_Dịch vụ_Tháng', index=False)
                df_vdtptxh.to_excel(writer, sheet_name='Vốn đầu tư PTXH_Quý', index=False)
                df_vdtnsnn.to_excel(writer, sheet_name='Vốn Ngân sách Nhà nước_Tháng', index=False)
                df_fdi.to_excel(writer, sheet_name='FDI_Tháng', index=False)
                df_cctm.to_excel(writer, sheet_name='Cán cân thương mại_Tháng', index=False)
                df_cctt.to_excel(writer, sheet_name='Cán cân Thanh toán_Quý', index=False)
                df_vt.to_excel(writer, sheet_name='Vận tải_Tháng', index=False)
                df_kqt.to_excel(writer, sheet_name='Khách quốc tế_Tháng', index=False)
                df_ds.to_excel(writer, sheet_name='Dân số_Năm', index=False)
                df_tn.to_excel(writer, sheet_name='Thất nghiệp_Quý', index=False)
                df_ld.to_excel(writer, sheet_name='Lao động_Quý', index=False)
                df_ncp.to_excel(writer, sheet_name='Nợ chính phủ_Năm', index=False)
                df_tcns.to_excel(writer, sheet_name='Thu chi ngân sách_Quý', index=False)

                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Vĩ mô",
                    data=buffer,
                    file_name="3_Dữ liệu Vĩ mô.xlsx",
                    mime="application/vnd.ms-excel"
                )
        else:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_gdp_q.head(25).to_excel(writer, sheet_name='GDP_Quý', index=False)
                df_gdp_y.head(25).to_excel(writer, sheet_name='GDP_Năm', index=False)
                df_gdpbinhquan.head(25).to_excel(writer, sheet_name='GDP_Bình quân', index=False)
                df_cpi.head(25).to_excel(writer, sheet_name='CPI_Tháng', index=False)
                df_iip.head(25).to_excel(writer, sheet_name='SX Công nghiệp_Tháng', index=False)
                df_pmi.head(25).to_excel(writer, sheet_name='PMI_Tháng', index=False)
                df_hhdv.head(25).to_excel(writer, sheet_name='Hàng hóa_Dịch vụ_Tháng', index=False)
                df_vdtptxh.head(25).to_excel(writer, sheet_name='Vốn đầu tư PTXH_Quý', index=False)
                df_vdtnsnn.head(25).to_excel(writer, sheet_name='Vốn Ngân sách Nhà nước_Tháng', index=False)
                df_fdi.head(25).to_excel(writer, sheet_name='FDI_Tháng', index=False)
                df_cctm.head(25).to_excel(writer, sheet_name='Cán cân thương mại_Tháng', index=False)
                df_cctt.head(25).to_excel(writer, sheet_name='Cán cân Thanh toán_Quý', index=False)
                df_vt.head(25).to_excel(writer, sheet_name='Vận tải_Tháng', index=False)
                df_kqt.head(25).to_excel(writer, sheet_name='Khách quốc tế_Tháng', index=False)
                df_ds.head(25).to_excel(writer, sheet_name='Dân số_Năm', index=False)
                df_tn.head(25).to_excel(writer, sheet_name='Thất nghiệp_Quý', index=False)
                df_ld.head(25).to_excel(writer, sheet_name='Lao động_Quý', index=False)
                df_ncp.head(25).to_excel(writer, sheet_name='Nợ chính phủ_Năm', index=False)
                df_tcns.head(25).to_excel(writer, sheet_name='Thu chi ngân sách_Quý', index=False)


                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Vĩ mô",
                    data=buffer,
                    file_name="3_Dữ liệu Vĩ mô.xlsx",
                    mime="application/vnd.ms-excel"
                )