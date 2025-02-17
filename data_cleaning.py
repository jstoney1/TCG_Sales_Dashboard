# Import necessary libraries
import pandas as pd

# Load the data
df = pd.read_csv('card_sales_data.csv')

# Display the first few rows to understand the structure
print(df.head())

# Remove redundant columns
columns_to_drop = ['Seller Name', 'Product Type']  # Adjust these based on your CSV's column names
df = df.drop(columns=columns_to_drop)

# Check for missing values
print(df.isnull().sum())

# Data Cleaning Steps:

# 1. Handle Missing Values
# For 'Net Sales', assume it's the sum of 'Item Unit Price (USD)' and 'Shipping'
df['Net Sales'] = df['Net Sales'].fillna(df['Item Unit Price (USD)'] + df['Shipping'])

# For 'Net Revenue', 'Refunded', 'Commission Fees', 'Program Fees', 'Processing Fees', 'Total Fees':
# Here, we're assuming missing values should be zero since they might not apply to all transactions
columns_to_zero = ['Net Revenue', 'Refunded', 'Commission Fees', 'Program Fees', 'Processing Fees', 'Total Fees']
for column in columns_to_zero:
    df[column] = df[column].fillna(0)

# 2. Convert data types if necessary
# Ensure numeric columns are treated as numbers
numeric_columns = ['Item Unit Price (USD)', 'Shipping', 'Net Sales', 'Net Revenue', 'Refunded', 'Commission Fees', 'Program Fees', 'Processing Fees', 'Total Fees']
for column in numeric_columns:
    df[column] = pd.to_numeric(df[column], errors='coerce')  # Coerce errors to NaN

# 3. Date Handling
# Convert 'Day of Seller Ordered At (ET)' to datetime for easier manipulation later
df['Day of Seller Ordered At (ET)'] = pd.to_datetime(df['Day of Seller Ordered At (ET)'], format='%m/%d/%y')

# 4. Check for duplicates
# Remove duplicate entries based on all columns
df.drop_duplicates(inplace=True)

# 5. Handle inconsistent data
# Example: Standardize 'Product Condition' if there are variations like 'Near Mint' vs 'NM'
df['Item Condition'] = df['Item Condition'].str.lower().str.replace('near mint', 'nm').str.strip()

# 6. Calculate or correct derived metrics
# Ensure 'TOTAL PRODUCT COUNT' matches the number of items in each order
df['TOTAL PRODUCT COUNT'] = df['TOTAL PRODUCT COUNT'].astype(int)

# 7. Save the cleaned data
df.to_csv('cleaned_card_sales_data.csv', index=False)

# Display cleaned data info
print(df.info())

# Check if there are still any missing values
print(df.isnull().sum())
