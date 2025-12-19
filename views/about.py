import streamlit as st
import requests
import toml
import pandas as pd
from lib.setup_background import setup_header_sidebar
from lib.local_path import local_path

# local_path = local_path()

setup_header_sidebar()
# Change CSS styles
with open("styles.css") as f:
    st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)


st.markdown(
    """
<span style="color: #EF10BB;font-weight: bold;">DATAHUK</span> cung cấp trọn bộ dữ liệu chứng khoán
trong các file excel và bộ template phân tích mẫu trên POWERBI. \n

---
🎯 Dữ liệu bao gồm:
- Dữ liệu từng cổ phiếu: tổng quan, lịch sử cổ tức, công ty con, cổ đông, báo cáo tài chính, chỉ số tài chính, chỉ số kĩ thuật cơ bản \n
- Dữ liệu chỉ số VNINDEX, HNXINDEX, UPCOMINDEX \n
- Dữ liệu Ngành: báo cáo tài chính, chỉ số tài chính \n
- Dữ liệu Thị trường và bộ lọc: bộ lọc - dữ liệu toàn bộ các mã về chỉ số tài chính, chỉ số kĩ thuật cơ bản, 
thị trường - dữ liệu chỉ số ngành, độ rộng thị trường, giá trị giao dịch nước ngoài, cung cầu \n
- Dữ liệu Vĩ mô: GDP, CPI, cán cân thương mại, chỉ số sản xuất công nghiệp, FDI, Vốn Ngân sách Nhà nước, vận tải, khách quốc tế,
dân số, thất nghiệp... \n
- Dữ liệu Lãi suât tiền tệ: cung tiền M2, huy động, tín dụng, dự trữ ngoại hối, tỷ giá trung tâm, lãi suất liên ngân hàng \n
- Dữ liệu giá hàng hóa theo lĩnh vực: Tiêu dùng, Hóa chất, Kim loại, Năng lượng, Nhựa - cao su, Vật liệu xây dựng \n
---
🎯 Quý nhà đầu tư tải dữ liệu tại tab 💎 Tải dữ liệu! \n""", unsafe_allow_html=True)

st.markdown("""

- Điền email đã đăng kí, nhấn enter và chọn dữ liệu muốn tải \n
- Chọn nút "Cập nhật dữ liệu", đợi cập nhật xong và ấn Tải dữ liệu \n
👉 Quý NĐT đăng kí trải nghiệm tại: <a href="https://www.facebook.com/datahuk68">@datahuk68</a> hoặc <a href="https://t.me/datahuk_thangtrung">@datahuk_thangtrung</a>
"""
, unsafe_allow_html=True)

# st.image(
#     "img_user_guide/switch_pages.gif"
# )

st.code(
    """
Sơ đồ Data Web-app:
|
|-- 🏠 Trang chủ
|-- 💎 Tải dữ liệu
""", language="python", line_numbers=10
)
