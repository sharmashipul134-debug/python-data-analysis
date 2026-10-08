import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from io import StringIO

st.set_page_config(page_title="Sales Data Analysis", page_icon="📊", layout="wide")
st.title("📊 Python Sales Data Analysis Application")
st.write("Load, clean, analyze and visualize sales data using Pandas and Matplotlib.")
uploaded = st.file_uploader("Upload a CSV file", type=["csv"])

if uploaded:
    df = pd.read_csv(uploaded)
else:
    df = pd.read_csv("sales_data.csv")
    st.info("Using the sample sales_data.csv. Upload your own CSV to analyze another dataset.")

# Data cleaning
df.columns = [c.strip() for c in df.columns]
df = df.drop_duplicates()
for col in ["Quantity", "Unit_Price", "Sales"]:
    if col in df.columns:
        df[col] = pd.to_numeric(df[col], errors="coerce")
if "Date" in df.columns:
    df["Date"] = pd.to_datetime(df["Date"], errors="coerce")
df = df.dropna(subset=["Sales"])

st.subheader("Dataset Preview")
st.dataframe(df.head(10), use_container_width=True)

c1, c2, c3, c4 = st.columns(4)
c1.metric("Total Sales", f"₹{df['Sales'].sum():,.0f}")
c2.metric("Total Quantity", f"{df['Quantity'].sum():,.0f}" if "Quantity" in df else "N/A")
c3.metric("Orders", f"{len(df):,}")
c4.metric("Average Sale", f"₹{df['Sales'].mean():,.0f}")

st.subheader("Analysis")
col1, col2 = st.columns(2)

with col1:
    if "Product" in df.columns:
        product_sales = df.groupby("Product")["Sales"].sum().sort_values(ascending=False)
        st.write("**Sales by Product**")
        st.bar_chart(product_sales)

with col2:
    if "Region" in df.columns:
        region_sales = df.groupby("Region")["Sales"].sum().sort_values(ascending=False)
        st.write("**Sales by Region**")
        st.bar_chart(region_sales)

st.subheader("Monthly Sales Trend")
if "Date" in df.columns:
    monthly = df.dropna(subset=["Date"]).set_index("Date").resample("ME")["Sales"].sum()
    st.line_chart(monthly)

st.subheader("Category Summary")
if "Category" in df.columns:
    summary = df.groupby("Category").agg(
        Total_Sales=("Sales","sum"),
        Total_Quantity=("Quantity","sum") if "Quantity" in df.columns else ("Sales","count"),
        Average_Sale=("Sales","mean")
    ).round(2)
    st.dataframe(summary, use_container_width=True)

st.subheader("Generate Report")
report = f"""SALES DATA ANALYSIS REPORT

Total sales: ₹{df['Sales'].sum():,.2f}
Total quantity: {df['Quantity'].sum():,.0f}
Number of orders: {len(df)}
Average sale: ₹{df['Sales'].mean():,.2f}
Highest single sale: ₹{df['Sales'].max():,.2f}
Lowest single sale: ₹{df['Sales'].min():,.2f}
"""
if "Product" in df.columns:
    top_product = df.groupby("Product")["Sales"].sum().idxmax()
    report += f"Top product by sales: {top_product}\n"
if "Region" in df.columns:
    top_region = df.groupby("Region")["Sales"].sum().idxmax()
    report += f"Top region by sales: {top_region}\n"

st.download_button("⬇️ Download Text Report", report, file_name="sales_analysis_report.txt")
