#✅ Library Imports: Loads the necessary libraries — pandas for data manipulation, Streamlit for web interface, and Plotly Express for visualizations.
#✅ Streamlit Configuration: Sets up the initial page configuration, defining the page title shown in the browser tab and applying a wide layout to better use the screen space.
import pandas as pd
# Imports the pandas library for handling tabular data
import streamlit as st
# Imports Streamlit for building interactive web interfaces
import plotly.express as px
# Imports Plotly Express for creating interactive visualizations
import io

#✅ Page Configuration: Defines how the Streamlit app appears, setting the browser tab title and adjusting the layout to use the full width of the screen, making the dashboard more spacious and visually appealing.
# Page configuration
st.set_page_config(page_title="Dashboard_de_Vendas", layout="wide")
# Sets the page title that appears in the browser tab and configures the page layout to "wide"
# (full screen width) for a more spacious dashboard view in Streamlit


#✅ Data Loading & Preparation: Loads the sales data from a CSV, handling specific separators and decimal formats.
#✅ Converts the ‘Date’ column to a datetime object to enable time-based operations.
#✅ Sorts the dataset chronologically and extracts the year-month portion into a new ‘Month’ column, useful for grouping or plotting by month.
#✅ Sidebar Filter: Adds a sidebar dropdown where the user can select a specific month from the data.
#✅ Based on the user’s selection, filters the dataset so the dashboard only displays data relevant to that chosen month.
# Load data
df = pd.read_csv("supermarket_sales.csv", sep=";", decimal=",")
# Reads the CSV file using semicolon as separator and comma as decimal mark

df["Date"] = pd.to_datetime(df["Date"])
# Converts the 'Date' column to datetime format

df = df.sort_values("Date")
# Sorts the dataframe by the 'Date' column in ascending order

df["Month"] = df["Date"].dt.strftime('%Y-%m')
# Creates a new 'Month' column in 'YYYY-MM' string format extracted from 'Date'

# Sidebar
month = st.sidebar.selectbox("Select the Month", sorted(df["Month"].unique()))
# Creates a dropdown in the sidebar allowing the user to select a month from the available unique months

df_filtered = df[df["Month"] == month]
# Filters the dataframe to include only rows that match the selected month

#✅ Dashboard Titles: Sets up the main title and subheader for the Streamlit dashboard interface.
#✅ Clearly informs the user about the purpose of the dashboard (supermarket sales) and shows the selected month dynamically using the month variable.
# Title
st.title("📊 Dashboard de Vendas - Supermercado")
# Displays the main title at the top of the Streamlit app

st.subheader(f"Selected month: {month}")
# Displays a subheader showing the currently selected month


#✅ KPI Display: Creates a visually appealing section with three key performance indicators: total revenue, average rating, and number of orders.
#✅ Uses Streamlit columns to neatly align the metrics side by side for clarity.
#✅ All values are calculated based on the filtered data for the selected month, giving users a quick performance snapshot.
# KPIs
st.markdown("### 📈 Key Performance Indicators")
# Adds a section header for the KPI (metrics) section

kpi1, kpi2, kpi3 = st.columns(3)
# Creates three equal-width columns to display the KPIs side by side

kpi1.metric("Total Revenue", f"R$ {df_filtered['Total'].sum():,.2f}")
# Shows the total revenue for the selected month

kpi2.metric("Average Rating", f"{df_filtered['Rating'].mean():.2f}")
# Displays the average customer rating for the selected month

kpi3.metric("Number of Orders", f"{df_filtered.shape[0]}")
# Shows the total number of orders (rows) for the selected month

#✅ Main Visuals Layout: Sets up two columns to display two key charts side by side.
#✅ One chart shows daily revenue trends, while the other shows revenue breakdown by product type.
#✅ Uses Plotly for interactive, visually appealing bar charts, and Streamlit to render them responsively.
# Main chart layout
col1, col2 = st.columns(2)
# Creates two side-by-side columns to place the main charts

# Chart 1: Revenue by day
daily_total = df_filtered.groupby("Date")[["Total"]].sum().reset_index()
# Groups the filtered data by date and sums total revenue per day

fig_date = px.bar(daily_total, x="Date", y="Total", color_discrete_sequence=px.colors.qualitative.Set2,
                  title="Revenue by Day")
# Creates a bar chart showing daily revenue

col1.plotly_chart(fig_date, use_container_width=True)
# Displays the chart in the first column, using full container width

# Chart 2: Revenue by product type
product_total = df_filtered.groupby("Product line")[["Total"]].sum().reset_index()
# Groups the filtered data by product line and sums total revenue per product type

fig_prod = px.bar(product_total, x="Total", y="Product line", orientation="h",
                  color_discrete_sequence=px.colors.qualitative.Set2, title="Revenue by Product Type")
