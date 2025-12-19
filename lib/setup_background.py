import streamlit as st



l_social_media_links = [
    "https://www.facebook.com/datahuk68",
    # "https://www.youtube.com/",
    # "https://www.instagram.com/",
    # "https://www.threads.net/"
    ]

def setup_header_sidebar():
    # Config page setting
    st.set_page_config(layout="wide",initial_sidebar_state="expanded",
                        # page_icon='img/logo_Tramdautu_ico.ico',
                        page_title= "DATAHUK")
    
    
    # Navbar
    with st.container():
        st.image(image='img/logo_datahuk_svg.svg', width=100)

    # with st.container():
    #     st.text("DATAHUK")
    
    # # Sidebar
    # # st.sidebar.image('img/logo_Tramdautu_svg.svg',width=40)
    # text_intro = " - platform trực quan hóa các dữ liệu về chứng khoán thị trường Việt Nam"
    # st.sidebar.markdown(f"""<span style="color: #00C256;font-weight: bold;">Trạm Đầu Tư</span>{text_intro}""", unsafe_allow_html=True)
    # st.sidebar.image("img_user_guide/qr_dnse.png",width=120,caption="Quét mã mở TK Chứng khoán tại đây nhé!")
    
    # add social links to sidebar
    st.sidebar.markdown("**Mua dữ liệu tại: 👇**")
    st.sidebar.markdown("🎯 Facebook: "+"""<a href="https://www.facebook.com/datahuk68">@datahuk68</a>""",unsafe_allow_html=True)
    st.sidebar.markdown("🤖 Telegram: "+"""<a href="https://t.me/datahuk_thangtrung">@datahuk_thangtrung</a>""",unsafe_allow_html=True)
    st.sidebar.markdown("---")
    st.sidebar.markdown("**Channel:**")
    st.sidebar.markdown("📢 Telegram: "+"""<a href="https://t.me/chungkhoanmoingay">Chứng khoán mỗi ngày</a>""",unsafe_allow_html=True)

    # # add qr dnse
    # st.sidebar.image("img_user_guide/qr_tpbank.png", width=120, caption="TPBANK-07031518801-TRAN THI TUYET MAI")
    # st.sidebar.markdown("Platform miễn phí nhưng donate tùy tâm nhé anh/chị/em!")