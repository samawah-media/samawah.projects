import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from data_manager import DataManager
from datetime import datetime
import time
import base64
import os
from streamlit_option_menu import option_menu

# --- Samawah Brand Color Palette ---
SAMAWAH_NAVY = "#062759"      # Primary Dark
SAMAWAH_TEAL = "#118791"      # Primary Teal
SAMAWAH_MINT = "#97D3CB"      # Soft Teal
SAMAWAH_ORANGE = "#FEB25D"    # Accent Orange
SAMAWAH_SALMON = "#FE6D6A"    # Soft Red
SAMAWAH_RED = "#EA4355"       # Primary Red
SAMAWAH_BG = "#F7F5F0"        # Main Background
SAMAWAH_TEXT = "#414042"      # Primary Text

# --- Page Configuration ---
st.set_page_config(
    page_title="مشاريع سماوة",
    page_icon="https://res.cloudinary.com/dg4pnw73t/image/upload/v1768640793/%D9%84%D9%88%D8%AC%D9%88_%D8%B3%D9%85%D8%A7%D9%88%D8%A9_qrui2s.png",
    layout="wide",
    initial_sidebar_state="collapsed",
    menu_items={
        'About': "إدارة المشاريع الداخلية والخارجية - سماوة"
    }
)

# --- Open Graph / Meta Tags Injection ---
st.markdown("""
    <style>div.stButton > button:first-child {background-color: #062759; color: white;}</style>
    <meta property="og:image" content="https://res.cloudinary.com/dg4pnw73t/image/upload/v1768640793/%D9%84%D9%88%D8%AC%D9%88_%D8%B3%D9%85%D8%A7%D9%88%D8%A9_qrui2s.png">
    <meta property="og:title" content="مشاريع سماوة">
    <meta property="og:description" content="إدارة المشاريع الداخلية والخارجية">
""", unsafe_allow_html=True)

# --- AUTHENTICATION ---
def check_password():
    """Returns `True` if the user had a correct password."""

    def password_entered():
        """Checks whether a password entered by the user is correct."""
        if st.session_state["password"] in st.secrets["passwords"].values():
            st.session_state["password_correct"] = True
            # Store the username based on password (optional logic)
            del st.session_state["password"]  # don't store password
        else:
            st.session_state["password_correct"] = False

    if "password_correct" not in st.session_state:
        # First run, show input for password
        st.markdown(f"""
        <style>
        .stApp {{ background-color: #F7F5F0; }}
        </style>
        """, unsafe_allow_html=True)
        
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.image("https://res.cloudinary.com/dg4pnw73t/image/upload/v1768640793/%D9%84%D9%88%D8%AC%D9%88_%D8%B3%D9%85%D8%A7%D9%88%D8%A9_qrui2s.png", width=150)
            st.title("بوابة مشاريع سماوة")
            st.text_input(
                "يرجى إدخال رمز الدخول", type="password", on_change=password_entered, key="password"
            )
            st.caption("🔒 هذا النظام خاص بموظفي سماوة فقط")
        return False
        
    elif not st.session_state["password_correct"]:
        # Password validation error
        col1, col2, col3 = st.columns([1, 2, 1])
        with col2:
            st.markdown("<br><br>", unsafe_allow_html=True)
            st.image("https://res.cloudinary.com/dg4pnw73t/image/upload/v1768640793/%D9%84%D9%88%D8%AC%D9%88_%D8%B3%D9%85%D8%A7%D9%88%D8%A9_qrui2s.png", width=150)
            st.title("بوابة مشاريع سماوة")
            st.text_input(
                "يرجى إدخال رمز الدخول", type="password", on_change=password_entered, key="password"
            )
            st.error("😕 رمز الدخول غير صحيح")
        return False
    else:
        # Password correct
        return True

if not check_password():
    st.stop()

# --- Custom Branded Fonts Loading ---
def get_base64_font(font_path):
    with open(font_path, "rb") as f:
        data = f.read()
    return base64.b64encode(data).decode()

# Font paths (using relative paths for deployment)
current_dir = os.path.dirname(os.path.abspath(__file__))
# The fonts are outside the samawah_pmis folder in the root directory
fonts_dir = os.path.join(os.path.dirname(current_dir), "fonts")

