import toml
import streamlit as st
import requests
import toml
import pandas as pd
import io
import time
from concurrent.futures import ThreadPoolExecutor

# local_path = local_path()
# local secrets
# secrets = toml.load(local_path + ".streamlit/secrets.toml")
api_base_tcbs = st.secrets["api"]["api_base_tcbs"]
api_base_stockbiz = st.secrets["api"]["api_base_stockbiz"]


d_dividend = {"cash":"Tiền mặt", "share": "Cổ phiếu"}
d_headers = {
    "stockbiz": {"Authorization": "Bearer eyJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiIsIng1dCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSIsImtpZCI6IkdYdExONzViZlZQakdvNERWdjV4QkRITHpnSSJ9.eyJpc3MiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4iLCJhdWQiOiJodHRwczovL2FjY291bnRzLmZpcmVhbnQudm4vcmVzb3VyY2VzIiwiZXhwIjoxODg5NjIyNTMwLCJuYmYiOjE1ODk2MjI1MzAsImNsaWVudF9pZCI6ImZpcmVhbnQudHJhZGVzdGF0aW9uIiwic2NvcGUiOlsiYWNhZGVteS1yZWFkIiwiYWNhZGVteS13cml0ZSIsImFjY291bnRzLXJlYWQiLCJhY2NvdW50cy13cml0ZSIsImJsb2ctcmVhZCIsImNvbXBhbmllcy1yZWFkIiwiZmluYW5jZS1yZWFkIiwiaW5kaXZpZHVhbHMtcmVhZCIsImludmVzdG9wZWRpYS1yZWFkIiwib3JkZXJzLXJlYWQiLCJvcmRlcnMtd3JpdGUiLCJwb3N0cy1yZWFkIiwicG9zdHMtd3JpdGUiLCJzZWFyY2giLCJzeW1ib2xzLXJlYWQiLCJ1c2VyLWRhdGEtcmVhZCIsInVzZXItZGF0YS13cml0ZSIsInVzZXJzLXJlYWQiXSwianRpIjoiMjYxYTZhYWQ2MTQ5Njk1ZmJiYzcwODM5MjM0Njc1NWQifQ.dA5-HVzWv-BRfEiAd24uNBiBxASO-PAyWeWESovZm_hj4aXMAZA1-bWNZeXt88dqogo18AwpDQ-h6gefLPdZSFrG5umC1dVWaeYvUnGm62g4XS29fj6p01dhKNNqrsu5KrhnhdnKYVv9VdmbmqDfWR8wDgglk5cJFqalzq6dJWJInFQEPmUs9BW_Zs8tQDn-i5r4tYq2U8vCdqptXoM7YgPllXaPVDeccC9QNu2Xlp9WUvoROzoQXg25lFub1IYkTrM66gJ6t9fJRZToewCt495WNEOQFa_rwLCZ1QwzvL0iYkONHS_jZ0BOhBCdW9dWSawD6iF1SIQaFROvMDH1rg"},
    "tcbs": {"Authorization":"Bearer eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCJ9.eyJpc3MiOiJhdXRoZW5fc2VydmljZSIsImV4cCI6MTc2NjE1NzcwNiwianRpIjoiIiwiaWF0IjoxNzY2MTE0NTA2LCJzdWIiOiIxMDAwMDY3MTk4OCIsImN1c3RvZHlJRCI6IjEwNUM1MTI4MTQiLCJ0Y2JzSWQiOiIxMDAwMDY3MTk4OCIsImVtYWlsIjoidGhhbmd0cnVuZzkzQGdtYWlsLmNvbSIsInJvbGVzIjpbImN1c3RvbWVyIl0sInNjb3BlcyI6WyJhbGw6YWxsIiwic29ja2V0OmFsbCJdLCJzdGVwdXBfZXhwIjowLCJzb3RwX3NpZ24iOiIiLCJjbGllbnRfa2V5IjoiMTAwMDA2NzE5ODguOVQyUkJXZmp6Tk9mSWxBU1BIRjIiLCJzZXNzaW9uSUQiOiJlMGI2MzU4Ny03ZWQ1LTQ4NzQtODFmNy04NWFmMDAyMGJkZmIiLCJhY2NvdW50X3N0YXR1cyI6IjEiLCJvdHAiOiIiLCJvdHBUeXBlIjoiIiwib3RwU291cmNlIjoiVENJTlZFU1QiLCJvdHBTZXNzaW9uSWQiOiIiLCJhY2NvdW50VHlwZSI6IlBSSU1BUlkiLCJwcmltYXJ5U3ViIjoiIiwicHJpbWFyeUN1c3RvZHlJRCI6IiIsImVub3RwX3NpZ24iOiIiLCJzcWFfc2lnbiI6IiIsImVuX290cCI6IiIsImVuT1RQVHlwZSI6IiIsImNhU3RhdHVzIjoiSUdOT1JFIiwiY3VzVHlwZSI6IklORElWSURVQUwiLCJ0ZW5hbnQiOiJ0Y2JzIn0.SJdq8L6uJeunnpFFy3EEtvpJQFfvMj1gGjTLrVhy8zJ7_x5sdLGvFoybpKKjrYP4jkWIrsaQiNNyIoKnAFNOo_dw2HmYFBUEqk-4PRnV-N0tLcuwftlzKcPwf_DvMfaEgHoOY9xDbVKMcb34evt-vnd0KPrlxk38Q_8J3IOBHNPIJFMwWRAxi-LonT4QE_hCquZji-8-ChcC3mE2gmjXsFxtSrJ0WL8S_1bkUr4KXmzqrCGAuDNR3NAD2NoDMqwUwP6sV-maPy8qnNX2w-27xkNwVaBwZjDrWlrqdZiQobVDH3aBgh8_Xn1WGTXpbvPFLFkdaPiZdO0cBzppoj51Ng"}
}


