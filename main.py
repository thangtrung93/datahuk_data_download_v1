import streamlit as st

pg=st.navigation(
    [
        st.Page("views/about.py", title="Trang chủ", icon ="🏠",default=True),
        st.Page("views/data_download.py", title="Tải dữ liệu", icon="💎"),
    ]
)

pg.run()