# Fallback in case the structure changes during deployment
if not os.path.exists(fonts_dir):
    fonts_dir = os.path.join(current_dir, "fonts")

font_bold = os.path.join(fonts_dir, "samawah-bold.ttf")
font_medium = os.path.join(fonts_dir, "samawah-medium.ttf")
font_regular = os.path.join(fonts_dir, "samawah-regular.ttf")

try:
    b64_bold = get_base64_font(font_bold)
    b64_medium = get_base64_font(font_medium)
    b64_regular = get_base64_font(font_regular)
    
    font_css = f"""
    @font-face {{
        font-family: 'SamawahBold';
        src: url(data:font/ttf;base64,{b64_bold}) format('truetype');
    }}
    @font-face {{
        font-family: 'SamawahMedium';
        src: url(data:font/ttf;base64,{b64_medium}) format('truetype');
    }}
    @font-face {{
        font-family: 'SamawahRegular';
        src: url(data:font/ttf;base64,{b64_regular}) format('truetype');
    }}
    """
except Exception as e:
    # Fallback to Cairo if fonts can't be loaded
    font_css = "@import url('https://fonts.googleapis.com/css2?family=Cairo:wght@400;600;700&display=swap');"
    st.error(f"Error loading fonts: {e}")

# --- Brand Identity CSS ---
st.markdown(f"""
    <style>
    {font_css}
    
    * {{ font-family: 'SamawahRegular', 'Cairo', sans-serif !important; }}
    
    h1, h2, h3, .brand-title {{ 
        font-family: 'SamawahBold', sans-serif !important; 
        font-weight: 700;
        letter-spacing: -0.02em;
    }}
    
    .label, .metric-card .label, .stTabs [data-baseweb="tab"] {{ 
        font-family: 'SamawahMedium', sans-serif !important; 
        font-weight: 600;
        font-size: 1rem !important;
    }}
    
    .value {{ 
        font-family: 'SamawahBold', sans-serif !important; 
        font-weight: 800;
        font-size: 2.2rem !important;
        color: {SAMAWAH_NAVY};
    }}

    .stButton > button {{
        font-family: 'SamawahMedium', sans-serif !important;
        border-radius: 8px !important;
    }}

    /* Sidebar Typographies */
    [data-testid="stSidebar"] * {{
        font-family: 'SamawahMedium', sans-serif !important;
    }}
    
    /* DataFrame & Table Typography */
    .stDataFrame, .stTable, div[data-testid="stTable"] {{
        font-family: 'SamawahRegular', sans-serif !important;
    }}
    .stDataFrame th, .stTable th {{
        font-family: 'SamawahBold', sans-serif !important;
        background-color: {SAMAWAH_NAVY} !important;
        color: white !important;
    }}
    
    .delta {{ 
        font-family: 'SamawahMedium', sans-serif !important; 
        font-size: 0.85rem !important; 
        margin-top: 0.4rem; 
        color: {SAMAWAH_TEAL}; 
        font-weight: 600; 
    }}

    /* Tabs Styling */
    .stTabs [data-baseweb="tab-list"] {{
        gap: 24px;
        background-color: transparent;
        border-bottom: 1px solid rgba(0, 0, 0, 0.05);
    }}
    .stTabs [data-baseweb="tab"] {{
        height: 50px;
        background-color: transparent !important;
        border: none !important;
        color: #7f8c8d !important;
        font-weight: 600 !important;
    }}
    .stTabs [aria-selected="true"] {{
        color: {SAMAWAH_NAVY} !important;
        border-bottom: 3px solid {SAMAWAH_NAVY} !important;
    }}

    /* Main Background */
    .stApp {{
        background-color: {SAMAWAH_BG};
        color: {SAMAWAH_TEXT};
    }}
    
    /* Sidebar Styling */
    [data-testid="stSidebar"] {{
        background-color: {SAMAWAH_NAVY};
        color: white;
    }}
    
    /* Metrics / KPI Cards */
    .metric-card {{
        background: white;
        border: 1px solid rgba(0, 0, 0, 0.05);
        border-right: 5px solid {SAMAWAH_TEAL};
        border-radius: 12px;
        padding: 1.5rem;
        text-align: right;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.02);
        transition: all 0.3s ease;
        animation: fadeIn 0.5s ease-out forwards;
    }}
    .metric-card:hover {{
        transform: translateY(-2px);
        box-shadow: 0 8px 25px rgba(0, 0, 0, 0.05);
    }}
    

    /* Hide Default Streamlit Branding */
    header {{ background: transparent !important; }}
    header [data-testid="stHeader"] {{ background: transparent !important; }}
    footer {{ visibility: hidden !important; }}
    #MainMenu {{ visibility: hidden !important; }}
    button[data-testid="stHeaderDeployButton"] {{ display: none !important; }}
    [data-testid="stToolbar"] {{ display: none !important; }}
    
    /* Hide Sidebar completely - we use top navigation now */
    [data-testid="stSidebar"] {{ display: none !important; }}
    button[data-testid="stSidebarExpandButton"], 
    div[data-testid="stSidebarCollapseButton"] {{ 
        display: none !important; 
    }}
    
    /* Animation Keyframes */
    @keyframes fadeIn {{
        from {{ opacity: 0; transform: translateY(10px); }}
        to {{ opacity: 1; transform: translateY(0); }}
    }}
    
    /* Apply Animations */
    .metric-card {{
        animation: fadeIn 0.5s ease-out forwards;
    }}
    .stPlotlyChart {{
        animation: fadeIn 0.7s ease-out forwards;
    }}
    
    /* Input Field Styling */
    div[data-baseweb="select"] > div {{
        background-color: white !important;
        border-radius: 8px !important;
        border: 1px solid rgba(0,0,0,0.08) !important;
    }}

    /* RTL Layout Fixes */
    .stMarkdown {{ text-align: right; direction: rtl; }}
    .stDataFrame {{ direction: rtl; }}
    </style>
    """, unsafe_allow_html=True)


