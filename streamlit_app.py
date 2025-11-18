import streamlit as st
import sqlite3
import pandas as pd
import os

st.set_page_config(page_title="Classe Mini 6.50 DB", layout="wide")
st.title("Classe Mini 6.50 – Complete History 1977-2025")

st.markdown("""
**The most complete open database of the Classe Mini 6.50 — free forever**

- 1,400+ boats (Scow / Maxi / Foiling / Pointy filters)  
- 15,000+ race results 1977–2025  
- 800+ skippers (gender, nationality, training base, pedigree)  
- Ownership chains & sales history  
- Updated every Monday automatically

Live data will appear here in the next 24–48 h — stay tuned!
""")

st.balloons()