def get_overview(ticker):
    # get url
    def get_url_overview(ticker):
        d_url = {
            "overview": f'{api_base_tcbs}tcanalysis/v1/ticker/{ticker}/overview',
            "dividend": f'{api_base_tcbs}tcanalysis/v1/company/{ticker}/dividend-payment-histories?page=0&size=20',
            "shareholders": f'{api_base_stockbiz}{ticker}/holders',
            "sub_companies": f'{api_base_stockbiz}{ticker}/subsidiaries',
            "audit_firm": f'{api_base_tcbs}tcanalysis/v1/company/{ticker}/audit-firms?page=0&size=10',
            "evaluation_history": f'{api_base_tcbs}tcanalysis/v1/evaluation/{ticker}/historical-chart?period=1&tWindow=D',
            "stock_indicator": f'{api_base_tcbs}tcanalysis/v1/data-charts/indicator?ticker={ticker}',
            "stock_foreign_volume": f'{api_base_tcbs}tcanalysis/v1/data-charts/vol-foreign?ticker={ticker}'

        }
        return d_url
    def get_headers_by_url():
        d_headers_by_url = {
            "overview": "tcbs",
            "dividend": "tcbs",
            "shareholders": "stockbiz",
            "sub_companies": "stockbiz",
            "audit_firm": "tcbs",
            "evaluation_history": "tcbs",
            "stock_indicator": "tcbs",
            "stock_foreign_volume": "tcbs"
        }
        return d_headers_by_url

    d_url = get_url_overview(ticker)
    d_headers_by_url = get_headers_by_url()

    # function: get json
    def get_json(url, headers):
        req = requests.get(url, headers=headers).json()
        time.sleep(2)
        return req
    
    def get_json_all(d_url):
        executor = ThreadPoolExecutor(100)

        d_json = {key: [] for key in list(d_url.keys())}
        for key_x, url in d_url.items():
            try:
                headers = d_headers[d_headers_by_url[key_x]]
                future = executor.submit(get_json, (url), (headers))
                d_json[key_x] = future
            except:
                pass
        return d_json
    
    d_json_all = get_json_all(d_url)

    # function: get df
    def get_df_overview():
        l_col = ["Mã", "Sàn", "Tên viết tắt", "Ngành", "Năm thành lập", "Số lượng nhân viên", "Số lượng cổ đông", "Sở hữu khối ngoại", "Website", "Số lượng cổ phiếu niêm yết_triệu cổ", "Số lượng cổ phiếu phát hành_triệu cổ"]
        try:
            req = d_json_all["overview"].result()
            industry_type = req["industry"]
            df = pd.json_normalize(req)
            df.rename(columns={ "ticker" : "Mã",  "exchange" : "Sàn",  "shortName" : "Tên viết tắt",  "industry" : "Ngành",  "establishedYear" : "Năm thành lập",  "noEmployees" : "Số lượng nhân viên",  "foreignPercent" : "Sở hữu khối ngoại",  "website" : "Website",  "noShareholders" : "Số lượng cổ đông",  "outstandingShare" : "Số lượng cổ phiếu niêm yết_triệu cổ",  "issueShare" : "Số lượng cổ phiếu phát hành_triệu cổ"}, inplace=True)
            df = df[l_col]
        except:
            df = pd.DataFrame(columns=l_col)
        return df, industry_type

    def get_df_dividend():
        l_col = ["Mã", "Năm", "Ngày", "Hình thức", "Tỷ lệ cổ tức"]
        try:
            req = d_json_all["dividend"].result()
            df = pd.json_normalize(req["listDividendPaymentHis"])
            df["issueMethod"] = df["issueMethod"].apply(lambda x: d_dividend[x])
            df.rename(columns={"ticker": "Mã", "exerciseDate": "Ngày", "cashYear": "Năm", "cashDividendPercentage": "Tỷ lệ cổ tức", "issueMethod": "Hình thức"}, inplace=True)
            df = df[l_col]
        except:
            df = pd.DataFrame(columns=l_col)
        return df

    def get_df_shareholders():
        l_col = ["Mã", "Mã CK tổ chức sở hữu", "Sàn", "Tên", "Vị trí","Số lượng cổ phần","Tỷ lệ sở hữu", "Cập nhật"]
        try:
            req = d_json_all["shareholders"].result()
            df = pd.json_normalize(req)
            df["reported"] = df["reported"].apply(lambda x: x.replace("T00:00:00",""))
            df.rename(columns={"Custom": "Mã", "reported": "Cập nhật", "ownership": "Tỷ lệ sở hữu", "shares": "Số lượng cổ phần", "position": "Vị trí", "name": "Tên", "institutionHolderSymbol": "Mã CK tổ chức sở hữu", "institutionHolderExchange": "Sàn"}, inplace=True)
            df["Mã"] = ticker
            df = df[l_col]
        except:
            df = pd.DataFrame(columns=l_col)
        return df


    def get_df_sub_companies():
        l_col = ["Mã", "Tên", "Mã CK trên sàn", "Sàn", "Tỷ lệ sở hữu","Số lượng cổ phần","Vốn Điều lệ"]
        try:
            req = d_json_all["sub_companies"].result()
            df = pd.json_normalize(req)
            df = df[df["ownership"] > 0]
            df.rename(columns={"Custom": "Mã", "companyName": "Tên", "exchange": "Sàn", "symbol": "Mã CK trên sàn", "ownership": "Tỷ lệ sở hữu", "shares": "Số lượng cổ phần", "charterCapital": "Vốn Điều lệ"}, inplace=True)
            df["Mã"] = ticker
            df = df[l_col]
        except:
            df = pd.DataFrame(columns=l_col)
        return df

    
    def get_df_audit_firm():
        l_col = ["Mã", "Năm", "Công ty Kiểm toán"]
        try:
            req = d_json_all["audit_firm"].result()
            df = pd.json_normalize(req["listAuditFirm"])
            df.rename(columns={"ticker": "Mã", "yearReport": "Năm", "auditFirmName": "Công ty Kiểm toán"}, inplace=True)
            df = df[l_col]
        except:
            df = pd.DataFrame(columns=l_col)
        return df


    def get_df_evaluation_history():
        l_col = ["Mã", "Ngày", "PE", "PB", "PE_ngành", "PB_ngành", "PE_vnindex", "PB_vnindex"]
        try:
            req = d_json_all["evaluation_history"].result()
            df = pd.json_normalize(req["data"])
            df.rename(columns={"to": "Ngày", "pe": "PE", "pb": "PB", "industryPe": "PE_ngành", "industryPb": "PB_ngành", "indexPe": "PE_vnindex", "indexPb": "PB_vnindex"}, inplace=True)
            df["Mã"] = ticker
            df = df[l_col]
        except:
            df = pd.DataFrame(columns=l_col)
        return df


    def get_df_stock_indicator():
        l_col = ["Ngày", "Mã", "Giá đóng cửa", "SMA5", "SMA20", "MACD", "MACD_histogram", "Stockhk", "Stockhd", "RSI", "ADX"]
        try:
            req = d_json_all["stock_indicator"].result()
            df = pd.json_normalize(req["listTechnicalIndicator"])
            df.rename(columns={"ticker": "Mã", "closePrice": "Giá đóng cửa", "sma5": "SMA5", "sma20": "SMA20", "macd": "MACD", "macdhist": "MACD_histogram", "rsi": "RSI", "adx": "ADX", "stochk": "Stockhk", "stochd": "Stockhd", "dateReport": "Ngày"}, inplace=True)
            df = df[l_col]
            df['Ngày'] = pd.to_datetime(df['Ngày'], format="%d/%m/%Y")
        except:
            df = pd.DataFrame(columns=l_col)
        return df

    def get_df_stock_foreign_volume():
        l_col = ["Ngày", "Mã", "KLGD_Nước ngoài_Mua", "KLGD_Nước ngoài_Bán", "KLGD_Nước ngoài_ròng", "KLGD_Nước ngoài_tích lũy", "KLGD", "RS_xếp hạng"]
        try:
            req = d_json_all["stock_foreign_volume"].result()
            df = pd.json_normalize(req["listVolumeForeignInfoDto"])
            df.rename(columns={"ticker": "Mã", "foreignBuy": "KLGD_Nước ngoài_Mua", "foreignSell": "KLGD_Nước ngoài_Bán", "netForeignVol": "KLGD_Nước ngoài_ròng", "dateReport": "Ngày", "accNetFVol": "KLGD_Nước ngoài_tích lũy", "rsRank": "RS_xếp hạng", "totalVolume": "KLGD"}, inplace=True)
            df = df[l_col]
            df['Ngày'] = pd.to_datetime(df['Ngày'], format="%d/%m/%Y")
        except:
            df = pd.DataFrame(columns=l_col)
        return df
    
    df_overview, industry_type = get_df_overview()
    df_dividend = get_df_dividend()
    df_shareholders = get_df_shareholders()
    df_sub_companies = get_df_sub_companies()
    df_audit_firm= get_df_audit_firm()
    df_evaluation_history = get_df_evaluation_history()
    df_stock_indicator = get_df_stock_indicator()
    df_stock_foreign_volume = get_df_stock_foreign_volume()
    return df_overview, industry_type, df_dividend, df_shareholders, df_sub_companies, df_audit_firm, df_evaluation_history, df_stock_indicator, df_stock_foreign_volume