# --- Components ---
def kpi_card(title, value, delta=None):
    st.markdown(f"""
    <div class="metric-card">
        <div class="label">{title}</div>
        <div class="value">{value}</div>
        <div class="delta">{delta if delta else ""}</div>
    </div>
    """, unsafe_allow_html=True)

# ---Data Initialization ---
with st.spinner('جاري تحميل بيانات المنصة...'):
    dm = DataManager()
    projects_df = dm.load_data("Projects")
    tasks_df = dm.load_data("Tasks")

# ===== MODERN TOP NAVIGATION BAR =====
st.markdown("""
    <div style='padding: 1rem 0 0.5rem 0; background: rgba(247, 245, 240, 0.95); 
                position: sticky; top: 0; z-index: 1000; border-bottom: 2px solid #118791;'>
    </div>
""", unsafe_allow_html=True)

with st.container():
    col_nav, col_project, col_logo = st.columns([4, 2, 1])
    
    # Modern Navigation Menu (Left)
    with col_nav:
        st.markdown("<div style='padding-top: 15px;'>", unsafe_allow_html=True)
        selected_view = option_menu(
            menu_title=None,
            options=["لوحة التحكم", "مخطط جانت", "المهام", "التحديات", "المستندات", "الاجتماعات", "الإعدادات"],
            icons=["speedometer2", "bar-chart-line", "list-task", "exclamation-triangle", "file-earmark-text", "people", "gear"],
            menu_icon="cast",
            default_index=0,
            orientation="horizontal",
            styles={
                "container": {"padding": "0!important", "background-color": "transparent"},
                "icon": {"color": "#118791", "font-size": "18px"}, 
                "nav-link": {
                    "font-family": "'SamawahMedium', sans-serif",
                    "font-size": "15px",
                    "text-align": "center",
                    "margin": "0px",
                    "padding": "10px 15px",
                    "color": "#414042",
                    "border-radius": "8px"
                },
                "nav-link-selected": {
                    "background-color": "#062759",
                    "color": "white",
                    "font-weight": "600"
                },
            }
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Smart Project Selector (Center)
    with col_project:
        st.markdown("<div style='padding-top: 20px;'>", unsafe_allow_html=True)
        
        # Safety check for projects_df
        if not projects_df.empty and 'Name' in projects_df.columns:
            project_options = ["📊 كل المشاريع"] + projects_df['Name'].tolist()
        else:
            project_options = ["📊 كل المشاريع (لا توجد بيانات)"]
            
        selected_project = st.selectbox(
            "اختر المشروع",
            project_options,
            key="project_selector",
            label_visibility="collapsed"
        )
        st.markdown("</div>", unsafe_allow_html=True)

    # Logo (Right)
    with col_logo:
        # High quality logo URL from Cloudinary
        logo_url = "https://res.cloudinary.com/dg4pnw73t/image/upload/v1768640793/%D9%84%D9%88%D8%AC%D9%88_%D8%B3%D9%85%D8%A7%D9%88%D8%A9_qrui2s.png"
        st.markdown(f'''
            <div style="padding-top: 5px; display: flex; align-items: center; justify-content: center;">
                <img src="{logo_url}" style="width: 80px; border-radius: 50%; mix-blend-mode: multiply;">
            </div>
        ''', unsafe_allow_html=True)

# Store selections in session state
st.session_state.current_project = selected_project
st.session_state.current_view = selected_view

st.markdown("---")

# === Content Rendering Based on Selected View ===

# Filter data based on selected project
if selected_project == "📊 كل المشاريع" or "لا توجد بيانات" in selected_project:
    p_info = projects_df.iloc[0] if (not projects_df.empty and len(projects_df) > 0) else None
    p_id = None
    p_tasks = tasks_df.copy() if not tasks_df.empty else pd.DataFrame()
else:
    if not projects_df.empty and 'Name' in projects_df.columns:
        matching_projects = projects_df[projects_df['Name'] == selected_project]
        if not matching_projects.empty:
            p_info = matching_projects.iloc[0]
            p_id = p_info['Project_ID']
            p_tasks = tasks_df[tasks_df['Project_ID'] == p_id].copy() if not tasks_df.empty else pd.DataFrame()
        else:
            p_info, p_id, p_tasks = None, None, pd.DataFrame()
    else:
        p_info, p_id, p_tasks = None, None, pd.DataFrame()

# KPIs Calculation (Based on Task Count, Supporting Arabic/English)
if not p_tasks.empty:
    total_tasks = len(p_tasks)
    # Supporting both "Completed" and "مكتمل"
    completed_tasks = len(p_tasks[p_tasks['Status'].isin(['Completed', 'مكتمل'])])
    in_progress_tasks = len(p_tasks[p_tasks['Status'].isin(['In Progress', 'جاري التنفيذ', 'قيد التنفيذ', 'قيد الإنجاز'])])
    remaining_tasks = total_tasks - completed_tasks
    progress_pct = round((completed_tasks / total_tasks) * 100, 1) if total_tasks > 0 else 0
else:
    total_tasks, completed_tasks, in_progress_tasks, remaining_tasks, progress_pct = 0, 0, 0, 0, 0

# Date calculation logic
try:
    target_date = pd.to_datetime(p_info['End_Date'])
    days_left = (target_date - datetime.now()).days
except:
    days_left = 0

# Display content header
if p_info is not None:
    st.markdown(f"### {selected_project}")
    
st.markdown("<br>", unsafe_allow_html=True)

# === VIEW ROUTING: Display content based on selected navigation option ===

# ---- VIEW: لوحة التحكم (Dashboard) ----
if selected_view == "لوحة التحكم":
    # Project Header/Banner
    if p_info is not None:
        p_logo = p_info['Logo_URL'] if 'Logo_URL' in p_info and pd.notna(p_info['Logo_URL']) else None
        
        hero_col1, hero_col2 = st.columns([3, 1])
        with hero_col1:
             st.markdown(f"""
                <div style="padding: 1rem; border-right: 5px solid {SAMAWAH_NAVY}; background: white; border-radius: 8px;">
                    <h2 style="margin:0; color: {SAMAWAH_NAVY};">{p_info['Name']}</h2>
                    <p style="margin:5px 0 0 0; color: #666; font-size: 0.9rem;">{p_info.get('Description', 'إدارة المشروع ومتابعة الإنجاز')}</p>
                </div>
            """, unsafe_allow_html=True)
        with hero_col2:
            if p_logo:
                st.markdown(f"""
                    <div style="display: flex; justify-content: flex-end; align-items: center; height: 100%;">
                        <img src="{p_logo}" style="max-height: 80px; max-width: 100%; object-fit: contain; border-radius: 5px;">
                    </div>
                """, unsafe_allow_html=True)
        st.markdown("---")

    # KPIs Row
    c1, c2, c3, c4 = st.columns(4)
    with c1: kpi_card("نسبة الإنجاز", f"{progress_pct}%", f"{completed_tasks} مهمة مكتملة")
    with c2: kpi_card("المهام المتبقية", f"{remaining_tasks}", f"من {total_tasks} مهمة")
    
    if p_info is not None:
        with c3: kpi_card("الميزانية التقديرية", f"{int(p_info['Total_Budget']/1000)}k ر.س", "💰 إجمالي")
        with c4: 
            if days_left < 0:
                kpi_card("الموعد النهائي", "انتهى الموعد", f"📅 {p_info['End_Date']}")
            else:
                kpi_card("الموعد النهائي", f"باقي {days_left} يوم", f"📅 {p_info['End_Date']}")
    
    st.markdown("<br>", unsafe_allow_html=True)
    
    # Analytics Charts
    st.markdown("### 📊 تحليلات المشروع")
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("#### 📊 حالة المهام")
        if not p_tasks.empty:
            st_counts = p_tasks['Status'].value_counts().reset_index()
            st_counts.columns = ['الحالة', 'العدد']
            fig_st = px.bar(st_counts, x='العدد', y='الحالة', orientation='h', color='الحالة',
                            color_discrete_map={
                                "Completed": SAMAWAH_TEAL, "مكتمل": SAMAWAH_TEAL,
                                "In Progress": SAMAWAH_ORANGE, "جاري التنفيذ": SAMAWAH_ORANGE, "قيد التنفيذ": SAMAWAH_ORANGE,
                                "Not Started": SAMAWAH_NAVY, "لم يبدأ": SAMAWAH_NAVY
                            })
            fig_st.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)', showlegend=False)
            st.plotly_chart(fig_st, use_container_width=True)
    
    with col2:
        st.markdown("#### 👥 أحمال العمل")
        if not p_tasks.empty:
            wl = p_tasks.groupby('Owner').size().reset_index(name='count').sort_values('count')
            fig_wl = px.bar(wl, x='count', y='Owner', orientation='h', color_discrete_sequence=[SAMAWAH_NAVY])
            fig_wl.update_layout(paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)')
            st.plotly_chart(fig_wl, use_container_width=True)

