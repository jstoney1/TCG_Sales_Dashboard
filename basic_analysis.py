import pandas as pd

# Load datasets from data subfolder
sales_df = pd.read_csv(r"C:\Users\Owner\Desktop\TCG_Sales_Dashboard\data\ProfessorSteg Sales Report - ProfessorSteg Sales Report.csv")
order_df = pd.read_csv(r"C:\Users\Owner\Desktop\TCG_Sales_Dashboard\data\TCGPlayer Card Business Spreadsheet - Order Data.csv")
card_df = pd.read_csv(r"C:\Users\Owner\Desktop\TCG_Sales_Dashboard\data\TCGPlayer Card Business Spreadsheet - Single Card Data.csv")
expenses_df = pd.read_csv(r"C:\Users\Owner\Desktop\TCG_Sales_Dashboard\data\TCGPlayer Card Business Spreadsheet - Business Expenses.csv")

# Clean sales data (master CSV)
sales_df['Item Unit Price (USD)'] = pd.to_numeric(sales_df['Item Unit Price (USD)'].replace(r'[\$,]', '', regex=True), errors='coerce').fillna(0)
sales_df['Shipping*'] = pd.to_numeric(sales_df['Shipping*'].replace(['FREE', 'N/A', ''], 0).replace(r'[\$,]', '', regex=True), errors='coerce').fillna(0)
sales_df['Total Fees*'] = pd.to_numeric(sales_df['Total Fees*'].replace(r'[\$,]', '', regex=True), errors='coerce').fillna(0)
sales_df['Net Sales*'] = pd.to_numeric(sales_df['Net Sales*'].replace(r'[\$,]', '', regex=True), errors='coerce').fillna(0)
sales_df['Net Revenue*'] = pd.to_numeric(sales_df['Net Revenue*'].replace(r'[\$,]', '', regex=True), errors='coerce').fillna(0)
sales_df['Cost Basis'] = pd.to_numeric(sales_df['Cost Basis'].replace(r'[\$,]', '', regex=True), errors='coerce').fillna(0.25)
print("Number of sales rows:", len(sales_df))
print("Columns in sales_df:", sales_df.columns.tolist())

# Clean order data
order_df = order_df.rename(columns={'Product Price': 'Item Price (USD)', 'Shipping Price': 'Shipping Charged'})
order_df['Item Price (USD)'] = pd.to_numeric(order_df['Item Price (USD)'].replace(r'[\$,]', '', regex=True), errors='coerce').fillna(0)
order_df['Shipping Charged'] = pd.to_numeric(order_df['Shipping Charged'].replace(['FREE', 'N/A', ''], 0).replace(r'[\$,]', '', regex=True), errors='coerce').fillna(0)
print("Number of order rows:", len(order_df))

# Clean card data
card_df.rename(columns={'Card Name': 'Product Name', 'Set': 'Set Name'}, inplace=True)
card_df['Purchase Price'] = pd.to_numeric(card_df['Purchase Price'].replace(r'[\$,]', '', regex=True), errors='coerce').fillna(0)

# Merge datasets, keep all sales_df rows
merged_df = sales_df.merge(order_df[['Order ID', 'Item Price (USD)', 'Shipping Charged', 'Order Date']], 
                          left_on='Order Number', right_on='Order ID', how='left')
merged_df = merged_df.merge(card_df[['Product Name', 'Set Name', 'Purchase Price']], 
                            on=['Product Name', 'Set Name'], how='left')

# Finalize columns
merged_df['Quantity'] = merged_df['TOTAL PRODUCT COUNT']
merged_df['Item Price (USD)'] = merged_df['Item Price (USD)'].fillna(merged_df['Item Unit Price (USD)'])
merged_df['Shipping'] = merged_df['Shipping Charged'].fillna(merged_df['Shipping*'])
merged_df['Total Fees'] = merged_df['Total Fees*']
merged_df['Cost Basis'] = merged_df['Purchase Price'].fillna(merged_df['Cost Basis'])  # Prefer card_df cost
merged_df['Profit'] = merged_df['Net Revenue*'] - (merged_df['Cost Basis'] * merged_df['Quantity'])
merged_df['Profit Margin (%)'] = (merged_df['Profit'] / (merged_df['Net Revenue*'] + merged_df['Total Fees'])) * 100

# Clean expenses data
expenses_df['Amount'] = pd.to_numeric(expenses_df['Amount'].replace(r'[\$,]', '', regex=True), errors='coerce').fillna(0)

# Debug prints
print("Number of merged rows:", len(merged_df))
print("Columns in merged_df:", merged_df.columns.tolist())
print("Sample data:", merged_df[['Product Name', 'Quantity', 'Item Price (USD)', 'Shipping', 'Net Revenue*', 'Total Fees', 'Cost Basis']].head().to_dict())

# Basic analysis
total_units = merged_df['Quantity'].sum()
gross_sales = merged_df['Net Sales*'].sum()  # Use Net Sales* for gross, pre-fees
net_revenue = merged_df['Net Revenue*'].sum()  # Should be $1,343.98
total_fees = merged_df['Total Fees'].sum()
total_cost = (merged_df['Cost Basis'] * merged_df['Quantity']).sum()
total_profit = net_revenue - total_cost
total_expenses = expenses_df['Amount'].sum()
net_profit = total_profit - total_expenses
profit_margin = (net_profit / (net_revenue + total_fees)) * 100 if (net_revenue + total_fees) > 0 else 0

print(f"Total Units Sold: {total_units}")
print(f"Gross Sales: ${gross_sales:.2f}")
print(f"Net Revenue: ${net_revenue:.2f}")
print(f"Total Fees: ${total_fees:.2f}")
print(f"Total Cost: ${total_cost:.2f}")
print(f"Total Profit (before expenses): ${total_profit:.2f}")
print(f"Total Business Expenses: ${total_expenses:.2f}")
print(f"Net Profit (after expenses): ${net_profit:.2f}")
print(f"Overall Profit Margin: {profit_margin:.2f}%")

# Top 5 sales with profit
top_sales = merged_df.nlargest(5, 'Net Revenue*')[['Product Name', 'Net Revenue*', 'Cost Basis', 'Profit', 'Day of Seller Ordered At (ET)', 'Product Line']]
print("\nTop 5 Sales with Profit:\n", top_sales)

# Product line and set breakdowns
product_lines = merged_df.groupby('Product Line')[['Net Sales*', 'Profit']].sum()
print("\nSales and Profit by Product Line:\n", product_lines)
set_summary = merged_df.groupby('Set Name')[['Net Sales*', 'Profit']].sum().nlargest(5, 'Net Sales*')
print("\nTop 5 Sets by Sales:\n", set_summary)