# Creates a horizontal bar chart showing revenue by product line

col2.plotly_chart(fig_prod, use_container_width=True)
# Displays the chart in the second column, using full container width


#✅ Additional Visuals: Adds more analytical charts: revenue by branch, revenue by payment type, and average rating by branch.
#✅ Uses Streamlit columns to organize these visual elements into clear, side-by-side layouts.
#✅ Enhances dashboard insights by covering both sales performance and customer satisfaction metrics.
# Additional charts
col3, col4 = st.columns(2)
# Creates two more side-by-side columns for extra charts

# Chart 3: Revenue by branch (city)
city_total = df_filtered.groupby("City")[["Total"]].sum().reset_index()
# Groups data by city and sums total revenue per branch

fig_city = px.bar(city_total, x="City", y="Total", color_discrete_sequence=px.colors.qualitative.Set2,
                  title="Revenue by Branch")
# Creates a bar chart showing total revenue per city (branch)

col3.plotly_chart(fig_city, use_container_width=True)
# Displays the chart in the third column

# Chart 4: Revenue by payment type
fig_kind = px.pie(df_filtered, values="Total", names="Payment",
                  color_discrete_sequence=px.colors.qualitative.Set2, title="Revenue by Payment Type")
# Creates a pie chart showing the revenue share by payment method

col4.plotly_chart(fig_kind, use_container_width=True)
# Displays the chart in the fourth column

col5, col6 = st.columns(2)
# Creates another pair of columns for additional charts

# Chart 5: Average rating by branch (city)
city_rating = df_filtered.groupby("City")[["Rating"]].mean().reset_index()
# Groups data by city and calculates the average customer rating per branch

fig_rating = px.bar(city_rating, x="City", y="Rating", color_discrete_sequence=px.colors.qualitative.Set2,
                    title="Average Rating by Branch")
# Creates a bar chart showing the average rating per city (branch)

col5.plotly_chart(fig_rating, use_container_width=True)
# Displays the chart in the fifth column

#✅ Advanced Visuals: Adds a line chart, heatmap, histogram, and boxplot for deeper insights into sales trends, product performance, ratings, and city-level distributions.
#✅ Uses different Plotly chart types to visualize varied data relationships effectively.
#✅ Provides an optional expandable table to let users inspect the underlying filtered data in detail.
# NEW Chart 6: Daily revenue trend (line chart)
fig_trend = px.line(daily_total, x="Date", y="Total", markers=True,
                    color_discrete_sequence=px.colors.qualitative.Set2, title="Daily Revenue Trend")
# Creates a line chart showing daily revenue evolution

st.plotly_chart(fig_trend, use_container_width=True)
# Displays the line chart on the main page

# NEW Chart 7: Product vs. City matrix (heatmap)
prod_city = df_filtered.groupby(["City", "Product line"])[["Total"]].sum().reset_index()
# Groups data by city and product line, summing total revenue

fig_heat = px.density_heatmap(prod_city, x="City", y="Product line", z="Total",
                              color_continuous_scale="Viridis", title="Product vs. City Matrix")
# Creates a heatmap showing the relationship between products and cities by revenue

st.plotly_chart(fig_heat, use_container_width=True)
# Displays the heatmap on the main page

# NEW Chart 8: Ratings distribution (histogram)
fig_hist = px.histogram(df_filtered, x="Rating", nbins=10,
                        color_discrete_sequence=px.colors.qualitative.Set2, title="Ratings Distribution")
# Creates a histogram showing the distribution of customer ratings

st.plotly_chart(fig_hist, use_container_width=True)
# Displays the histogram on the main page

# NEW Chart 9: Revenue distribution by city (boxplot)
fig_box = px.box(df_filtered, x="City", y="Total",
                 color_discrete_sequence=px.colors.qualitative.Set2, title="Revenue Distribution by City")
# Creates a boxplot showing sales distribution across cities

st.plotly_chart(fig_box, use_container_width=True)
# Displays the boxplot on the main page

# Show complete filtered data table (optional)
with st.expander("🔍 View filtered data table"):
    st.dataframe(df_filtered)
# Adds an expandable section where users can view the full filtered dataset as a table


    # Convert DataFrame to CSV
    csv = df_filtered.to_csv(index=False).encode('utf-8')
    st.download_button(
        label="⬇️ Download CSV",
        data=csv,
        file_name='filtered_data.csv',
        mime='text/csv'
    )

    # Convert DataFrame to Excel
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_filtered.to_excel(writer, index=False, sheet_name='Filtered Data')
    buffer.seek(0)  # Reset buffer position to the start

    st.download_button(
        label="⬇️ Download Excel",
        data=buffer,
        file_name='filtered_data.xlsx',
        mime='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet'
    )
