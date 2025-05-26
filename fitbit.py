import streamlit as st
import pandas as pd
import glob

# Ändra bakgrundsfärg och färgpalett
st.set_page_config(page_title='Visualisering av Fitbit-data', page_icon='📊', layout='wide')
st.markdown("""
    <style>
    .stApp {
        background-color: #000;
    }
    .stButton>button {
        background-color: #4CAF50;
        color: white;
    }
    .stMarkdown {
        color: #fff;
    }
    h1 {
        color: #fff;
    }
    .stChart {
        background-color: #fff !important;
    }
    .stChart > div {
        background-color: #fff !important;
    }
    </style>
    """, unsafe_allow_html=True)

st.title('Visualisering av Fitbit-data')

# Hitta alla excelfiler i mappen
def list_excel_files():
    return ['FitbitMerged.xlsx', 'FitbitMerged2.xlsx']

# Läs in och slå ihop alla excelfiler
def load_data(files):
    dfs = []
    for file in files:
        df = pd.read_excel(file, engine='openpyxl')
        dfs.append(df)
    data = pd.concat(dfs, ignore_index=True)
    return data

excel_files = list_excel_files()

if not excel_files:
    st.error('Inga excelfiler hittades!')
    st.stop()

# Låt användaren välja fil(er)
selected_files = st.multiselect('Välj excelfil(er):', excel_files, default=excel_files)

if not selected_files:
    st.warning('Välj minst en fil för att visa data.')
    st.stop()

# Läs in data
data = load_data(selected_files)

# Visa rådata
data.columns = [col.strip() for col in data.columns]  # Ta bort eventuella whitespaces
st.subheader('Rådata')
st.dataframe(data.head(100))

# Omvandla ActivityDate till datum om det behövs
if not pd.api.types.is_datetime64_any_dtype(data['ActivityDate']):
    data['ActivityDate'] = pd.to_datetime(data['ActivityDate'])

# Kontrollera om kolumnen 'UserID' finns, annars använd 'Id'
user_column = 'UserID' if 'UserID' in data.columns else 'Id'
user_ids = data[user_column].dropna().unique()
selected_users = st.multiselect('Välj användare:', user_ids, default=user_ids)

filtered_data = data[data[user_column].isin(selected_users)]

# Kontrollera om kolumnen 'Total Steps' finns, annars använd 'TotalSteps'
steps_column = 'Total Steps' if 'Total Steps' in filtered_data.columns else 'TotalSteps'

# Grupp och summera steg per dag
steps_per_day = filtered_data.groupby('ActivityDate')[steps_column].sum().reset_index()

st.subheader('Total Steps per dag')
st.line_chart(steps_per_day, x='ActivityDate', y=steps_column, use_container_width=True, color='#1f77b4')

# Grupp och summera steg per användare
top_users = filtered_data.groupby(user_column)[steps_column].sum().sort_values(ascending=False).reset_index()
st.subheader('Total Steps per användare')
st.bar_chart(top_users, x=user_column, y=steps_column, use_container_width=True, color='#1f77b4')

# Tabell för antal dagar med steg över 0 per användare
days_over_zero = filtered_data[filtered_data[steps_column] > 0].groupby(user_column).size().reset_index(name='Antal dagar med steg över 0')
st.subheader('Antal dagar med steg över 0 per användare')
st.dataframe(days_over_zero)

# Diagram för varje användare per datum
st.subheader('Steg per användare per datum')
for user in selected_users:
    user_data = filtered_data[filtered_data[user_column] == user]
    st.write(f'Användare: {user}')
    st.line_chart(user_data, x='ActivityDate', y=steps_column, use_container_width=True, color='#1f77b4')

st.markdown('---')
st.write('Tips: Du kan ladda upp fler excelfiler i mappen och ladda om sidan för att se dem!')
