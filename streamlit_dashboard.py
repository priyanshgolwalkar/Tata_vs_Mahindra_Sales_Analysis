import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

# Set up Streamlit page config
st.set_page_config(page_title="Tata vs Mahindra Sales Dashboard", layout="wide")

# Define a consistent color palette for visualizations
color_palette = "Set2"  # Feel free to experiment with different palettes like "Set1", "Pastel1", etc.

@st.cache_data
def load_data():
    df = pd.read_excel("Tata_Mahindra_sales.xlsx")
    df['Year'] = df['Year'].astype(str)
    
    # Calculate Yearly Growth Rate (%)
    df = df.sort_values(by=['Brand', 'Year'])
    df['Yearly Growth Rate (%)'] = df.groupby('Brand')['Total Sales'].pct_change() * 100
    df['Yearly Growth Rate (%)'].fillna(0, inplace=True)  # Replace NaN for the first year with 0
    
    return df

df = load_data()

# Sidebar Filters
st.sidebar.header("Filter Data")
selected_years = st.sidebar.multiselect("Select Year(s):", options=sorted(df['Year'].unique()), default=sorted(df['Year'].unique()))
selected_segments = st.sidebar.multiselect("Select Segment(s):", options=sorted(df['Segment'].unique()), default=sorted(df['Segment'].unique()))
selected_engine = st.sidebar.multiselect("Select Engine Type:", options=sorted(df['Engine Type'].unique()), default=sorted(df['Engine Type'].unique()))

# Apply Filters
filtered_df = df[(df['Year'].isin(selected_years)) & 
                 (df['Segment'].isin(selected_segments)) & 
                 (df['Engine Type'].isin(selected_engine))]

st.title("📊 Tata vs Mahindra Sales Dashboard")

# 1. Monthly Sales Trend: Tata vs Mahindra
st.subheader("Monthly Sales Trend: Tata vs Mahindra")
monthly_sales = filtered_df.groupby(['Month', 'Brand'])['Sales Volume'].sum().reset_index()
fig1 = px.line(monthly_sales, x='Month', y='Sales Volume', color='Brand', title='Monthly Sales Trend', 
               color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig1, use_container_width=True)

# 2. Average Market Share (2021–2024) using Seaborn
st.subheader("Average Market Share (2021–2024)")
avg_market_share = filtered_df.groupby('Brand')['Market Share (%)'].mean().reset_index()

# Seaborn Plot
plt.figure(figsize=(8, 5))
sns.barplot(data=avg_market_share, x='Brand', y='Market Share (%)', palette=color_palette)
plt.title('Average Market Share (2021-2024)')
plt.ylabel('Market Share (%)')
st.pyplot(plt)  # Render Seaborn plot in Streamlit

# 3. Segment-Wise Sales Comparison
st.subheader("Segment-Wise Sales Comparison")
segment_sales = filtered_df.groupby(['Segment', 'Brand'])['Sales Volume'].sum().reset_index()
fig3 = px.bar(segment_sales, x='Segment', y='Sales Volume', color='Brand', barmode='group', 
              color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig3, use_container_width=True)

# 4. Fuel Type Popularity
st.subheader("Fuel Type Popularity")
fuel_popularity = filtered_df.groupby(['Engine Type', 'Brand'])['Sales Volume'].sum().reset_index()
fig4 = px.bar(fuel_popularity, x='Engine Type', y='Sales Volume', color='Brand', barmode='group', 
              color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig4, use_container_width=True)

# 5. Price Distribution: Tata vs Mahindra
st.subheader("Price Distribution: Tata vs Mahindra")
fig5 = px.box(filtered_df, x='Brand', y='Price (₹)', color='Brand', title='Price Distribution', 
              color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig5, use_container_width=True)

# 6. Year-over-Year Growth Rate
st.subheader("Year-over-Year Growth Rate")
yoy_growth = filtered_df.groupby(['Year', 'Brand'])['Yearly Growth Rate (%)'].mean().reset_index()
fig6 = px.line(yoy_growth, x='Year', y='Yearly Growth Rate (%)', color='Brand', 
               color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig6, use_container_width=True)

# 7. Top 5 Best-Selling Models
st.subheader("Top 5 Best-Selling Models")
top_models = filtered_df.groupby(['Model', 'Brand'])['Sales Volume'].sum().reset_index()
top5 = top_models.sort_values(by='Sales Volume', ascending=False).head(5)
fig7 = px.bar(top5, x='Model', y='Sales Volume', color='Brand', color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig7, use_container_width=True)

# 8. Which Brand Dominates Each Segment
st.subheader("Brand Dominance by Segment")
segment_dom = filtered_df.groupby(['Segment', 'Brand'])['Sales Volume'].sum().reset_index()
fig8 = px.sunburst(segment_dom, path=['Segment', 'Brand'], values='Sales Volume', 
                   color='Brand', color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig8, use_container_width=True)

# 9. Heatmap of Total Sales by Year and Month
st.subheader("Sales Heatmap by Year and Month")
sales_heat = filtered_df.groupby(['Year', 'Month'])['Sales Volume'].sum().unstack().fillna(0)
fig9, ax9 = plt.subplots(figsize=(12, 5))
sns.heatmap(sales_heat, cmap="YlGnBu", annot=True, fmt=".0f", ax=ax9)
st.pyplot(fig9)

# 10. Price vs Market Share
st.subheader("Price vs Market Share")
fig10 = px.scatter(filtered_df, x='Price (₹)', y='Market Share (%)', color='Brand', hover_data=['Model'], 
                   color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig10, use_container_width=True)

# 11. Cumulative Sales Comparison
st.subheader("Cumulative Sales Comparison: Tata vs Mahindra")
cumulative_sales = filtered_df.groupby(['Year', 'Brand'])['Sales Volume'].sum().groupby(level=1).cumsum().reset_index()
cumulative_sales.columns = ['Year', 'Brand', 'Cumulative Sales']
fig11 = px.line(cumulative_sales, x='Year', y='Cumulative Sales', color='Brand', 
               color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig11, use_container_width=True)

# 12. Compact SUV Market Share
st.subheader("Compact SUV Market Share")
compact_suv = filtered_df[filtered_df['Segment'] == 'Compact SUV']
fig12 = px.pie(compact_suv, names='Brand', values='Market Share (%)', title='Compact SUV Market Share', 
               color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig12, use_container_width=True)

# 13. Mid Size SUV Market Share
st.subheader("Mid Size SUV Market Share")
mid_suv = filtered_df[filtered_df['Segment'] == 'Mid Size SUV']
fig13 = px.pie(mid_suv, names='Brand', values='Market Share (%)', title='Mid Size SUV Market Share', 
               color_discrete_sequence=px.colors.qualitative.Set2)
st.plotly_chart(fig13, use_container_width=True)

