import toml
import streamlit as st
import requests
import toml
import pandas as pd
from concurrent.futures import ThreadPoolExecutor
import time


d_industry_code = {"5300":"Bán lẻ", "8500":"Bảo hiểm", "8600":"Bất động sản",
                   "9500":"Công nghệ Thông tin", "0500":"Dầu khí",
                   "8700":"Dịch vụ tài chính", "7500":"Điện, nước & xăng dầu khí đốt",
                   "5700":"Du lịch và Giải trí", "2700":"Hàng & Dịch vụ Công nghiệp",
                   "3700":"Hàng cá nhân & Gia dụng", "1300":"Hóa chất", 
                   "3300":"Ô tô và phụ tùng", 
                   "1700":"Tài nguyên Cơ bản", "3500":"Thực phẩm và đồ uống","5500":"Truyền thông",
                   "6500":"Viễn thông", "2300":"Xây dựng và Vật liệu", "4500":"Y tế"}
d_industry_code_banking = {"8300": "Ngân hàng"}

api_base_tcbs = st.secrets["api"]["api_base_tcbs"]
auth_tcbs = st.secrets["headers"]["auth_tcbs"]

def get_financial_report_industry_q():

    # get urls
    def get_url(report_type, period_type, d_industry_code):
        l_url = [f'{api_base_tcbs}tcanalysis/v1/finance/industry/{industry_code}/{report_type}?yearly={period_type}' for industry_code in list(d_industry_code.keys())]
        return l_url
    l_url_q_bs = get_url("balancesheet", "0", d_industry_code)
    l_url_q_ic = get_url("incomestatement", "0", d_industry_code)
    l_url_q_cf = get_url("cashflow", "0", d_industry_code)
    l_url_q_ratio = get_url("financialratio", "0", d_industry_code)
    l_url_y_bs = get_url("balancesheet", "1", d_industry_code)
    l_url_y_ic = get_url("incomestatement", "1", d_industry_code)
    l_url_y_cf = get_url("cashflow", "1", d_industry_code)
    l_url_y_ratio = get_url("financialratio", "1", d_industry_code)

    l_url_q_bs_banking = get_url("balancesheet", "0", d_industry_code_banking)
    l_url_q_ic_banking = get_url("incomestatement", "0", d_industry_code_banking)
    l_url_q_ratio_banking = get_url("financialratio", "0", d_industry_code_banking)
    l_url_y_bs_banking = get_url("balancesheet", "1", d_industry_code_banking)
    l_url_y_ic_banking = get_url("incomestatement", "1", d_industry_code_banking)
    l_url_y_ratio_banking = get_url("financialratio", "1", d_industry_code_banking)

    # convert list of url to dict
    d_url_q_bs = {"q_bs":l_url_q_bs}
    d_url_q_ic = {"q_ic":l_url_q_ic}
    d_url_q_cf = {"q_cf":l_url_q_cf}
    d_url_q_ratio = {"q_ratio": l_url_q_ratio}
    
    # d_url_q_bs_banking = {"q_bs_banking":l_url_q_bs_banking}
    # d_url_q_ic_banking = {"q_ic_banking":l_url_q_ic_banking}
    # d_url_q_ratio_banking = {"q_ratio_banking": l_url_q_ratio_banking}
               
    # d_url_y_bs = {"y_bs":l_url_y_bs}
    # d_url_y_ic = {"y_ic":l_url_y_ic}
    # d_url_y_cf = {"y_cf":l_url_y_cf}
    # d_url_y_ratio = {"y_ratio": l_url_y_ratio}
    
    # d_url_y_bs_banking = {"y_bs_banking":l_url_y_bs_banking}
    # d_url_y_ic_banking = {"y_ic_banking":l_url_y_ic_banking}
    # d_url_y_ratio_banking = {"y_ratio_banking": l_url_y_ratio_banking}

    # function: get json
    def get_json(url, headers):
        req = requests.get(url, headers).json()
        time.sleep(2)
        return req

    # enable excecutor
    def get_json_all(d_url, headers):
        executor = ThreadPoolExecutor(100)

        d_json = {key: [] for key in list(d_url.keys())}
        for key_x, l_url in d_url.items():
            futures = []
            for url in l_url:
                try:        
                    future = executor.submit(get_json, (url)(headers))
                    futures.append(future)
                except:
                    pass
            d_json[key_x] = futures
        return d_json

    headers_tcbs = {"Authorization":auth_tcbs}
    d_json_q_bs = get_json_all(d_url_q_bs, headers_tcbs)
    d_json_q_ic = get_json_all(d_url_q_ic, headers_tcbs)
    d_json_q_cf = get_json_all(d_url_q_cf, headers_tcbs)
    d_json_q_ratio = get_json_all(d_url_q_ratio, headers_tcbs)

    # d_json_y_bs = get_json_all(d_url_y_bs)
    # d_json_y_ic = get_json_all(d_url_y_ic)
    # d_json_y_cf = get_json_all(d_url_y_cf)
    # d_json_y_ratio = get_json_all(d_url_y_ratio)    

    # d_json_q_bs_banking = get_json_all(d_url_q_bs_banking)
    # d_json_q_ic_banking = get_json_all(d_url_q_ic_banking)
    # d_json_q_ratio_banking = get_json_all(d_url_q_ratio_banking)

    # d_json_y_bs_banking = get_json_all(d_url_y_bs_banking)
    # d_json_y_ic_banking = get_json_all(d_url_y_ic_banking)
    # d_json_y_ratio_banking = get_json_all(d_url_y_ratio_banking)


    # rename column and sort column
    d_bs = {"quarter": "Quý", "year": "Năm", "shortAsset": "Tài sản ngắn hạn", "cash": "Tiền_tương đương tiền", "shortInvest": "Đầu tư ngắn hạn", "shortReceivable": "Phải thu ngắn hạn", "inventory": "Hàng tồn kho", "longAsset": "Tài sản dài hạn", "fixedAsset": "Tài sản cố định", "asset": "Tổng tài sản", "debt": "Tổng nợ phải trả", "shortDebt": "Vay ngắn hạn", "longDebt": "Vay dài hạn", "equity": "Vốn chủ", "capital": "Vốn điều lệ", "industry": "Ngành"}
    q_l_bs_sort = ["Ngành", "Quý", "Năm", "Tài sản ngắn hạn", "Tiền_tương đương tiền", "Đầu tư ngắn hạn", "Phải thu ngắn hạn", "Hàng tồn kho", "Tài sản dài hạn", "Tài sản cố định", "Tổng tài sản", "Tổng nợ phải trả", "Vay ngắn hạn", "Vay dài hạn", "Vốn chủ", "Vốn điều lệ"]
    d_bs_banking = {"quarter": "Quý", "year": "Năm", "cash": "Tiền_tương đương tiền", "centralBankDeposit": "Tiền gửi tại NHNN", "otherBankDeposit": "Tiền gửi tại các TCTD khác", "otherBankLoan": "Cho vay TCTD khác", "stockInvest": "Chứng khoán đầu tư", "customerLoan": "Cho vay khách hàng", "badLoan": "Nợ xấu", "provision": "Dự phòng cho vay KH", "netCustomerLoan": "Cho vay KH ròng", "fixedAsset": "Tài sản cố định", "payableInterest": "Lãi và phí phải trả", "otherAsset": "Tài sản khác", "asset": "Tổng tài sản", "otherBankCredit": "Tiền gửi của TCTD", "oweOtherBank": "Vay các TCTD", "oweCentralBank": "Nợ CP và NHNN", "deposit": "Tiền gửi khách hàng", "valuablePaper": "Phát hành giấy tờ có giá", "receivableInterest": "Lãi và phí phải thu", "otherDebt": "Nợ phải trả khác", "payable": "Tổng nợ phải trả", "capital": "Vốn điều lệ", "fund": "Quỹ của TCTD", "unDistributedIncome": "Lợi nhuận chưa phân phối", "equity": "Vốn chủ", "minorShareHolderProfit": "Lợi ích CĐkhông  kiểm soát", "industry": "Ngành"}
    q_l_bs_sort_banking = ["Ngành", "Quý", "Năm", "Tiền_tương đương tiền", "Tiền gửi tại NHNN", "Tiền gửi tại các TCTD khác", "Cho vay TCTD khác", "Chứng khoán đầu tư", "Cho vay khách hàng", "Nợ xấu", "Dự phòng cho vay KH", "Cho vay KH ròng", "Tài sản cố định", "Lãi và phí phải thu", "Tài sản khác", "Tổng tài sản", "Tiền gửi của TCTD", "Vay các TCTD", "Nợ CP và NHNN", "Tiền gửi khách hàng", "Phát hành giấy tờ có giá", "Lãi và phí phải trả", "Nợ phải trả khác", "Tổng nợ phải trả", "Vốn điều lệ", "Quỹ của TCTD", "Lợi nhuận chưa phân phối", "Vốn chủ", "Lợi ích CĐkhông  kiểm soát"]

    d_ic = {"quarter": "Quý", "year": "Năm", "revenue": "Doanh thu thuần", "yearRevenueGrowth": "Tăng trưởng Doanh thu cùng kì", "costOfGoodSold": "Giá vốn hàng bán", "grossProfit": "Lợi nhuận gộp", "operationExpense": "Chi phí hoạt động", "operationProfit": "Lợi nhuận hoạt động", "yearOperationProfitGrowth": "Tăng trưởng LN hoạt động", "ebitda": "EBITDA", "interestExpense": "Chi phí lãi vay", "preTaxProfit": "Lợi nhuận trước thuế", "postTaxProfit": "Lợi nhuận sau thuế", "shareHolderIncome": "LNST và cổ đông thiểu số", "yearShareHolderIncomeGrowth": "Tăng trưởng lợi nhuận sau thuế", "industry": "Ngành"}
    q_l_ic_sort = ["Ngành", "Quý", "Năm", "Doanh thu thuần", "Tăng trưởng Doanh thu cùng kì", "Giá vốn hàng bán", "Lợi nhuận gộp", "Chi phí hoạt động", "Lợi nhuận hoạt động", "Tăng trưởng LN hoạt động", "Chi phí lãi vay", "Lợi nhuận trước thuế", "Lợi nhuận sau thuế", "LNST và cổ đông thiểu số", "Tăng trưởng lợi nhuận sau thuế", "EBITDA"]
    d_ic_banking = {"quarter": "Quý", "year": "Năm", "revenue": "Thu nhập lãi thuần", "yearRevenueGrowth": "Tăng trưởng Thu nhập lãi thuần", "operationExpense": "Chi phí hoạt động", "operationProfit": "Tổng thu nhập hoạt động (TOI)", "serviceProfit": "Lãi thuần HĐ dịch vụ", "investProfit": "Lãi thuần HĐ đầu tư", "otherProfit": "Lãi thuần HĐ khác", "provisionExpense": "Chi phí dự phòng", "preTaxProfit": "Lợi nhuận trước thuế", "postTaxProfit": "Lợi nhuận sau thuế", "shareHolderIncome": "LNST và cổ đông thiểu số", "yearShareHolderIncomeGrowth": "Tăng trưởng LNST", "operationIncome": "Lợi nhuận trước dự phòng", "yearOperationProfitGrowth": "Tăng trưởng thu nhập hoạt động", "industry": "Ngành"}
    q_l_ic_sort_banking = ["Ngành", "Quý", "Năm", "Thu nhập lãi thuần", "Tăng trưởng Thu nhập lãi thuần", "Lãi thuần HĐ dịch vụ", "Lãi thuần HĐ đầu tư", "Lãi thuần HĐ khác", "Tổng thu nhập hoạt động (TOI)", "Tăng trưởng thu nhập hoạt động", "Chi phí dự phòng", "Lợi nhuận trước dự phòng", "Chi phí hoạt động", "Lợi nhuận trước thuế", "Lợi nhuận sau thuế", "LNST và cổ đông thiểu số", "Tăng trưởng LNST"]

    d_cf = {"quarter": "Quý", "year": "Năm", "investCost": "Chi phí đầu tư", "fromInvest": "Lưu chuyển từ HĐ đầu tư", "fromFinancial": "Lưu chuyển từ HĐ tài chính", "fromSale": "Lưu chuyển từ HĐ kinh doanh", "industry":"Ngành"}
    q_l_cf_sort = ["Ngành", "Quý", "Năm", "Lưu chuyển từ HĐ kinh doanh", "Lưu chuyển từ HĐ đầu tư", "Lưu chuyển từ HĐ tài chính"]

    d_ratio = {"year": "1_Năm", "priceToEarning": "1_PE", "priceToBook": "1_PB", "roe": "2_ROE", "roa": "2_ROA", "daysReceivable": "4_Số ngày Phải thu", "daysInventory": "4_Số ngày Tồn kho", "daysPayable": "4_Số ngày Phải trả", "ebitOnInterest": "3_EBIT/Chi phí lãi vay", "earningPerShare": "1_EPS", "bookValuePerShare": "1_BVPS", "equityOnTotalAsset": "6_Vốn chủ/Tổng tài sản", "equityOnLiability": "6_Vốn chủ/Nợ", "currentPayment": "4_Chỉ số Thanh toán hiện hành", "quickPayment": "4_Chỉ số Thanh toán nhanh", "grossProfitMargin": "2_Biên Lợi nhuận gộp", "operatingProfitMargin": "2_Biên Lợi nhuận hoạt động", "postTaxMargin": "2_Biên Lợi nhuận ròng", "debtOnEquity": "3_Nợ vay/Vốn chủ", "debtOnAsset": "3_Nợ vay/Tổng tài sản", "debtOnEbitda": "3_Nợ vay/EBITDA", "shortOnLongDebt": "3_Nợ ngắn hạn/dài hạn", "assetOnEquity": "6_Tài sản/Vốn chủ", "cashOnEquity": "3_Tiền mặt/Vốn chủ", "revenueOnWorkCapital": "5_Vòng quay Vốn lưu động", "capexOnFixedAsset": "5_CAPEX/Tài sản cố định", "badDebtPercentage": "4_NH_Tỷ lệ Nợ xấu", "interestMargin": "2_NH_Biên lãi thuần", "provisionOnBadDebt": "4_NH_Tỷ lệ Bao phủ nợ xấu", "equityOnLoan": "5_NH_Tỷ lệ Vốn chủ/Cho vay", "costToIncome": "2_NH_COI_Chi phí hoạt động/TOI", "loanOnAsset": "3_NH_Cho vay/Tổng tài sản", "loanOnDeposit": "3_NH_LDR_Cho vay/Tiền gửi", "depositOnEarnAsset": "3_NH_Tiền gửi/Tiền sản sinh lãi", "badDebtOnAsset": "4_NH_Nợ xấu/Tổng tài sản", "ebitdaOnStock": "1_EBITDA/CP", "cashOnCapitalize": "3_Tiền mặt/Vốn hóa", "postTaxOnPreTax": "6_LNST/LNTT", "preTaxOnEbit": "6_LNTT/EBIT", "ebitOnRevenue": "6_EBIT/Doanh thu thuần", "revenueOnAsset": "5_Vòng quay Tài sản", "epsChange": "1_Thay đổi_EPS", "ebitdaOnStockChange": "1_Thay đổi_EBITDA/CP", "bookValuePerShareChange": "1_Thay đổi_BVPS", "nonInterestOnToi": "2_NH_Thu nhập ngoài lãi/TOI", "costOfFinancing": "2_NH_Chi phí vốn", "preProvisionOnToi": "2_NH_LN trước dự phòng/TOI", "postTaxOnToi": "2_NH_LN sau thuế/TOI", "loanOnEarnAsset": "3_NH_Cho vay/Tài sản sinh lãi", "cancelDebt": "4_NH_Tỷ lệ xóa nợ", "liquidityOnLiability": "5_NH_Tài sản thanh khoản/Nợ phải trả", "payableOnEquity": "5_Nợ phải trả/Vốn chủ", "quarter": "1_Quý", "industry": "Ngành"}
    q_l_ratio_sort = ["Ngành", "1_Năm", "1_Quý", "1_BVPS", "1_EBITDA/CP", "1_EPS", "1_PB", "1_PE", "1_Thay đổi_BVPS", "1_Thay đổi_EBITDA/CP", "1_Thay đổi_EPS", "2_Biên Lợi nhuận gộp", "2_Biên Lợi nhuận hoạt động", "2_Biên Lợi nhuận ròng", "2_NH_Biên lãi thuần", "2_NH_COI_Chi phí hoạt động/TOI", "2_NH_Chi phí vốn", "2_NH_LN sau thuế/TOI", "2_NH_LN trước dự phòng/TOI", "2_NH_Thu nhập ngoài lãi/TOI", "2_ROA", "2_ROE", "3_EBIT/Chi phí lãi vay", "3_NH_Cho vay/Tài sản sinh lãi", "3_NH_Cho vay/Tổng tài sản", "3_NH_LDR_Cho vay/Tiền gửi", "3_NH_Tiền gửi/Tiền sản sinh lãi", "3_Nợ ngắn hạn/dài hạn", "3_Nợ vay/EBITDA", "3_Nợ vay/Tổng tài sản", "3_Nợ vay/Vốn chủ", "3_Tiền mặt/Vốn chủ", "3_Tiền mặt/Vốn hóa", "4_Chỉ số Thanh toán hiện hành", "capitalBalance", "4_Chỉ số Thanh toán nhanh", "4_NH_Nợ xấu/Tổng tài sản", "4_NH_Tỷ lệ Bao phủ nợ xấu", "4_NH_Tỷ lệ Nợ xấu", "4_NH_Tỷ lệ xóa nợ", "4_Số ngày Phải thu", "4_Số ngày Phải trả", "4_Số ngày Tồn kho", "5_CAPEX/Tài sản cố định", "5_NH_Tài sản thanh khoản/Nợ phải trả", "5_NH_Tỷ lệ Vốn chủ/Cho vay", "5_Nợ phải trả/Vốn chủ", "5_Vòng quay Tài sản", "5_Vòng quay Vốn lưu động", "6_EBIT/Doanh thu thuần", "6_LNST/LNTT", "6_LNTT/EBIT", "6_Tài sản/Vốn chủ", "6_Vốn chủ/Nợ", "6_Vốn chủ/Tổng tài sản"]
    d_ratio_banking = d_ratio
    q_l_ratio_sort_banking = q_l_ratio_sort

    def remove_quarter(l):
        return [x for x in l if x not in  ["Quý", "1_Quý"]]

    y_l_bs_sort = remove_quarter(q_l_bs_sort)
    y_l_bs_sort_banking = remove_quarter(q_l_bs_sort_banking)
    y_l_ic_sort = remove_quarter(q_l_ic_sort)
    y_l_ic_sort_banking = remove_quarter(q_l_ic_sort_banking)
    y_l_cf_sort = remove_quarter(q_l_cf_sort)
    y_l_ratio_sort = remove_quarter(q_l_ratio_sort)
    y_l_ratio_sort_banking = remove_quarter(q_l_ratio_sort_banking)


    # function: get df from json
    def get_df(d_json, report_type, d_industry_code, d_col, l_col):
        try:
            l_result = [i.result() for i in d_json[report_type]]
            result_flat = [i for sublist in l_result for i in sublist]
            
            df_result = pd.json_normalize(result_flat)
            df_result["ticker"]=df_result["ticker"].astype("str")
            df_result["industry"] = df_result["ticker"].apply(lambda x: d_industry_code[x])

            df_result.rename(columns=d_col, inplace=True)
            df_result = df_result[l_col]
        except:
            df_result = pd.DataFrame()
        return df_result
    
    # get all df
    df_q_bs = get_df(d_json_q_bs, "q_bs", d_industry_code, d_bs, q_l_bs_sort)
    df_q_ic = get_df(d_json_q_ic, "q_ic", d_industry_code, d_ic, q_l_ic_sort)
    df_q_cf = get_df(d_json_q_cf, "q_cf", d_industry_code, d_cf, q_l_cf_sort)
    df_q_ratio = get_df(d_json_q_ratio, "q_ratio", d_industry_code, d_ratio, q_l_ratio_sort)

    # df_y_bs = get_df(d_json_y_bs, "y_bs", d_industry_code, d_bs, y_l_bs_sort)
    # df_y_ic = get_df(d_json_y_ic, "y_ic", d_industry_code, d_ic, y_l_ic_sort)
    # df_y_cf = get_df(d_json_y_cf, "y_cf", d_industry_code, d_cf, y_l_cf_sort)
    # df_y_ratio = get_df(d_json_y_ratio, "y_ratio", d_industry_code, d_ratio, y_l_ratio_sort)

    # df_q_bs_banking = get_df(d_json_q_bs_banking, "q_bs_banking", d_industry_code_banking, d_bs_banking, q_l_bs_sort_banking)
    # df_q_ic_banking = get_df(d_json_q_ic_banking, "q_ic_banking", d_industry_code_banking, d_ic_banking, q_l_ic_sort_banking)
    # df_q_ratio_banking = get_df(d_json_q_ratio_banking, "q_ratio_banking", d_industry_code_banking, d_ratio_banking, q_l_ratio_sort_banking)

    # df_y_bs_banking = get_df(d_json_y_bs_banking, "y_bs_banking", d_industry_code_banking, d_bs_banking, y_l_bs_sort_banking)
    # df_y_ic_banking = get_df(d_json_y_ic_banking, "y_ic_banking", d_industry_code_banking, d_ic_banking, y_l_ic_sort_banking)
    # df_y_ratio_banking = get_df(d_json_y_ratio_banking, "y_ratio_banking", d_industry_code_banking, d_ratio_banking, y_l_ratio_sort_banking)
    return df_q_bs, df_q_ic, df_q_cf, df_q_ratio
