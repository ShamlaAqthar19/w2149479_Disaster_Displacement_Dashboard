import streamlit as st
import pandas as pd
import plotly.express as px
#set page config
st.set_page_config(page_title='Disaster Displacement Dashboard', layout='wide')
#loading the clean dataset
@st.cache_data 
def load_data():
    return pd.read_csv('../cleaned_data.csv')
df = load_data()
#dashboard title and description
st.title('Disaster Displacement Analysis')
st.markdown(f'This dashboard analyses **{len(df):,}** recorded disaster displacement events globally')
#
sum_displacement = df['new_displacement'].sum()
hazard_top = df.groupby('hazard_type_name')['new_displacement'].sum().idxmax()
col_1,col_2 = st.columns(2)
with col_1:
    st.metric('Total people displaced', f'{sum_displacement:,.0f}')
with col_2:
    st.metric('Top Hazard type', hazard_top)
#trend line
st.subheader('Displacement Trend over the years')
trend = df.groupby('year')['new_displacement'].sum().reset_index()
plotfig = px.line(trend, x='year',y='new_displacement',markers=True,title='Displacement by Year')
st.plotly_chart(plotfig,use_container_width=True)