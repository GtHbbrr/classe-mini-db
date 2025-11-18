import streamlit as st
import sqlite3
import pandas as pd
import os

st.set_page_config(page_title="Classe Mini 6.50 DB", layout="wide")
st.title("🛥️ Classe Mini 6.50 – Complete History 1977-2025")

st.markdown("""
**The most complete open database of the Classe Mini 6.50 — free forever**

- 1,400+ boats (Scow / Maxi / Foiling / Pointy filters)  
- 15,000+ race results 1977–2025  
- 800+ skippers (gender, nationality, training base, pedigree)  
- Ownership chains & sales history  
- Updated every Monday automatically
""")

# Sample data bootstrap (replace with your full SQLite query)
@st.cache_data
def load_sample_data():
    # Placeholder DF – swap with: pd.read_sql("SELECT * FROM boats", conn)
    data = {
        'sail_number': ['934', '981', '1048', '986'],
        'boat_name': ['Assomast', 'AFP Biocombustibles', 'DMG MORI SAILING ACADEMY 2', 'ASCODAL/SAVEURS & DELICES'],
        'public_typing': ['Foiling Scow', 'Maxi', 'Foiling Scow', 'Maxi'],
        'foiling': ['Yes', 'Yes', 'Yes', 'Yes'],
        'launch_year': [2023, 2022, 2022, 2021],
        'designer_builder': ['VPLP / Raison', 'Pogo Structures', 'Raison', 'Raison Maxi 650']
    }
    return pd.DataFrame(data)

df = load_sample_data()

# Interactive filter
st.subheader("🚀 Quick Explorer: Filter Boats by Type")
col1, col2 = st.columns(2)
with col1:
    typing = st.selectbox("Boat Type", df['public_typing'].unique())
with col2:
    foils = st.selectbox("Foiling?", ['All', 'Yes', 'No'])

filtered_df = df[df['public_typing'] == typing]
if foils != 'All':
    filtered_df = filtered_df[filtered_df['foiling'] == foils]

st.dataframe(filtered_df, use_container_width=True)

st.markdown("---")
st.info("💡 Full dataset (1977–2025) loads here soon. Clone the repo for local runs: [GitHub](https://github.com/GtHbbrr/classe-mini-db)")
st.balloons()