# ---- VIEW: مخطط جانت (Gantt) ----
elif selected_view == "مخطط جانت":
    st.markdown("### 📅 الجدول الزمني")
    
    if not p_tasks.empty:
        p_tasks['start'] = pd.to_datetime(p_tasks['Start_Date'])
        p_tasks['end'] = pd.to_datetime(p_tasks['End_Date'])
        
        col_f1, col_f2, col_f3 = st.columns(3)
        with col_f1: group_by = st.selectbox("عرض حسب", ["المهام", "القسم", "المسؤول"], key="g_group")
        with col_f2: 
            current_status_vals = p_tasks['Status'].unique().tolist()
            default_status = [v for v in current_status_vals if v not in ['مكتمل', 'Completed']]
            s_filter = st.multiselect("الحالة", current_status_vals, default=default_status if default_status else current_status_vals, key="g_status")
        with col_f3: o_filter = st.multiselect("المسؤول", p_tasks['Owner'].unique().tolist(), key="g_owner")
        
        filtered_tasks = p_tasks.copy()
        if s_filter: filtered_tasks = filtered_tasks[filtered_tasks['Status'].isin(s_filter)]
        if o_filter: filtered_tasks = filtered_tasks[filtered_tasks['Owner'].isin(o_filter)]
        
        y_col = "Sub_Task" if group_by == "المهام" else "Task" if group_by == "القسم" else "Owner"
        
        if group_by == "القسم" and not filtered_tasks.empty:
            dept_agg = filtered_tasks.groupby('Task').agg({
                'start': 'min', 'end': 'max', 'Status': 'first',
                'Sub_Task': lambda x: f"({len(x)}) مهام"
            }).reset_index()
            dept_agg['Combined_Label'] = dept_agg['Task']
            display_tasks = dept_agg
            y_col = "Combined_Label"
        elif group_by == "المهام":
            if "Task" in filtered_tasks.columns and "Sub_Task" in filtered_tasks.columns:
                filtered_tasks['Task_Sub'] = filtered_tasks['Task'].astype(str) + " : " + filtered_tasks['Sub_Task'].astype(str)
                display_tasks = filtered_tasks
                y_col = "Task_Sub"
            else:
                display_tasks = filtered_tasks
        else:
            display_tasks = filtered_tasks
            y_col = "Owner"
        
        if not display_tasks.empty:
            fig = px.timeline(
                display_tasks, x_start="start", x_end="end", y=y_col, color="Status",
                template="plotly_white",
                color_discrete_map={
                    "Completed": SAMAWAH_MINT, "مكتمل": SAMAWAH_MINT,
                    "In Progress": SAMAWAH_TEAL, "جاري التنفيذ": SAMAWAH_TEAL, "قيد التنفيذ": SAMAWAH_TEAL,
                    "Not Started": "#ecf0f1", "لم يبدأ": "#ecf0f1"
                }
            )
            fig.update_layout(
                paper_bgcolor='rgba(0,0,0,0)', plot_bgcolor='rgba(0,0,0,0)',
                margin=dict(l=10, r=10, t=10, b=10),
                height=max(400, len(filtered_tasks) * 30),
                yaxis={'categoryorder': 'total ascending', 'title': None},
                xaxis={'title': None, 'showgrid': True},
                legend=dict(orientation="h", yanchor="bottom", y=1.02, xanchor="right", x=1)
            )
            st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("لا توجد مهام لعرضها.")

