import pandas as pd

# Load data from raw GitHub URL
url = "https://raw.githubusercontent.com/jstoney1/TCG_Sales_Dashboard/refs/heads/main/data/ProfessorSteg%20Sales%20Report%20-%20ProfessorSteg%20Sales%20Report.csv"
df = pd.read_csv(url)

# Clean data
df['Net Sales'] = df['Net Sales'].replace(0, df['Item Unit Price (USD)'] * df['TOTAL PRODUCT COUNT'] + df['Shipping']).fillna(0)
df['Net Revenue'] = df['Net Revenue'].replace('', df['Item Unit Price (USD)'] * df['TOTAL PRODUCT COUNT'] - df['Total Fees']).fillna(0)

# Analysis
total_units = df['TOTAL PRODUCT COUNT'].sum()
gross_sales = df['Net Sales'].sum()
net_revenue = df['Net Revenue'].sum()
total_fees = df['Total Fees'].sum()
profit_margin = (net_revenue / gross_sales) * 100 if gross_sales > 0 else 0

print(f"Total Units Sold: {total_units}")
print(f"Gross Sales: ${gross_sales:.2f}")
print(f"Net Revenue: ${net_revenue:.2f}")
print(f"Total Fees: ${total_fees:.2f}")
print(f"Profit Margin: {profit_margin:.2f}%")

# Top 5 sales
top_sales = df.nlargest(5, 'Net Revenue')[['Product Name', 'Net Revenue', 'Day of Seller Ordered At (ET)']]
print("\nTop 5 Sales:\n", top_sales)

# Basic product line breakdown
product_lines = df.groupby('Product Line')['Net Sales'].sum()
print("\nSales by Product Line:\n", product_lines)
