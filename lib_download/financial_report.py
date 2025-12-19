import toml
import streamlit as st
import requests
import toml
import pandas as pd
from lib.setup_background import setup_header_sidebar
from lib.local_path import local_path
import io
import time
from concurrent.futures import ThreadPoolExecutor

# local_path = local_path()

# local secrets
# secrets = toml.load(local_path + ".streamlit/secrets.toml")
url_cus = st.secrets["api"]["url_cus"]
api_industry = st.secrets["api"]["api_industry"]
api_base_mas = st.secrets["api"]["api_base_mas"]
api_base_tcbs = st.secrets["api"]["api_base_tcbs"]
api_base_vci = st.secrets["api"]["api_base_vci"]
auth_tcbs = st.secrets["headers"]["auth_tcbs"]

# function: get json
def get_json(url, headers):
    req = requests.get(url, headers=headers).json()
    time.sleep(2)
    return req

def get_json_all(d_url, headers):
    executor = ThreadPoolExecutor(100)

    d_json = {key: [] for key in list(d_url.keys())}
    for key_x, url in d_url.items():
        try:
            future = executor.submit(get_json, (url, headers))
            d_json[key_x] = future
        except:
            pass
    return d_json

# Financial report
def get_financial_report(ticker):
    def get_json(url, headers):
        req = requests.get(url, headers=headers).json()
        time.sleep(2)
        return req
    
    headers = {
    "Accept": "application/json",
    "Accept-Encoding": "gzip, deflate, br, zstd",
    "Accept-Language": "en-US,en;q=0.9",
    "Cache-Control": "no-cache",
    "Connection": "keep-alive",
    "Host": "iq.vietcap.com.vn",
    "Origin": "https://trading.vietcap.com.vn",
    "Pragma": "no-cache",
    "Referer": "https://trading.vietcap.com.vn/",
    "Sec-CH-UA": '"Not)A;Brand";v="8", "Chromium";v="138", "Microsoft Edge";v="138"',
    "Sec-CH-UA-Mobile": "?0",
    "Sec-CH-UA-Platform": '"Windows"',
    "Sec-Fetch-Dest": "empty",
    "Sec-Fetch-Mode": "cors",
    "Sec-Fetch-Site": "same-site",
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36 Edg/138.0.0.0"
    }
    l_report_type = ['BALANCE_SHEET', 'INCOME_STATEMENT', 'CASH_FLOW']
    
    def get_metrics(ticker):
        url = f"https://iq.vietcap.com.vn/api/iq-insight-service/v1/company/{ticker}/financial-statement/metrics"
        json_metrics = get_json(url, headers)['data']
        df_metrics_bs = pd.DataFrame(json_metrics['BALANCE_SHEET'])
        df_metrics_ic = pd.DataFrame(json_metrics['INCOME_STATEMENT'])
        df_metrics_cf = pd.DataFrame(json_metrics['CASH_FLOW'])
        df_metrics_note = pd.DataFrame(json_metrics['NOTE'])
        df_metrics = pd.concat([df_metrics_bs, df_metrics_ic, df_metrics_cf, df_metrics_note])
        df_metrics["field_sort"] = df_metrics.index
        return df_metrics[["field", "field_sort","fullTitleEn", "fullTitleVi"]]
    df_metrics = get_metrics(ticker)
    
    json_all = {}
    for report_type in l_report_type:
        url = f"{api_base_vci}company/{ticker}/financial-statement?section={report_type}"
        json_report = get_json(url, headers)["data"]
        json_all[report_type] = {'years': json_report['years'], 'quarters': json_report['quarters']}
        time.sleep(2)

    def get_df(json_all,report_type, period_type):
        d_column = {"years": ["Mã", "Năm", "Chỉ số", "Chỉ số_en", "Giá trị_tỷ đồng"],
                    "quarters": ["Mã", "Năm", "Quý", "Chỉ số", "Chỉ số_en", "Giá trị_tỷ đồng"]}
        
        df_report = pd.DataFrame(json_all[report_type][period_type])

        df_melt = df_report.melt(id_vars=['organCode', 'ticker', 'createDate',
                                          'updateDate', 'yearReport', 'lengthReport',
                                          'publicDate'], var_name='field')

        df_result = df_melt.merge(df_metrics, on="field", how="left")
        df_sub = df_result[["ticker", "yearReport", "lengthReport", 
                            "field_sort", "fullTitleVi", "fullTitleEn", "value"]]
        df_sub = df_sub.dropna().copy()
        df_sub["value"] = df_sub["value"].apply(lambda x: x/pow(10,9))
        df_sort = df_sub.sort_values(by=['yearReport', 'lengthReport', 'field_sort'], 
                                     ascending=[False, False, True])        
        df_sort.rename(columns={"ticker":"Mã", "yearReport":"Năm", "lengthReport":"Quý", 
                                "fullTitleVi": "Chỉ số", "fullTitleEn":"Chỉ số_en",
                                "value":"Giá trị_tỷ đồng"}, inplace=True)
        df_result = df_sort[d_column[period_type]].copy()
        return df_result
    
    df_q_bs = get_df(json_all, "BALANCE_SHEET", "quarters")
    df_q_ic = get_df(json_all, "INCOME_STATEMENT", "quarters")
    df_q_cf = get_df(json_all, "CASH_FLOW", "quarters")
    df_y_bs = get_df(json_all, "BALANCE_SHEET", "years")
    df_y_ic = get_df(json_all, "INCOME_STATEMENT", "years")
    df_y_cf = get_df(json_all, "CASH_FLOW", "years")
    
    return df_q_bs, df_q_ic, df_q_cf, df_y_bs, df_y_ic, df_y_cf