# ---- VIEW: المهام (Tasks) ----
elif selected_view == "المهام":
    st.markdown("### 📋 قائمة المهام")
    
    if not p_tasks.empty:
        cols_to_show = ['Task', 'Owner', 'Status', 'Start_Date', 'End_Date', 'Sub_Task']
        display_df = p_tasks[cols_to_show].copy()
        
        edited_df = st.data_editor(
            display_df,
            column_config={
                "Task": "القسم",
                "Sub_Task": "المهمة",
                "Owner": "المسؤول",
                "Status": st.column_config.SelectboxColumn(
                    "الحالة", 
                    options=["مكتمل", "جاري التنفيذ", "قيد التنفيذ", "لم يبدأ", "Completed", "In Progress", "Not Started"], 
                    required=True
                ),
                "Start_Date": "البدء",
                "End_Date": "التسليم"
            },
            use_container_width=True,
            hide_index=True,
            key="pro_editor_samawah"
        )
        
        if st.button("💾 حفظ البيانات وتحديث Google Sheets", type="primary"):
            # Properly merge edited columns back into the full tasks dataframe
            for col in edited_df.columns:
                tasks_df.loc[p_tasks.index, col] = edited_df[col].values
            if dm.save_task_updates(tasks_df):
                st.toast("تم تحديث البيانات حياً على Google Sheets!", icon="🚀")
                time.sleep(1)
                st.rerun()
    else:
        st.info("لا توجد مهام لعرضها.")

