import streamlit as st
import pandas as pd
import plotly.express as px
import os

# Set up page configuration for Scandinavian Dark Mode
st.set_page_config(
    page_title="Conference Hunter",
    page_icon="🎯",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for Scandinavian Dark Mode (minimalist, clean, high contrast)
st.markdown("""
<style>
    /* Global background and text colors */
    .stApp {
        background-color: #121212;
        color: #E0E0E0;
    }
    
    /* Import modern minimalist font */
    @import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;600&display=swap');
    
    /* Headers */
    h1, h2, h3 {
        color: #FFFFFF !important;
        font-family: 'Outfit', sans-serif !important;
        font-weight: 300 !important;
        letter-spacing: 1px;
    }
    
    /* Clean metric cards */
    div[data-testid="stMetricValue"] {
        font-size: 2.5rem;
        color: #4CAF50;
        font-weight: 200;
    }
    div[data-testid="stMetricLabel"] {
        color: #A0A0A0;
        font-size: 1rem;
        letter-spacing: 0.5px;
    }
    
    /* Sidebar styling */
    .css-1d391kg, .css-1lcbmhc {
        background-color: #1A1A1A;
    }
    
    /* Footer styling */
    .footer {
        position: fixed;
        left: 0;
        bottom: 0;
        width: 100%;
        background-color: #121212;
        color: #888888;
        text-align: center;
        padding: 10px;
        font-size: 0.85rem;
        border-top: 1px solid #333333;
        z-index: 100;
    }
</style>
""", unsafe_allow_html=True)

# Application Header
st.title("🎯 Conference Hunter")
st.markdown("---")

# Load Data
@st.cache_data
def load_data():
    file_path = "conference_data.xlsx"
    if not os.path.exists(file_path):
        file_path = "dummy_data.xlsx"
    
    try:
        df = pd.read_excel(file_path)
        return df
    except Exception as e:
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.warning("No data found! Waiting for background scraper to finish...")
else:
    # Sidebar Filters
    st.sidebar.title("Filters")
    st.sidebar.markdown("Refine your intelligence")
    
    topics = ["All"] + sorted(df["Topic"].dropna().unique().tolist())
    selected_topic = st.sidebar.selectbox("Select Topic", topics)
    
    companies = sorted(df["Company"].dropna().unique().tolist())
    selected_companies = st.sidebar.multiselect("Select Companies", companies, default=[])
    
    # Filter Data
    filtered_df = df.copy()
    if selected_topic != "All":
        filtered_df = filtered_df[filtered_df["Topic"] == selected_topic]
    if selected_companies:
        filtered_df = filtered_df[filtered_df["Company"].isin(selected_companies)]
        
    # Key Metrics
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric("Total Speakers", f"{len(filtered_df):,}")
    with col2:
        st.metric("Unique Companies", f"{filtered_df['Company'].nunique():,}")
    with col3:
        st.metric("Total Conferences", f"{filtered_df['Conference Name'].nunique():,}")
    with col4:
        st.metric("Topics Covered", f"{filtered_df['Topic'].nunique():,}")
        
    st.markdown("---")
    
    # Download Section
    import io
    
    @st.cache_data
    def convert_df_to_excel(df_to_convert):
        output = io.BytesIO()
        with pd.ExcelWriter(output, engine='openpyxl') as writer:
            df_to_convert.to_excel(writer, index=False, sheet_name='Speakers')
        return output.getvalue()

    st.subheader("📥 Export Data")
    dl_col1, dl_col2 = st.columns(2)
    
    with dl_col1:
        st.download_button(
            label="Download Filtered Selection (Excel)",
            data=convert_df_to_excel(filtered_df),
            file_name="conference_selection.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            use_container_width=True
        )
        
    with dl_col2:
        st.download_button(
            label="Download Full Database (Excel)",
            data=convert_df_to_excel(df),
            file_name="conference_full_database.xlsx",
            mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
            type="primary",
            use_container_width=True
        )
        
    st.markdown("---")
    
    # Main Content Area
    col_chart, col_table = st.columns([1, 1.5])
    
    with col_chart:
        st.subheader("Top 10 Companies Represented")
        top_companies = filtered_df["Company"].value_counts().head(10).reset_index()
        top_companies.columns = ["Company", "Count"]
        
        # Futuristic Bar Chart
        fig = px.bar(
            top_companies, 
            x="Count", 
            y="Company", 
            orientation='h',
            color="Count",
            color_continuous_scale="Viridis",
            template="plotly_dark"
        )
        fig.update_layout(
            plot_bgcolor="rgba(0,0,0,0)",
            paper_bgcolor="rgba(0,0,0,0)",
            margin=dict(l=0, r=0, t=0, b=0),
            yaxis={'categoryorder':'total ascending'},
            showlegend=False
        )
        st.plotly_chart(fig, use_container_width=True)

    with col_table:
        st.subheader("Speaker Database")
        # Clean dataframe display
        st.dataframe(
            filtered_df,
            use_container_width=True,
            height=400,
            hide_index=True
        )

# Footer branding
st.markdown('<div class="footer">Programmed by <b>Steve Zhelyazkov</b> | Conference Hunter 2026</div>', unsafe_allow_html=True)
