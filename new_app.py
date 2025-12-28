import streamlit as st
import pandas as pd
import streamlit.components.v1 as components

# ۱. تنظیمات صفحه
st.set_page_config(page_title="واحد رامسر", page_icon="🏫", layout="wide")

# ۲. بخش CSS برای استایل‌دهی به محیط Streamlit
st.markdown("""
    <style>
    [data-testid="stHeader"] {display: none;}
    #MainMenu {visibility: hidden;}
    .stAppDeployButton {display: none;}
    footer {visibility: hidden;}
    .stApp { background-color: #050a14; direction: rtl; }
    
    /* استایل کادر فیلترها */
    [data-testid="stVerticalBlockBorderWrapper"] > div:nth-child(1) {
        background-color: #060d1a !important;
        border: 2px solid #64ffda !important;
        border-radius: 20px !important;
        padding: 40px !important;
        margin: 20px auto !important;
        max-width: 850px !important;
    }

    h1, h2, h3, label, p { color: white !important; text-align: center !important; }

    div.stButton > button {
        background-color: transparent !important;
        color: #64ffda !important;
        border: 2px solid #64ffda !important;
        width: 100% !important;
        border-radius: 12px !important;
        height: 50px !important;
    }
    
    .footer {
        position: fixed; left: 0; bottom: 0; width: 100%;
        background-color: #050a14; color: #64ffda;
        text-align: center; padding: 12px 0; font-size: 13px;
        border-top: 1px solid rgba(100, 255, 218, 0.1);
    }
    </style>
    """, unsafe_allow_html=True)

# ۳. هدر
st.markdown("<h1 style='color: #64ffda !important;'>دانشگاه آزاد اسلامی واحد رامسر</h1>", unsafe_allow_html=True)
st.markdown("<p style='margin-bottom: 30px;'>سامانه هوشمند جستجوی برنامه کلاسی اساتید</p>", unsafe_allow_html=True)

# ۴. بارگذاری داده‌ها
try:
    df = pd.read_excel("schedule.xlsx")
    df = df.astype(str)
except Exception as e:
    st.error(f"خطا در خواندن فایل اکسل: {e}")
    st.stop()

def clean_time(time_str):
    if ':' in str(time_str):
        parts = str(time_str).strip().split(':')
        if len(parts) >= 2: return f"{parts[0]}:{parts[1]}"
    return time_str

# ۵. فیلترها
with st.container(border=True):
    col1, col2 = st.columns(2)
    with col1:
        lessons = ['-- انتخاب درس --'] + sorted(df['نام درس'].unique().tolist())
        sel_lesson = st.selectbox("📚 نام درس:", lessons)
    with col2:
        profs = ['-- انتخاب استاد --'] + sorted(df['نام استاد'].unique().tolist())
        sel_prof = st.selectbox("👨‍🏫 نام استاد:", profs)
    
    btn_col1, btn_col2 = st.columns(2)
    with btn_col1:
        search_clicked = st.button("🔍 جستجوی برنامه")
    with btn_col2:
        if st.button("♻️ پاکسازی فیلترها"): st.rerun()

# ۶. نمایش نتایج با استفاده از Component HTML
if search_clicked:
    if sel_lesson.startswith('--') and sel_prof.startswith('--'):
        st.warning("⚠️ لطفاً حداقل یکی از فیلترها را انتخاب کنید.")
    else:
        query = df.copy()
        if not sel_lesson.startswith('--'):
            query = query[query['نام درس'] == sel_lesson]
        if not sel_prof.startswith('--'):
            query = query[query['نام استاد'] == sel_prof]
        
        if not query.empty:
            st.markdown("<h3 style='color: #64ffda !important;'>📋 لیست کلاس‌ها:</h3>", unsafe_allow_html=True)
            
            table_rows = ""
            for i, row in query.reset_index(drop=True).iterrows():
                table_rows += f"""
                <tr>
                    <td>{i+1}</td>
                    <td>{row['نام درس']}</td>
                    <td>{row['روز']}</td>
                    <td>{clean_time(row['زمان شروع'])}</td>
                    <td>{row['شماره کلاس']}</td>
                </tr>
                """
            
            # طراحی کامل جدول در قالب یک رشته HTML واحد
            final_html_code = f"""
            <div style="direction: rtl; font-family: Tahoma, Arial; padding: 10px;">
                <table style="width: 100%; border-collapse: collapse; background-color: #0f1b2a; color: white; border-radius: 15px; overflow: hidden; box-shadow: 0 4px 20px rgba(100, 255, 218, 0.15);">
                    <thead>
                        <tr style="background-color: #64ffda; color: black;">
                            <th style="padding: 15px;">ردیف</th>
                            <th style="padding: 15px;">نام درس</th>
                            <th style="padding: 15px;">روز</th>
                            <th style="padding: 15px;">زمان کلاس</th>
                            <th style="padding: 15px;">شماره کلاس</th>
                        </tr>
                    </thead>
                    <tbody style="text-align: center;">
                        {table_rows}
                    </tbody>
                </table>
                <style>
                    td {{ padding: 12px; border-bottom: 1px solid rgba(100,255,218,0.1); }}
                    tr:last-child td {{ border-bottom: none; }}
                </style>
            </div>
            """
            # استفاده از components.html برای رندر قطعی و بدون نمایش کد
            components.html(final_html_code, height=400, scrolling=True)
        else:
            st.info("😔 کلاسی پیدا نشد.")

st.markdown('<div class="footer">Design & Development by: AHB | ۲۰۲۵</div>', unsafe_allow_html=True)