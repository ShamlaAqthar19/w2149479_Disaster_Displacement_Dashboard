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
#dashboard main heading and description
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
#applying the filters
filter_df = df[(df['year']>= years[0]) &
               (df['year']<= years[1])&
               (df['hazard_type_name'].isin(hazard_list))]
if filter_df.empty:
    st.warning('Please select at least one Hazard Type in the side bar to view analysis')
else:
    #KPI chart to show the total number of displacments across the years
    sum_displacement = filter_df['new_displacement'].sum()
    #KPI chart to show the most contribution hazard type
    hazard_top = filter_df.groupby('hazard_type_name')['new_displacement'].sum().idxmax()
    #KPI chart to show the most affected country
    top_country = filter_df.groupby('country_name')['new_displacement'].sum().idxmax()
    col_1,col_2, col_3= st.columns(3)
    with col_1:
        st.metric('Total People Displaced', f'{sum_displacement:,.0f}')
    with col_2:
        st.metric('Top Hazard Type', hazard_top)
    with col_3:
        st.metric('Most Affected Country', top_country)
    st.divider()
    #Line chart
    #trend line to see how many displacements happened across the years
    st.subheader('Trend of Disaster Displacements Over Time')
    #grouping the displacements by year (2008-2024)
    trend = filter_df.groupby('year')['new_displacement'].sum().reset_index()
    plotfig = px.line(trend, x='year',y='new_displacement',labels={'year': 'Year', 'new_displacement': 'Number of Displacements'}, markers=True, color_discrete_sequence=['darkorange'])
    st.plotly_chart(plotfig,use_container_width=True)
    #Bar chart
    #Top 10 affected countries
    st.subheader('Top 10 Countries with Highest Disaster Displacements')
    top_10 = filter_df.groupby('country_name')['new_displacement'].sum().reset_index().nlargest(10,'new_displacement')
    topfig = px.bar(top_10, x='country_name', y='new_displacement',labels={'country_name': 'Country', 'new_displacement': 'Number of Displacements'}, color ='new_displacement', color_continuous_scale='Oranges', text_auto='.2s')
    st.plotly_chart(topfig,use_container_width=True)
    #Line chart
    #line chart to show the hazard trend over the years
    st.subheader('Top 5 Hazard Trends Over Time')
    #adding a check to prevent the app crashing if only if 5< or 5>hazard types are selected
    h_count = filter_df['hazard_type_name'].nunique()
    n_top = min(5,h_count)
    h_trend = filter_df.groupby('hazard_type_name')['new_displacement'].sum().nlargest(n_top).index
    h_trend_filter = filter_df[filter_df['hazard_type_name'].isin(h_trend)]
    h_trend_f = h_trend_filter.groupby(['year', 'hazard_type_name'])['new_displacement'].sum().reset_index()
    hazardfig = px.line(h_trend_f, x='year', y='new_displacement', labels={'year': 'Year', 'new_displacement': 'Number of Displacements'},color = 'hazard_type_name',markers=True,color_discrete_sequence=px.colors.qualitative.Vivid)
    st.plotly_chart(hazardfig, use_container_width=True)
    #Bar chart
    #bar chart to show the number of displacments by hazard types
    st.subheader('Displacements by Hazard Type')
    no_of_hazard = filter_df.groupby('hazard_type_name')['new_displacement'].sum().reset_index().sort_values('new_displacement', ascending=False)
    #kept in ascending order for easiness
    barfig = px.bar(no_of_hazard, x='new_displacement', y='hazard_type_name',labels={'new_displacement': 'Number of Displacements', 'hazard_type_name':'Hazard Type'},orientation='h',color = 'hazard_type_name', text_auto='.2s')
    st.plotly_chart(barfig, use_container_width=True)
    #Map
    #ploting a map 
    st.subheader('Global Distribution of Disaster Displacements')
    #grouping displacements by country
    country_map = filter_df.groupby('country_name')['new_displacement'].sum().reset_index()
    mapfig = px.choropleth(country_map,locations='country_name', locationmode='country names', color='new_displacement',hover_name='country_name',color_continuous_scale=px.colors.sequential.Oranges)
    st.plotly_chart(mapfig, use_container_width=True)
