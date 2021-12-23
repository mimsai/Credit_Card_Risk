import streamlit as st
import pandas    as pd
import numpy     as np

from datetime         import datetime

import plotly.express as px

st.set_page_config (layout = 'wide')

@st.cache(allow_output_mutation = True)

def get_data (path):
    data = pd.read_csv(path)
    
    return data


def overview_data(data):
    
    ##Statistic Descriptive
    
    num_att = data.select_dtypes( include = ['int64', 'float64'])
    
    # Central Tendency - Mean, Median
    
    media = pd.DataFrame (num_att.apply (np.mean))
    mediana = pd.DataFrame (num_att.apply (np.median))
    
    #Dispersion - std, min, max, range, skew, kurtosis
    
    std = pd.DataFrame (num_att.apply (np.std))
    min_ = pd.DataFrame (num_att.apply (min))
    max_ = pd.DataFrame (num_att.apply (max))
    
    df1 = pd.concat ([max_, min_, media, mediana, std], axis = 1).reset_index()
    
    df1.columns =['attributes', 'max', 'min', 'media', 'mediana', 'std']
    
    st.header ('Statistic Descriptive')
    st.dataframe (df1)

    return None

 
    
def data_distribution (data):
    
    #=====================================================================
    # Distribuição dos Imóveis por Categorias Comerciais
    #=====================================================================
    
    st.sidebar.title('Características do Cliente')
    st.title ('Características do Cliente')
    
    #------------------- Average Age per Loan
    
    #filters
    
    min_age = int(data['person_age'].min())
    max_age = int(data['person_age'].max())
    
    st.sidebar.subheader('Select Max Age')
    f_age = st.sidebar.slider('person_age', min_age,max_age,min_age)
    
    st.header('Average Age per Loan Amnt')
    
    #data select
    
    df = data.loc[data['person_age'] < f_age]
    
    df = df[['person_age', 'loan_amnt']].groupby('person_age').mean().reset_index()
    
    
    #plot
    fig = px.line (df, x = 'person_age', y = 'loan_amnt')
    st.plotly_chart(fig, use_container_width = True)
    
   
    #----------------------- Histograma
    
    st.header ('Grade Distribution')
    st.sidebar.subheader ('Select Max Grade')
    
    #filtering GRADE
    f_grade = st.sidebar.selectbox('Max Grade of Client', sorted(set(data['loan_grade'].unique())))
    df = data.loc[data['loan_grade'] <= f_grade]
    
    #plot
    fig = px.histogram (df, x = 'loan_grade', nbins = 329)
    st.plotly_chart(fig, use_container_width = True)
    
    #filterinh HOME OWNERSHIP
    f_grade = st.sidebar.selectbox('Home Ownership', sorted(set(data['person_home_ownership'].unique())))
    #df = data.loc[data['person_home_ownership'] <= f_grade]
    
    #plot
    fig = px.histogram (data, x = 'person_home_ownership', nbins = 329)
    st.plotly_chart(fig, use_container_width = True)
    
    return None




if __name__ == '__main__':

    #data extration
    #get data
    path = 'df_dashboard.csv'

    #get geofile
    
    data = get_data (path)

    
    #transformation
    
    overview_data(data)
    
    data_distribution (data)

