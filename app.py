
import streamlit as st
import pandas as pd
import plotly.express as px

st.set_page_config(layout="wide")
st.title("📊 Amazon Reviews Dashboard – Memory Cards")

# Load data
@st.cache_data
def load_data():
    return pd.read_csv("amazon_reviews_light_version.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filters")
selected_rating = st.sidebar.multiselect("Select Star Ratings", options=sorted(df['overall score - 1 is bad and 5 is excellent'].unique()), default=sorted(df['overall score - 1 is bad and 5 is excellent'].unique()))
selected_sentiment = st.sidebar.multiselect("Select Sentiment", options=df['Sentiment'].unique(), default=df['Sentiment'].unique())
selected_fraud = st.sidebar.multiselect("Fraud Suspect", options=df['Fraud Suspect'].unique(), default=df['Fraud Suspect'].unique())

# Apply filters
filtered_df = df[
    (df['overall score - 1 is bad and 5 is excellent'].isin(selected_rating)) &
    (df['Sentiment'].isin(selected_sentiment)) &
    (df['Fraud Suspect'].isin(selected_fraud))
]

# Show KPIs
col1, col2, col3 = st.columns(3)
col1.metric("Total Reviews", len(filtered_df))
col2.metric("Avg. Rating", round(filtered_df['overall score - 1 is bad and 5 is excellent'].mean(), 2))
col3.metric("Positive Sentiment %", f"{(filtered_df['Sentiment'] == 'Positive').mean() * 100:.1f}%")

# Charts
st.subheader("⭐ Rating Distribution")
fig_rating = px.histogram(filtered_df, x='overall score - 1 is bad and 5 is excellent', color='Sentiment', barmode='group')
st.plotly_chart(fig_rating, use_container_width=True)

st.subheader("🕵️ Fraud Suspects Overview")
fraud_chart = filtered_df['Fraud Reason'].value_counts().reset_index()
fraud_chart.columns = ['Reason', 'Count']
fig_fraud = px.bar(fraud_chart, x='Reason', y='Count', title="Fraud Reasons", text_auto=True)
st.plotly_chart(fig_fraud, use_container_width=True)

st.subheader("📋 Sample Reviews")
st.dataframe(filtered_df[['reviewerName', 'reviewText', 'Sentiment', 'Fraud Suspect', 'Fraud Reason']].head(20))
