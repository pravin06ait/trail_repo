import pandas as pd

df=pd.read_csv('Online_Retail.csv')
print(df.head(5))
print(df.info())

customer_counts = df['CustomerID'].value_counts()

print(customer_counts)

duplicate_rows = df[df.duplicated()]

print("Duplicate Rows:")
print(duplicate_rows)

print("Number of Duplicate Rows:")
print(df.duplicated().sum())

df = df.dropna(subset=['CustomerID'])

print("Shape after removing rows with missing CustomerID:")
print(df.shape)

df = df.drop_duplicates()

print("Shape after removing duplicates:")
print(df.shape)

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

print("Info after converting InvoiceDate to datetime:")
print(df.info())

df['TotalAmount'] = df['Quantity'] * df['UnitPrice']
print("Info after calculating TotalAmount:")
print(df.info())

print("Rows with negative Quantity:")
print(df[df['Quantity'] < 0].head())

df = df[df['Quantity'] > 0]
print("Shape after removing rows with negative Quantity:")
print(df.shape)

df = df[df['UnitPrice'] > 0]
print("Shape after removing rows with negative UnitPrice:")
print(df.shape)

cancelled_orders = df[
    df['InvoiceNo'].astype(str).str.startswith('C')
]

print("Cancelled Orders:")
print(cancelled_orders.head())

df = df[
    ~df['InvoiceNo'].astype(str).str.startswith('C')
]
print("Shape after removing cancelled orders:")
print(df.shape)

df['CustomerID'] = df['CustomerID'].astype(int)

print(df['TotalAmount'].describe())

df.to_csv(
    'cleaned_online_retail.csv',
    index=False
)

print("Cleaned dataset saved successfully")