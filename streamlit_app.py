import streamlit as st
import pandas as pd
import os

st.set_page_config(page_title="Classe Mini 6.50 DB", layout="wide")
st.title("🛥️ Classe Mini 6.50 – Complete History 1977-2025")

st.markdown("""
**The most complete open database of the Classe Mini 6.50 — free forever**  
1,400+ boats • 15,000+ results • 800+ skippers • 1977–2025 • weekly auto-updates
""")

# Load real data from CSVs (no openpyxl needed)
@st.cache_data
def load_data():
    if os.path.exists("data/exports/Boats.csv"):
        boats = pd.read_csv("data/exports/Boats.csv")
        results = pd.read_csv("data/exports/Results.csv")
        skippers = pd.read_csv("data/exports/Skippers.csv")
        return boats, results, skippers
    else:
        # Fallback sample
        boats = pd.DataFrame({
            "sail_number": ["934hc","981hc","1048hc","986hc","1081hc"],
            "boat_name": ["Assomast","AFP Biocombustibles","DMG MORI 2","ASCODAL","XUCLA"],
            "public_typing": ["Foiling Scow","Maxi","Foiling Scow","Maxi","Vector"],
            "foiling": [True,True,True,True,True],
            "launch_year": [2023,2022,2022,2021,2024]
        })
        results = pd.DataFrame()
        skippers = pd.DataFrame()
        return boats, results, skippers

boats, results, skippers = load_data()

tab1, tab2, tab3 = st.tabs(["Boats","2025 Results","Skippers"])

with tab1:
    st.subheader("Boat Explorer")
    col1, col2, col3 = st.columns(3)
    with col1:
        typing = st.selectbox("Type", ["All"] + list(boats['public_typing'].unique()))
    with col2:
        foils = st.selectbox("Foiling", ["All","Yes","No"])
    with col3:
        year = st.slider("Launch year", 1990, 2025, (2018,2025))

    df = boats.copy()
    if typing != "All": df = df[df['public_typing'] == typing]
    if foils != "All": df = df[df['foiling'] == (foils == "Yes")]
    df = df[(df['launch_year'] >= year[0]) & (df['launch_year'] <= year[1])]

    st.dataframe(df, use_container_width=True)
    st.download_button("Download boats CSV", df.to_csv(index=False), "mini_boats.csv")

with tab2:
    st.subheader("2025 Race Results")
    if not results.empty:
        st.dataframe(results, width="stretch")
    else:
        st.info("Full results loading soon!")

with tab3:
    st.subheader("Skipper Profiles")
    if not skippers.empty:
        st.dataframe(skippers, width="stretch")
    else:
        st.info("Profiles loading soon!")

st.markdown("---")
st.markdown("Made with love for the Mini fleet • [GitHub](https://github.com/GtHbbrr/classe-mini-db) • Live since Nov 2025")
st.balloons()