# ---- VIEW: التحديات (Challenges) ----
elif selected_view == "التحديات":
    st.markdown("### ⚠️ التحديات والمخاطر")
    challenges_df = dm.load_data("Challenges")
    p_challenges = challenges_df[challenges_df['Project_ID'] == p_id] if p_id else challenges_df
    if not p_challenges.empty:
        st.dataframe(p_challenges[['Description', 'Status', 'Risk_Impact']], use_container_width=True, hide_index=True)
    else:
        st.info("لا توجد مخاطر مسجلة حالياً.")

# ---- VIEW: المستندات (Documents) ----
elif selected_view == "المستندات":
    st.markdown("### 📁 المستندات")
    docs_df = dm.load_data("Documents")
    p_docs = docs_df[docs_df['Project_ID'] == p_id] if p_id else docs_df
    if not p_docs.empty:
        for _, row in p_docs.iterrows():
            st.markdown(f"""
            <div style="background: white; border-right: 4px solid {SAMAWAH_RED}; padding: 1rem; border-radius: 8px; margin-bottom: 0.5rem;">
                <b>{row['Name']}</b> <a href="{row['Link_URL']}" target="_blank" style="float:left; color:{SAMAWAH_TEAL};">🔗 رابط</a>
            </div>
            """, unsafe_allow_html=True)
    else:
        st.info("لا توجد مستندات مرتبطة بهذا المشروع.")

