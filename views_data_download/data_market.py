import streamlit as st
import requests
import pandas as pd
import io
from lib_download.market_index import get_market_index


def data_market(customer_type):
    btn_refresh = st.button(label="Cập nhật dữ liệu")
    if btn_refresh:
        df_flow_breadth, df_flow_market_foreign_value, df_flow_market_value_trading, df_flow_industry_index, df_flow_supply_demand = get_market_index()

        st.warning("Cập nhật xong!")

        if customer_type == "customer":
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_flow_industry_index.to_excel(writer, sheet_name='Chỉ số ngành', index=False)
                df_flow_breadth.to_excel(writer, sheet_name='Độ rộng thị trường', index=False)
                df_flow_market_foreign_value.to_excel(writer, sheet_name='Giá trị GD ròng Nước ngoài', index=False)
                df_flow_market_value_trading.to_excel(writer, sheet_name='Giá trị giao dịch', index=False)
                df_flow_supply_demand.to_excel(writer, sheet_name='Cung cầu', index=False)

                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Thị trường",
                    data=buffer,
                    file_name="2_Dữ liệu Thị trường.xlsx",
                    mime="application/vnd.ms-excel"
                )
        else:
            buffer = io.BytesIO()
            with pd.ExcelWriter(buffer, engine='xlsxwriter') as writer:

                # Write each dataframe to a different worksheet.
                df_flow_industry_index.head(25).to_excel(writer, sheet_name='Chỉ số ngành', index=False)
                df_flow_breadth.head(25).to_excel(writer, sheet_name='Độ rộng thị trường', index=False)
                df_flow_market_foreign_value.head(25).to_excel(writer, sheet_name='Giá trị GD ròng Nước ngoài', index=False)
                df_flow_market_value_trading.head(25).to_excel(writer, sheet_name='Giá trị giao dịch', index=False)
                df_flow_supply_demand.head(25).to_excel(writer, sheet_name='Cung cầu', index=False)

                # Close the Pandas Excel writer and output the Excel file to the buffer
                writer.close()
                st.download_button(
                    label="Tải Dữ liệu Thị trường",
                    data=buffer,
                    file_name="2_Dữ liệu Thị trường.xlsx",
                    mime="application/vnd.ms-excel"
                )