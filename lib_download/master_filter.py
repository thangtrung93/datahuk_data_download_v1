import streamlit as st
import requests
import pandas as pd
from datetime import datetime, timedelta

url_master_filter = st.secrets["api"]["url_master_filter"]

d_col = {"ticker": "0_Mã", "date": "0_Ngày", "marketCap": "1_Vốn hóa_tỷ đồng", "roe": "2_ROE", "activeBuyPercentage": "5_Phần trăm mua chủ động", "pe": "2_PE", "pb": "2_PB", "evEbitda": "2_EV/EBITDA", "alpha": "1_alpha", "beta": "1_beta", "priceNearRealtime": "1_Thị giá", "freeTransferRate": "1_Tỷ lệ chuyển nhượng tự do", "dividendYield": "2_Tỷ suất cổ tức", "grossMargin": "2_Biên lợi nhuận gộp", "netMargin": "2_Biên lợi nhuận ròng", "doe": "2_DOE", "eps": "2_EPS", "netCashPerMarketCap": "2_Tiền mặt ròng/Vốn hóa", "netCashPerTotalAssets": "2_Tiền mặt ròng/Tài sản", "profitForTheLast4Quarters": "2_Lợi nhuận 4 quý gần nhất", "revenueGrowth1Year": "3_Tăng trưởng Doanh thu 1 năm_%", "revenueGrowth5Year": "3_Tăng trưởng Doanh thu 5 năm_%", "epsGrowth1Year": "3_Tăng trưởng EPS 1 năm_%", "epsGrowth5Year": "3_Tăng trưởng EPS 5 năm_%", "lastQuarterRevenueGrowth": "3_Tăng trưởng Doanh thu Quý gần nhất", "secondQuarterRevenueGrowth": "3_Tăng trưởng Doanh thu Quý gần nhì", "lastQuarterProfitGrowth": "3_Tăng trưởng Lợi nhuận Quý gần nhất", "secondQuarterProfitGrowth": "3_Tăng trưởng Lợi nhuận Quý gần nhì", "avgTradingValue5Day": "4_Giá trị giao dịch TB 5 ngày", "avgTradingValue10Day": "4_Giá trị giao dịch TB 10 ngày", "avgTradingValue20Day": "4_Giá trị giao dịch TB 20 ngày", "volumeVsVSma5": "4_Khối lượng so với SMA 5", "volumeVsVSma10": "4_Khối lượng so với SMA 10", "volumeVsVSma20": "4_Khối lượng so với SMA 20", "volumeVsVSma50": "4_Khối lượng so với SMA 50", "priceGrowth1Week": "4_Thay đổi giá 1 tuần", "priceGrowth1Month": "4_Thay đổi giá 1 tháng", "percent1YearFromPeak": "4_Phần trăm cách đỉnh trong năm gần nhất", "percentAwayFromHistoricalPeak": "4_Phần trăm cách đỉnh lịch sử", "percent1YearFromBottom": "4_Phần trăm so với đáy trong năm gần nhất", "percentOffHistoricalBottom": "4_Phần trăm so với đáy lịch sử", "priceVsSMA5.vi": "4_Giá vs SMA 5", "priceVsSMA20.vi": "4_Giá vs SMA 20", "priceVsSma10.vi": "4_Giá vs SMA 10", "priceVsSma50.vi": "4_Giá vs SMA 50", "priceVsSMA100.vi": "4_Giá vs SMA 100", "numIncreaseContinuousDay": "5_Số phiên giá tăng liên tiếp", "numDecreaseContinuousDay": "5_Số phiên giảm giá liên tiếp", "exchangeName.vi": "1_Sàn", "industryName.vi": "1_Ngành", "rsi14": "6_RSI 14", "relativeStrength3Day": "6_RS 3 ngày", "relativeStrength1Month": "6_RS 1 tháng", "relativeStrength3Month": "6_RS 3 tháng", "relativeStrength1Year": "6_RS 1 năm", "macdHistogram.vi": "6_MACD Histogram", "rsi14Status.vi": "6_Trạng thái RSI 14", "foreignTransaction.vi": "4_Lực mua bán Khối ngoại", "heatingUp.vi": "7_Tăng giá nóng", "priceBreakOut52Week.vi": "7_Tín hiệu phá đỉnh giá 52 tuần", "sarVsMacdHist.vi": "7_Tín hiệu SAR_MACD histogram", "dmiSignal.vi": "7_Tín hiệu DMI", "bollingBandSignal.vi": "7_Tín hiệu Bolling Band", "suddenlyHighVolumeMatching": "4_Đột biến Khối lượng"}
l_col_sort = list(d_col.values())
l_col_sort.sort()

def get_master_filter():
    df = pd.read_csv(url_master_filter)
    df = df.rename(columns=df.iloc[0]).drop(df.index[0])
    df.rename(columns = d_col, inplace=True)
    if "7_Tín hiệu phá đỉnh giá 52 tuần" not in df.columns.to_list():
        df["7_Tín hiệu phá đỉnh giá 52 tuần"]=""
    df_master_filter = df[l_col_sort]
    for col in l_col_sort:
        try:
            df_master_filter[col]= df_master_filter[col].astype(float)
        except:
            pass

    df_stock = df_master_filter[["0_Mã", "1_Ngành", "1_Sàn"]].copy()
    df_stock.rename(columns = {"0_Mã": "Mã","1_Ngành":"Ngành", "1_Sàn":"Sàn"}, inplace=True)
    return df_stock, df_master_filter