# Financial Ratio
def get_financial_ratio(ticker):
    def get_url(ticker):
        d_is_year={"0":"q_ratio", "1":"y_ratio"}
        d_url = {}
        for is_year in ["0", "1"]:
            period_type = d_is_year[is_year]
            url = f'{api_base_tcbs}tcanalysis/v1/finance/{ticker}/financialratio?yearly={is_year}&isAll=True'
            d_url[period_type] = url
        return d_url
    
    d_url = get_url(ticker)

    headers_tcbs = {
        "Accept": "application/json",
        "Accept-Language": "vi",
        "Authorization":auth_tcbs, 
        "Content-Type":"application/json",
        "Referer":"https://tcinvest.tcbs.com.vn/",
        "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/143.0.0.0 Safari/537.36 Edg/143.0.0.0"
    }
    d_json_all = {key: get_json(d_url[key], headers_tcbs) for key in list(d_url.keys())}

    def get_df(report):
        period_type = report[0:1]
        try:
            req=d_json_all[report]
            df = pd.json_normalize(req)
            df.rename(columns={"ticker": "1_Mã", "year": "1_Năm", "priceToEarning": "1_PE", "priceToBook": "1_PB", "roe": "2_ROE", "roa": "2_ROA", "daysReceivable": "4_Số ngày Phải thu", "daysInventory": "4_Số ngày Tồn kho", "daysPayable": "4_Số ngày Phải trả", "ebitOnInterest": "3_EBIT/Chi phí lãi vay", "earningPerShare": "1_EPS", "bookValuePerShare": "1_BVPS", "equityOnTotalAsset": "6_Vốn chủ/Tổng tài sản", "equityOnLiability": "6_Vốn chủ/Nợ", "currentPayment": "4_Chỉ số Thanh toán hiện hành", "quickPayment": "4_Chỉ số Thanh toán nhanh", "grossProfitMargin": "2_Biên Lợi nhuận gộp", "operatingProfitMargin": "2_Biên Lợi nhuận hoạt động", "postTaxMargin": "2_Biên Lợi nhuận ròng", "debtOnEquity": "3_Nợ vay/Vốn chủ", "debtOnAsset": "3_Nợ vay/Tổng tài sản", "debtOnEbitda": "3_Nợ vay/EBITDA", "shortOnLongDebt": "3_Nợ ngắn hạn/dài hạn", "assetOnEquity": "6_Tài sản/Vốn chủ", "cashOnEquity": "3_Tiền mặt/Vốn chủ", "revenueOnWorkCapital": "5_Vòng quay Vốn lưu động", "capexOnFixedAsset": "5_CAPEX/Tài sản cố định", "badDebtPercentage": "4_NH_Tỷ lệ Nợ xấu", "interestMargin": "2_NH_Biên lãi thuần", "provisionOnBadDebt": "4_NH_Tỷ lệ Bao phủ nợ xấu", "equityOnLoan": "5_NH_Tỷ lệ Vốn chủ/Cho vay", "costToIncome": "2_NH_COI_Chi phí hoạt động/TOI", "loanOnAsset": "3_NH_Cho vay/Tổng tài sản", "loanOnDeposit": "3_NH_LDR_Cho vay/Tiền gửi", "depositOnEarnAsset": "3_NH_Tiền gửi/Tiền sản sinh lãi", "badDebtOnAsset": "4_NH_Nợ xấu/Tổng tài sản", "ebitdaOnStock": "1_EBITDA/CP", "cashOnCapitalize": "3_Tiền mặt/Vốn hóa", "postTaxOnPreTax": "6_LNST/LNTT", "preTaxOnEbit": "6_LNTT/EBIT", "ebitOnRevenue": "6_EBIT/Doanh thu thuần", "revenueOnAsset": "5_Vòng quay Tài sản", "epsChange": "1_Thay đổi_EPS", "ebitdaOnStockChange": "1_Thay đổi_EBITDA/CP", "bookValuePerShareChange": "1_Thay đổi_BVPS", "nonInterestOnToi": "2_NH_Thu nhập ngoài lãi/TOI", "costOfFinancing": "2_NH_Chi phí vốn", "preProvisionOnToi": "2_NH_LN trước dự phòng/TOI", "postTaxOnToi": "2_NH_LN sau thuế/TOI", "loanOnEarnAsset": "3_NH_Cho vay/Tài sản sinh lãi", "cancelDebt": "4_NH_Tỷ lệ xóa nợ", "liquidityOnLiability": "5_NH_Tài sản thanh khoản/Nợ phải trả", "payableOnEquity": "5_Nợ phải trả/Vốn chủ", "quarter": "1_Quý"}, inplace=True)
            df = df[sorted(df.columns)]
            df = df[['1_Mã', '1_Năm', '1_Quý'] + [col for col in df.columns if col not in ['1_Mã', '1_Năm', '1_Quý']]]

            
            if period_type == "y":
                df.drop(["1_Quý"], axis=1, inplace=True)
            df.drop(["capitalBalance", "cashCirculation", "creditGrowth", "dividend", "valueBeforeEbitda"], axis=1, inplace=True)
        except:
            l_col = ["1_Mã","1_Năm","1_BVPS","1_EBITDA/CP","1_EPS","1_PB","1_PE","1_Thay đổi_BVPS","1_Thay đổi_EBITDA/CP","1_Thay đổi_EPS","2_Biên Lợi nhuận gộp","2_Biên Lợi nhuận hoạt động","2_Biên Lợi nhuận ròng","2_NH_Biên lãi thuần","2_NH_COI_Chi phí hoạt động/TOI","2_NH_Chi phí vốn","2_NH_LN sau thuế/TOI","2_NH_LN trước dự phòng/TOI","2_NH_Thu nhập ngoài lãi/TOI","2_ROA","2_ROE","3_EBIT/Chi phí lãi vay","3_NH_Cho vay/Tài sản sinh lãi","3_NH_Cho vay/Tổng tài sản","3_NH_LDR_Cho vay/Tiền gửi","3_NH_Tiền gửi/Tiền sản sinh lãi","3_Nợ ngắn hạn/dài hạn","3_Nợ vay/EBITDA","3_Nợ vay/Tổng tài sản","3_Nợ vay/Vốn chủ","3_Tiền mặt/Vốn chủ","3_Tiền mặt/Vốn hóa","4_Chỉ số Thanh toán hiện hành","4_Chỉ số Thanh toán nhanh","4_NH_Nợ xấu/Tổng tài sản","4_NH_Tỷ lệ Bao phủ nợ xấu","4_NH_Tỷ lệ Nợ xấu","4_NH_Tỷ lệ xóa nợ","4_Số ngày Phải thu","4_Số ngày Phải trả","4_Số ngày Tồn kho","5_CAPEX/Tài sản cố định","5_NH_Tài sản thanh khoản/Nợ phải trả","5_NH_Tỷ lệ Vốn chủ/Cho vay","5_Nợ phải trả/Vốn chủ","5_Vòng quay Tài sản","5_Vòng quay Vốn lưu động","6_EBIT/Doanh thu thuần","6_LNST/LNTT","6_LNTT/EBIT","6_Tài sản/Vốn chủ","6_Vốn chủ/Nợ","6_Vốn chủ/Tổng tài sản"]
            if period_type == "y":
                l_col_result=l_col
            else:
                l_col_result=l_col+["1_Quý"]
            df = pd.DataFrame(columns=l_col_result)
        return df


    df_q_ratio = get_df("q_ratio")
    df_y_ratio = get_df("y_ratio")
    return df_q_ratio, df_y_ratio