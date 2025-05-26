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
data = pd.read_excel('step_counts.xlsx')
data.columns = [col.strip() for col in data.columns]
data[data.columns[0]] = pd.to_datetime(data[data.columns[0]])

# Skapa tabell med datum och summor
result = data.groupby(data.columns[0])[data.columns[1]].sum().reset_index()
result = result.sort_values(by=data.columns[0], ascending=True)

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
month_data = result[result[result.columns[0]].dt.month == selected_month].copy()
month_data = month_data.sort_values(by=result.columns[0])

st.subheader(f'Stegdata för {months[selected_month]}')
st.bar_chart(month_data.set_index(result.columns[0])[result.columns[1]], height=300)

# Skapa och visa diagram för varje år
st.subheader('Stegdata per år')
years = sorted(result[result.columns[0]].dt.year.unique())

for year in years:
    year_data = result[result[result.columns[0]].dt.year == year].copy()
    year_data = year_data.sort_values(by=result.columns[0])
    
    st.write(f'År {year}')
    st.bar_chart(year_data.set_index(result.columns[0])[result.columns[1]], height=300) 