# ---- VIEW: الاجتماعات (Meetings) ----
elif selected_view == "الاجتماعات":
    st.markdown("### 📅 توصيات الاجتماعات الدورية")
    st.caption("سجل التوصيات والمهام المطلوبة من الاجتماعات الدورية لمتابعة تقدم المشروع")
    
    # Load meeting recommendations data
    recommendations_df = dm.load_data("MeetingRecommendations")
    
    # Filter by project if a specific project is selected
    if p_id and not recommendations_df.empty and 'Project_ID' in recommendations_df.columns:
        p_recommendations = recommendations_df[recommendations_df['Project_ID'] == p_id].copy()
    else:
        p_recommendations = recommendations_df.copy() if not recommendations_df.empty else pd.DataFrame()
    
    # --- Add New Recommendation Form ---
    st.markdown("#### ➕ إضافة توصية جديدة")
    
    with st.form(key="add_recommendation_form", clear_on_submit=True):
        col_form1, col_form2 = st.columns(2)
        
        with col_form1:
            rec_date = st.date_input("📅 تاريخ الاجتماع", value=datetime.now().date())
            
            # Get list of team members from Tasks owners
            if not tasks_df.empty and 'Owner' in tasks_df.columns:
                team_members = tasks_df['Owner'].dropna().unique().tolist()
            else:
                team_members = ["مدير المشروع"]
            
            rec_owner = st.selectbox("👤 المسؤول عن التنفيذ", team_members)
        
        with col_form2:
            rec_task = st.text_area("📝 التوصية / المهمة", height=100, placeholder="أدخل تفاصيل التوصية أو المهمة المطلوبة...")
            rec_status = st.selectbox("📊 الحالة", ["قيد التنفيذ", "مكتمل", "معلق", "ملغي"])
        
        submit_button = st.form_submit_button(label="💾 إضافة التوصية", type="primary", use_container_width=True)
        
        if submit_button:
            if rec_task.strip():
                # Create new recommendation row
                new_rec = {
                    "Project_ID": p_id if p_id else (projects_df.iloc[0]['Project_ID'] if not projects_df.empty else "P001"),
                    "Date": str(rec_date),
                    "Recommendation": rec_task.strip(),
                    "Owner": rec_owner,
                    "Status": rec_status,
                    "Created_At": datetime.now().strftime("%Y-%m-%d %H:%M")
                }
                
                # Append to existing dataframe
                if recommendations_df.empty:
                    updated_df = pd.DataFrame([new_rec])
                else:
                    updated_df = pd.concat([recommendations_df, pd.DataFrame([new_rec])], ignore_index=True)
                
                # Save to data source
                if dm.save_meeting_recommendations(updated_df):
                    st.success("✅ تم إضافة التوصية بنجاح!")
                    st.rerun()
                else:
                    st.error("❌ حدث خطأ أثناء حفظ التوصية")
            else:
                st.warning("⚠️ الرجاء إدخال نص التوصية")
    
    st.markdown("---")
    
    # --- Display Existing Recommendations ---
    st.markdown("#### 📋 سجل التوصيات")
    
    if not p_recommendations.empty:
        # Add filters
        col_f1, col_f2 = st.columns(2)
        with col_f1:
            status_filter = st.multiselect(
                "تصفية حسب الحالة",
                p_recommendations['Status'].unique().tolist() if 'Status' in p_recommendations.columns else [],
                key="rec_status_filter"
            )
        with col_f2:
            owner_filter = st.multiselect(
                "تصفية حسب المسؤول",
                p_recommendations['Owner'].unique().tolist() if 'Owner' in p_recommendations.columns else [],
                key="rec_owner_filter"
            )
        
        # Apply filters
        filtered_recs = p_recommendations.copy()
        if status_filter and 'Status' in filtered_recs.columns:
            filtered_recs = filtered_recs[filtered_recs['Status'].isin(status_filter)]
        if owner_filter and 'Owner' in filtered_recs.columns:
            filtered_recs = filtered_recs[filtered_recs['Owner'].isin(owner_filter)]
        
        # Display as editable table
        cols_to_display = [col for col in ['Date', 'Recommendation', 'Owner', 'Status'] if col in filtered_recs.columns]
        
        if cols_to_display:
            edited_recs = st.data_editor(
                filtered_recs[cols_to_display],
                column_config={
                    "Date": st.column_config.DateColumn("📅 التاريخ", format="YYYY-MM-DD"),
                    "Recommendation": st.column_config.TextColumn("📝 التوصية", width="large"),
                    "Owner": st.column_config.TextColumn("👤 المسؤول"),
                    "Status": st.column_config.SelectboxColumn(
                        "📊 الحالة",
                        options=["قيد التنفيذ", "مكتمل", "معلق", "ملغي"],
                        required=True
                    )
                },
                use_container_width=True,
                hide_index=True,
                num_rows="dynamic",
                key="recommendations_editor"
            )
            
            # Save button for edits
            if st.button("💾 حفظ التعديلات", type="primary"):
                # Rebuild full dataframe with the user's edits
                if p_id and not recommendations_df.empty and 'Project_ID' in recommendations_df.columns:
                    # Keep other projects' data, replace current project's data with edits
                    other_projects = recommendations_df[recommendations_df['Project_ID'] != p_id]
                    edited_recs['Project_ID'] = p_id
                    edited_recs['Created_At'] = filtered_recs['Created_At'].values[:len(edited_recs)] if 'Created_At' in filtered_recs.columns else datetime.now().strftime("%Y-%m-%d %H:%M")
                    updated_full_df = pd.concat([other_projects, edited_recs], ignore_index=True)
                else:
                    updated_full_df = edited_recs
                
                if dm.save_meeting_recommendations(updated_full_df):
                    st.toast("تم حفظ التعديلات بنجاح!", icon="✅")
                    time.sleep(1)
                    st.rerun()
                else:
                    st.error("حدث خطأ أثناء الحفظ")
        else:
            st.info("لا توجد أعمدة لعرضها.")
    else:
        st.info("📭 لا توجد توصيات مسجلة لهذا المشروع. استخدم النموذج أعلاه لإضافة توصية جديدة.")
    
    # Statistics summary
    if not p_recommendations.empty and 'Status' in p_recommendations.columns:
        st.markdown("---")
        st.markdown("#### 📊 ملخص الإحصائيات")
        stat_cols = st.columns(4)
        total_recs = len(p_recommendations)
        completed_recs = len(p_recommendations[p_recommendations['Status'] == 'مكتمل'])
        pending_recs = len(p_recommendations[p_recommendations['Status'] == 'قيد التنفيذ'])
        suspended_recs = len(p_recommendations[p_recommendations['Status'] == 'معلق'])
        
        with stat_cols[0]:
            kpi_card("إجمالي التوصيات", str(total_recs), "📋 كل التوصيات")
        with stat_cols[1]:
            kpi_card("مكتملة", str(completed_recs), f"{round(completed_recs/total_recs*100, 1) if total_recs > 0 else 0}%")
        with stat_cols[2]:
            kpi_card("قيد التنفيذ", str(pending_recs), "⏳ جاري العمل")
        with stat_cols[3]:
            kpi_card("معلقة", str(suspended_recs), "⚠️ تحتاج متابعة")

# ---- VIEW: الإعدادات (Settings) ----
elif selected_view == "الإعدادات":
    st.markdown("### ⚙️ الإعدادات وحالة النظام")
    
    # Connection Status
    if dm.use_gsheets:
        st.success(f"✅ **متصل بـ Google Sheets**")
        st.caption(f"📄 {dm.sheet_url}")
    else:
        st.warning("⚠️ وضع المحلي - غير متصل بـ Google Sheets")
    
    st.divider()
    
    # Refresh Data Button
    if st.button("🔄 إعادة تحميل البيانات من Google Sheets"):
        st.cache_data.clear()
        st.rerun()
    
    st.divider()
    
    # System Info
    st.markdown("#### ℹ️ معلومات النظام")
    st.caption(f"📊 إجمالي المشاريع: {len(projects_df)}")
    st.caption(f"📋 إجمالي المهام: {len(tasks_df)}")
