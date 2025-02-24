import pandas as pd
import requests
import os

# Load datasets
sales_url = "https://raw.githubusercontent.com/jstoney1/TCG_Sales_Dashboard/refs/heads/main/data/ProfessorSteg%20Sales%20Report%20-%20ProfessorSteg%20Sales%20Report.csv"
order_url = "https://raw.githubusercontent.com/jstoney1/TCG_Sales_Dashboard/refs/heads/main/data/TCGPlayer%20Card%20Business%20Spreadsheet%20-%20Order%20Data.csv"
card_url = "https://raw.githubusercontent.com/jstoney1/TCG_Sales_Dashboard/refs/heads/main/data/TCGPlayer%20Card%20Business%20Spreadsheet%20-%20Single%20Card%20Data.csv"
set_url = "https://raw.githubusercontent.com/jstoney1/TCG_Sales_Dashboard/refs/heads/main/data/TCGPlayer%20Card%20Business%20Spreadsheet%20-%20Sales%20Data%20by%20Set.csv"
sales_by_card_url = "https://raw.githubusercontent.com/jstoney1/TCG_Sales_Dashboard/refs/heads/main/data/TCGPlayer%20Card%20Business%20Spreadsheet%20-%20Sales%20Data%20by%20Card.csv"
expenses_url = "https://raw.githubusercontent.com/jstoney1/TCG_Sales_Dashboard/refs/heads/main/data/TCGPlayer%20Card%20Business%20Spreadsheet%20-%20Business%20Expenses.csv"

sales_df = pd.read_csv(sales_url)
order_df = pd.read_csv(order_url)
card_df = pd.read_csv(card_url)
set_df = pd.read_csv(set_url)
sales_by_card_df = pd.read_csv(sales_by_card_url)
expenses_df = pd.read_csv(expenses_url)

# Clean sales data
sales_df['Net Sales'] = sales_df['Net Sales'].replace(0, sales_df['Item Unit Price (USD)'] * sales_df['TOTAL PRODUCT COUNT'] + sales_df['Shipping']).fillna(0)
sales_df['Net Revenue'] = sales_df['Net Revenue'].replace('', sales_df['Item Unit Price (USD)'] * sales_df['TOTAL PRODUCT COUNT'] - sales_df['Total Fees']).fillna(0)
sales_df['Cost Basis (USD)'] = sales_df['Cost Basis (USD)'].fillna(0.25)

# Clean order data
order_df = order_df.rename(columns={'Quantity Ordered': 'Quantity', 'Item Price': 'Item Price (USD)'})
order_df['Total Fees'] = order_df['Commission Fee'] + order_df['Payment Processing Fee'].fillna(0)

# Clean card data
card_df = card_df.rename(columns={'Cost': 'Cost Basis (USD)'})

# Merge datasets
merged_df = sales_df.merge(order_df[['Order Number', 'Product Name', 'Quantity', 'Item Price (USD)', 'Shipping Charged', 'Total Fees', 'Order Date']], 
                          on=['Order Number', 'Product Name'], how='left', suffixes=('_sales', '_order'))
merged_df = merged_df.merge(card_df[['Product Name', 'Set Name', 'Cost Basis (USD)']], 
                           on=['Product Name', 'Set Name'], how='left', suffixes=('', '_card'))
merged_df['Quantity'] = merged_df['Quantity'].fillna(merged_df['TOTAL PRODUCT COUNT'])
merged_df['Item Price (USD)'] = merged_df['Item Price (USD)_order'].fillna(merged_df['Item Unit Price (USD)'])
merged_df['Shipping'] = merged_df['Shipping Charged'].fillna(merged_df['Shipping'])
merged_df['Total Fees'] = merged_df['Total Fees_order'].fillna(merged_df['Total Fees_sales'])
merged_df['Cost Basis (USD)'] = merged_df['Cost Basis (USD)_card'].fillna(merged_df['Cost Basis (USD)'])
merged_df['Profit'] = merged_df['Net Revenue'] - (merged_df['Cost Basis (USD)'] * merged_df['Quantity'])
merged_df['Profit Margin (%)'] = (merged_df['Profit'] / (merged_df['Net Revenue'] + merged_df['Total Fees'])) * 100

# Basic analysis
total_units = merged_df['Quantity'].sum()
gross_sales = (merged_df['Item Price (USD)'] * merged_df['Quantity'] + merged_df['Shipping']).sum()
net_revenue = merged_df['Net Revenue'].sum()
total_fees = merged_df['Total Fees'].sum()
total_cost = (merged_df['Cost Basis (USD)'] * merged_df['Quantity']).sum()
total_profit = merged_df['Profit'].sum()
total_expenses = expenses_df['Amount'].sum()
net_profit = total_profit - total_expenses
overall_profit_margin = (net_profit / (net_revenue + total_fees)) * 100 if (net_revenue + total_fees) > 0 else 0

print(f"Total Units Sold: {total_units}")
print(f"Gross Sales: ${gross_sales:.2f}")
print(f"Net Revenue: ${net_revenue:.2f}")
print(f"Total Fees: ${total_fees:.2f}")
print(f"Total Cost: ${total_cost:.2f}")
print(f"Total Profit (before expenses): ${total_profit:.2f}")
print(f"Total Business Expenses: ${total_expenses:.2f}")
print(f"Net Profit (after expenses): ${net_profit:.2f}")
print(f"Overall Profit Margin: {overall_profit_margin:.2f}%")

# Top 5 sales with profit
top_sales = merged_df.nlargest(5, 'Net Revenue')[['Product Name', 'Net Revenue', 'Cost Basis (USD)', 'Profit', 'Profit Margin (%)', 'Day of Seller Ordered At (ET)', 'Product Line']]
print("\nTop 5 Sales with Profit:\n", top_sales)

# Fetch images
os.makedirs('images', exist_ok=True)
for index, row in top_sales.iterrows():
    if row['Product Line'] == 'Magic':
        card_name = row['Product Name']
        response = requests.get(f"https://api.scryfall.com/cards/named?exact={card_name}")
        if response.status_code == 200:
            card_data = response.json()
            image_url = card_data.get('image_uris', {}).get('normal', '')
            if image_url:
                img_data = requests.get(image_url).content
                with open(f"images/{card_name.replace('/', '_')}.jpg", 'wb') as img_file:
                    img_file.write(img_data)
                print(f"Saved image for {card_name}")
            else:
                print(f"No image URL for {card_name}")
        else:
            print(f"Failed to fetch {card_name}: {response.status_code}")

# Product line and set breakdowns
product_lines = merged_df.groupby('Product Line')[['Net Sales', 'Profit']].sum()
print("\nSales and Profit by Product Line:\n", product_lines)
set_summary = merged_df.groupby('Set Name')[['Net Sales', 'Profit']].sum().nlargest(5, 'Net Sales')
print("\nTop 5 Sets by Sales:\n", set_summary)