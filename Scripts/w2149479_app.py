#import libraries
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
#dashboard heading and description
st.title('Disaster Displacement Analysis')
st.markdown(f'This dashboard analyses **{len(df):,}** recorded disaster displacement events globally')
#adding a sidebar for filters 
st.sidebar.header('Filters')
#year selector
years = st.sidebar.slider('Years', int(df['year'].min()),
                          int(df['year'].max()),
                          (int(df['year'].min()), int(df['year'].max())))
#hazard selector
hazards = df['hazard_type_name'].unique()
hazard_list = st.sidebar.multiselect('Hazard Type', options=hazards, default=hazards)
#applying the filter
filter_df = df[(df['year']>= years[0]) &
               (df['year']<= years[1])&
               (df['hazard_type_name'].isin(hazard_list))]

#KPI chart to show the total number of displacments across the years and the most contributing hazard type
sum_displacement = filter_df['new_displacement'].sum()
hazard_top = filter_df.groupby('hazard_type_name')['new_displacement'].sum().idxmax()
col_1,col_2 = st.columns(2)
with col_1:
    st.metric('Total people displaced', f'{sum_displacement:,.0f}')
with col_2:
    st.metric('Top Hazard type', hazard_top)
#trend line to see how many accidents happened across the years
st.subheader('Displacement Trend over the years')
#grouping the displacements by year (2008-2024)
trend = filter_df.groupby('year')['new_displacement'].sum().reset_index()
plotfig = px.line(trend, x='year',y='new_displacement',markers=True, color_discrete_sequence=['darkorange'])
st.plotly_chart(plotfig,use_container_width=True)
#bar chart to show the no of displacments by hazard types
st.subheader('Displacements by Hazard')
no_of_hazard = filter_df.groupby('hazard_type_name')['new_displacement'].sum().reset_index().sort_values('new_displacement', ascending=False)
#kept in ascending order for easiness
barfig = px.bar(no_of_hazard, x='new_displacement', y='hazard_type_name', orientation='h',color = 'hazard_type_name')
st.plotly_chart(barfig, use_container_width=True)
#Top 10 affected countries
st.subheader('Top 10 Most Affected Countries')
top_10 = filter_df.groupby('country_name')['new_displacement'].sum().reset_index().nlargest(10,'new_displacement')
topfig = px.bar(top_10, x='country_name', y='new_displacement', color ='new_displacement', color_continuous_scale='Oranges')
st.plotly_chart(topfig,use_container_width=True)
#ploting a map 
st.subheader('Global Distribution of Displacements')
#grouping displacements by country
map = filter_df.groupby('country_name')['new_displacement'].sum().reset_index()
mapfig = px.choropleth(map,locations='country_name', locationmode='country names', color='new_displacement',hover_name='country_name',color_continuous_scale=px.colors.sequential.Oranges)
st.plotly_chart(mapfig, use_container_width=True)


