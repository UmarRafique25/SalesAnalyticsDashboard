import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

st.set_page_config(
    page_title='Sales Analytics Dashboard',
    page_icon='📊',
    layout='wide'
)

st.title('📊 Sales Analytics Dashboard')
st.markdown('Analyze sales performance, trends, and business insights.')

df = pd.read_csv('processed/cleaned_sales_data.csv')

st.subheader('Dataset Preview')
st.dataframe(df.head())

total_sales = df['sales'].sum()
total_profit = df['profit'].sum()
total_orders = df.shape[0]
avg_sales = df['sales'].mean()

col1, col2, col3, col4 = st.columns(4)

col1.metric('Total Sales', f'${total_sales:,.2f}')
col2.metric('Total Profit', f'${total_profit:,.2f}')
col3.metric('Total Orders', total_orders)
col4.metric('Average Sales', f'${avg_sales:,.2f}')

st.sidebar.header('Filters')

region = st.sidebar.selectbox(
    'Select Region',
    df['region'].unique()
)

filtered_df = df[df['region'] == region]

st.subheader(f'Data for {region} Region')
st.dataframe(filtered_df.head())

monthly_sales = filtered_df.groupby('month_name')['sales'].sum()

fig, ax = plt.subplots(figsize=(12,6))

monthly_sales.plot(kind='line', marker='o', ax=ax)

ax.set_title('Monthly Sales Trend')
ax.set_xlabel('Month')
ax.set_ylabel('Sales')

st.pyplot(fig)

monthly_profit = filtered_df.groupby('month_name')['profit'].sum()

fig, ax = plt.subplots(figsize=(12,6))

monthly_profit.plot(kind='bar', ax=ax)

ax.set_title('Monthly Profit Analysis')
ax.set_xlabel('Month')
ax.set_ylabel('Profit')

st.pyplot(fig)

top_products = filtered_df.groupby('product_name')['sales'].sum().sort_values(ascending=False).head(10)

fig, ax = plt.subplots(figsize=(12,6))

top_products.plot(kind='bar', ax=ax)

ax.set_title('Top Selling Products')
ax.set_xlabel('Products')
ax.set_ylabel('Sales')

plt.xticks(rotation=45)

st.pyplot(fig)

category_sales = filtered_df.groupby('category')['sales'].sum()

fig, ax = plt.subplots(figsize=(8,8))

category_sales.plot(kind='pie', autopct='%1.1f%%', ax=ax)

ax.set_ylabel('')
ax.set_title('Category-wise Sales Distribution')

st.pyplot(fig)

correlation = filtered_df.corr(numeric_only=True)

fig, ax = plt.subplots(figsize=(10,6))

sns.heatmap(correlation, annot=True, cmap='coolwarm', ax=ax)

ax.set_title('Correlation Heatmap')

st.pyplot(fig)

csv = filtered_df.to_csv(index=False)

st.download_button(
    label='Download Filtered Data',
    data=csv,
    file_name='filtered_sales_data.csv',
    mime='text/csv'
)

