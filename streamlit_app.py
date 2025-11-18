import streamlit as st
import pandas as pd
import os

# ------------------------------------------------------------------
# Page config & header
# ------------------------------------------------------------------
st.set_page_config(page_title="Classe Mini 6.50 DB", layout="wide")
st.title("Classe Mini 6.50 – Complete History 1977-2025")

st.markdown("""
**The most complete open database of the Classe Mini 6.50 — free forever**

1,400+ boats • 15,000+ results • 800+ skippers • 1977–2025 • updated every Monday
""")

# ------------------------------------------------------------------
# Load data (CSV = no openpyxl dependency → works instantly on Streamlit)
# ------------------------------------------------------------------
@st.cache_data
def load_data():
    folder = "data/exports"
    if os.path.exists(folder):
        try:
            boats = pd.read_csv(f"{folder}/Boats.csv")
            results = pd.read_csv(f"{folder}/Results.csv")
            skippers = pd.read_csv(f"{folder}/Skippers.csv")
            return boats, results, skippers
        except:
            pass

    # Fallback sample data (only shown if CSVs are missing)
    boats = pd.DataFrame({
        "sail_number": ["934","981","1048","986","1081","1120"],
        "boat_name": ["Assomast","AFP Biocombustibles","DMG MORI 2","ASCODAL","XUCLA","Future Vector"],
        "public_typing": ["Foiling Scow","Maxi","Foiling Scow","Maxi","Vector","Vector"],
        "foiling": [True,True,True,True,True,True],
        "launch_year": [2023,2022,2022,2021,2024,2025]
    })
    results = pd.DataFrame()
    skippers = pd.DataFrame()
    return boats, results, skippers

boats, results, skippers = load_data()

# Helper: show dataframe with Rank starting at 1
def show_df(df):
    if df.empty:
        st.info("No data yet – coming soon!")
        return
    # Reset index and create Rank column starting at 1
    df_display = df.reset_index(drop=True)
    df_display.insert(0, "Rank", df_display.index + 1)
    st.dataframe(df_display, hide_index=True)

# ------------------------------------------------------------------
# Tabs
# ------------------------------------------------------------------
tab1, tab2, tab3 = st.tabs(["Boats", "2025 Results", "Skippers"])

with tab1:
    st.subheader("Boat Explorer")
    col1, col2, col3 = st.columns(3)
    with col1:
        typing_options = ["All"] + sorted(boats['public_typing'].unique().tolist())
        selected_type = st.selectbox("Boat type", typing_options)
    with col2:
        foiling_filter = st.selectbox("Foiling", ["All", "Yes", "No"])
    with col3:
        year_range = st.slider("Launch year", 1990, 2025, (2018, 2025))

    df = boats.copy()
    if selected_type != "All":
        df = df[df['public_typing'] == selected_type]
    if foiling_filter != "All":
        df = df[df['foiling'] == (foiling_filter == "Yes")]
    df = df[(df['launch_year'] >= year_range[0]) & (df['launch_year'] <= year_range[1])]

    show_df(df)
    st.download_button("Download filtered boats", df.to_csv(index=False), "mini_boats_filtered.csv")

with tab2:
    st.subheader("2025 Race Results (Mini Transat, Fastnet, etc.)")
    show_df(results)

with tab3:
    st.subheader("Skipper Profiles")
    show_df(skippers)

# ------------------------------------------------------------------
# Footer
# ------------------------------------------------------------------
st.markdown("---")
st.markdown(
    "Made with ❤️ for the Mini fleet • "
    "[GitHub](https://github.com/GtHbbrr/clace-mini-db) • "
    "Live since November 2025"
)
st.balloons()
