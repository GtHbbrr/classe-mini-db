# 1. Set up Python environment
python3 -m venv venv && source venv/bin/activate
pip install pandas openpyxl sqlite3 lxml beautifulsoup4 requests streamlit

# 2. Create folder structure
mkdir -p data/{raw,processed,exports} src public notebooks tests

# 3. Create the first real files
cat > README.md << 'EOF'
# Classe Mini 6.50 – Open Database

Every boat, skipper and result since 1977 – open-source, free forever.

- 1,400+ boats (Scow / Maxi / Foiling / Pointy filters)  
- 15,000+ results (1977–2025)  
- Skipper profiles (gender, nationality, training base)  
- Weekly auto-updates

Live dashboard → coming this week  
Download → data/exports/classe_mini_2025_full.xlsx

Made with love for the Mini fleet.
EOF

# 4. Create a tiny working Streamlit app
cat > streamlit_app.py << 'EOF'
import streamlit as st
st.title("Classe Mini 6.50 – History Explorer")
st.write("Database loading…")
st.write("First public version coming in the next 48 hours!")
st.balloons()
EOF
