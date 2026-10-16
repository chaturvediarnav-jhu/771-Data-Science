# GDP by Country by Source App
import requests as rq
import bs4
import pandas as pd
import plotly.express as px
import streamlit as st
from io import StringIO

url_1 = 'https://en.wikipedia.org/wiki/List_of_countries_by_GDP_(nominal)'
url_region = 'https://en.wikipedia.org/w/index.php?title=List_of_countries_by_GDP_(nominal)&oldid=1187446467'
#need to make a user agent per wikipedia policy
headers = {'User-Agent': 'DS4BIOHomework/1.0 (chaturvedi.arnav.9@gmail.com)'}
#need at assign missing regions by hand for unavailable data (info from other wikipedia entries on each country)
missing = {
    'Channel Islands': 'Europe',
    'Isle of Man': 'Europe',
    'Faroe Islands': 'Europe',
    'Guam': 'Oceania',
    'American Samoa': 'Oceania',
    'Northern Mariana Islands': 'Oceania',
    'U.S. Virgin Islands': 'Americas',
    'Saint Martin': 'Americas',
}

#need to convert all strings to numbers and make sure no years are attached to numbers
def to_num(s):
    first = s.astype(str).str.extract(r'([\d,]+(?:\.\d+)?)')[0]
    return pd.to_numeric(first.astype(str).str.replace(',', ''), errors='coerce')

# we dont want to pull from wiki every time so store data in a cacahe
@st.cache_data
def load_data():
    page_1 = rq.get(url_1, headers = headers)
    page_region = rq.get(url_region, headers = headers)
    bs4page_1 = bs4.BeautifulSoup(page_1.text, 'html.parser')
    bs4page_region = bs4.BeautifulSoup(page_region.text, 'html.parser')
    tables_1 = bs4page_1.find('table',{'class':"wikitable"})
    tables_region = bs4page_region.find('table', {'id': 'mwmQ'})
    GDPbyC = pd.read_html(StringIO(str(tables_1)))[0]
    CRs = pd.read_html(StringIO(str(tables_region)))[0]
    GDPbyC = GDPbyC[GDPbyC['Country/Territory'] != 'World'].reset_index(drop=True)
    GDPbyC = GDPbyC.replace(r'\[.*?\]', '', regex=True)
    # use column lookup on wikipedia 
    def col(prefix):
        return next(c for c in GDPbyC.columns if str(c).startswith(prefix))

    data = pd.DataFrame({
        'Country': GDPbyC['Country/Territory'],
        'IMF': to_num(GDPbyC[col('IMF')]),
        'World Bank': to_num(GDPbyC[col('World Bank')]),
        'United Nations': to_num(GDPbyC[col('United Nations')]),
    })
    # country and region columns
    regions = CRs.iloc[:, :2].replace(r'\[.*?\]', '', regex=True)   
    regions.columns = ['Country', 'Region']
    data = data.merge(regions, on='Country', how='left')
    data['Region'] = data['Region'].fillna(data['Country'].map(missing))
    return data

data = load_data()

st.title ('GDP by Region')
dataoptions = ['IMF', 'World Bank', 'United Nations']
source = st.selectbox('Select GDP Data Source', dataoptions)

# if there is missing data, backfill data similar to original code
others = [s for s in ['IMF', 'World Bank', 'United Nations'] if s != source]
plot_data = data.copy()
plot_data['GDP'] = plot_data[source].fillna(plot_data[others[0]]).fillna(plot_data[others[1]])
plot_data = plot_data.dropna(subset=['GDP', 'Region'])

# make plot
fig = px.bar(plot_data, x='Region', y='GDP', color='Country',
             hover_name='Country',
             hover_data={'Region': False, 'Country': False},
             labels={'GDP': 'GDP (Million USD)'},
             title=f'GDP by Region ({source})')
fig.update_layout(showlegend=False)
st.plotly_chart(fig, use_container_width=True)