import streamlit as st
import pandas as pd

# Konfigurera sidan
st.set_page_config(page_title='Visualisering av stegdata', page_icon='📊', layout='wide')
st.markdown("""
    <style>
    .stApp {
        background-color: #ffffff;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stMarkdown {
        color: #000000;
    }
    h1 {
        color: #000000;
    }
    </style>
    """, unsafe_allow_html=True)

st.title('Steg per dag')

# Läs data
data = pd.read_excel('step_.xlsx')
data.columns = ['Datum', 'Steg']  # Sätt korrekta kolumnnamn
data['Datum'] = pd.to_datetime(data['Datum'])

# Skapa tabell med datum och summor
result = data.groupby('Datum')['Steg'].sum().reset_index()
result = result.sort_values(by='Datum', ascending=True)

# Visa tabellen
st.dataframe(result, hide_index=True)

# Skapa månadsväljare
months = {
    1: 'Januari', 2: 'Februari', 3: 'Mars', 4: 'April',
    5: 'Maj', 6: 'Juni', 7: 'Juli', 8: 'Augusti',
    9: 'September', 10: 'Oktober', 11: 'November', 12: 'December'
}
selected_month = st.selectbox('Välj månad', options=list(months.keys()), format_func=lambda x: months[x])

# Filtrera data för vald månad
month_data = result[result['Datum'].dt.month == selected_month].copy()
month_data = month_data.sort_values(by='Datum')

st.subheader(f'Stegdata för {months[selected_month]}')
st.line_chart(month_data.set_index('Datum')['Steg'], height=300)

# Skapa och visa diagram för varje år
st.subheader('Stegdata per år')
years = sorted(result['Datum'].dt.year.unique())

for year in years:
    year_data = result[result['Datum'].dt.year == year].copy()
    year_data = year_data.sort_values(by='Datum')
    
    st.write(f'År {year}')
    st.line_chart(year_data.set_index('Datum')['Steg'], height=300) 