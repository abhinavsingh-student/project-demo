import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(page_title="Netflix Pro Dashboard", layout="wide")

st.markdown("""
<style>
[data-testid="stAppViewContainer"] {background-color: #141414;}
h1, h2, h3 {color: #E50914!important;}
p, div, label, span {color: white!important;}
.stMetric {background-color: #221f1f; border-left: 4px solid #E50914; padding: 15px;}
[data-testid="stSidebar"] {background-color: #000;}
[data-testid="stSidebar"] * {color: white!important;}
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_data():
    df = pd.read_csv("netflix_titles.csv")
    df['release_year'] = df['release_year'].astype(int)
    df['country'] = df['country'].fillna("Unknown")
    return df

df = load_data()

st.title("🎬 Netflix Pro Dashboard")

# SIDEBAR
st.sidebar.header("🔍 Filters")
selected_type = st.sidebar.selectbox("Select Content Type", ["All", "Movie", "TV Show"])
year_range = st.sidebar.slider("Select Release Year Range", 
                               int(df['release_year'].min()), 
                               int(df['release_year'].max()), 
                               (2000, 2024))
selected_country = st.sidebar.multiselect("Select Country", options=sorted(df['country'].unique()))

# FILTER
filtered_df = df[(df['release_year'] >= year_range[0]) & (df['release_year'] <= year_range[1])]
if selected_type!= "All":
    filtered_df = filtered_df[filtered_df['type'] == selected_type]
if selected_country:
    filtered_df = filtered_df[filtered_df['country'].isin(selected_country)]

# METRICS
col1, col2, col3, col4 = st.columns(4)
col1.metric("Total Titles", len(filtered_df))
col2.metric("Movies", len(filtered_df[filtered_df['type']=='Movie']))
col3.metric("TV Shows", len(filtered_df[filtered_df['type']=='TV Show']))
col4.metric("Countries", filtered_df['country'].nunique())

# CHART 1
st.subheader("📊 Content by Type")
type_count = filtered_df['type'].value_counts()
fig1 = px.bar(type_count, x=type_count.index, y=type_count.values, color_discrete_sequence=['#E50914'])
fig1.update_layout(plot_bgcolor='#141414', paper_bgcolor='#141414', font_color='white')
st.plotly_chart(fig1, width='stretch')

# CHART 2
st.subheader("🌍 Top 10 Countries")
country_count = filtered_df['country'].value_counts().head(10)
fig2 = px.bar(country_count, x=country_count.index, y=country_count.values, color_discrete_sequence=['#E50914'])
fig2.update_layout(plot_bgcolor='#141414', paper_bgcolor='#141414', font_color='white', xaxis_tickangle=-45)
st.plotly_chart(fig2, width='stretch')

# CHART 3
st.subheader("📈 Titles Over Years")
year_count = filtered_df['release_year'].value_counts().sort_index()
fig3 = px.line(x=year_count.index, y=year_count.values)
fig3.update_traces(line_color='#E50914')
fig3.update_layout(plot_bgcolor='#141414', paper_bgcolor='#141414', font_color='white')
st.plotly_chart(fig3, width='stretch')

# DOWNLOAD
st.download_button("⬇️ Download CSV", filtered_df.to_csv(index=False), "netflix.csv")

# TABLE - FIXED
st.subheader("📋 Data Table")
st.dataframe(filtered_df[['title', 'type', 'release_year', 'country']], use_container_width=True, height=400)
import streamlit as st
import pandas as pd

st.set_page_config(page_title="Netflix Data App", layout="wide")

# 1. Data Load
@st.cache_data
def load_data():
    try:
        df = pd.read_csv("netflix_titles.csv") # yaha apni CSV file ka naam likh
        df.columns = df.columns.str.strip() # column ke naam saaf kar diye
        return df
    except FileNotFoundError:
        st.error("Error: netflix_titles.csv file nahi mili. File ko app.py ke saath same folder me rakh.")
        return pd.DataFrame()

df = load_data()

if df.empty:
    st.stop()

# 2. Sidebar - Filters
st.sidebar.title("🔍 Filters")

# Content Type Filter
content_list = ["All"] + sorted(df['type'].dropna().unique().tolist())
content_type = st.sidebar.selectbox("Select Content Type", content_list, key="content_type_filter")

# Year Range Filter
min_year = int(df['release_year'].min())
max_year = int(df['release_year'].max())
year_range = st.sidebar.slider("Select Release Year Range", min_year, max_year, (min_year, max_year), key="year_slider")

# Country Filter
country_list = ["All"] + sorted(df['country'].dropna().unique().tolist())
country = st.sidebar.selectbox("Select Country", country_list, key="country_filter")

# 3. Data Filtering
filtered_df = df.copy()

if content_type!= "All":
    filtered_df = filtered_df[filtered_df['type'] == content_type]

filtered_df = filtered_df[(filtered_df['release_year'] >= year_range[0]) & (filtered_df['release_year'] <= year_range[1])]

if country!= "All":
    filtered_df = filtered_df[filtered_df['country'].str.contains(country, na=False)]

# 4. Data Table
st.title("📋 Data Table")

# Jo columns chahiye unko safe tarike se lena
columns_to_show = []
for col in ['title', 'type', 'release_year', 'country', 'listed_in', 'Listed In', 'genre']:
    if col in filtered_df.columns:
        columns_to_show.append(col)

if columns_to_show:
    st.dataframe(filtered_df[columns_to_show], use_container_width=True)
else:
    st.warning("Dikhane ke liye koi column nahi mila.")

st.write(f"**Total Records:** {len(filtered_df)}")
