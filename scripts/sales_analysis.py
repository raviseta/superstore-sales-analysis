import pandas as pd
import matplotlib.pyplot as plt

df = pd.read_csv("data/superstore.csv")

df['Order Date'] = pd.to_datetime(
    df['Order Date'],
    format='%d-%m-%Y',
    errors='coerce'
)

# Check date parsing
missing_dates = df["Order Date"].isna().sum()
print(f"Missing Order Dates: {missing_dates}")

df['Profit Margin'] = df['Profit'] / df['Sales']
df['Month'] = df['Order Date'].dt.to_period('M').dt.to_timestamp()

sales_by_category = df.groupby('Category')['Sales'].sum().sort_values(ascending=False)
profit_by_category = df.groupby('Category')['Profit'].sum().sort_values(ascending=False)
region_sales = df.groupby('Region')['Sales'].sum().sort_values(ascending=False)
top_products = df.groupby('Product Name')['Sales'].sum().sort_values(ascending=False).head(10)
monthly_sales = df.groupby('Month')['Sales'].sum().reset_index()

discount_profit = df.groupby('Discount')['Profit'].mean().reset_index()

category_analysis = df.groupby('Category').agg({
    'Discount': 'mean',
    'Profit': 'sum'
}).reset_index()

furniture_analysis = df.groupby('Category').agg({
    'Discount': 'mean',
    'Profit': 'sum',
    'Sales': 'sum'
}).reset_index()

loss_products = df.groupby('Product Name')['Profit'].sum().sort_values().head(10)

# Print outputs
print("\nSales by Category:")
print(sales_by_category)

print("\nProfit by Category:")
print(profit_by_category)

print("\nSales by Region:")
print(region_sales)

print("\nTop 10 Products by Sales:")
print(top_products)

print("\nAverage Profit by Discount:")
print(discount_profit)

print("\nCategory Analysis:")
print(category_analysis)

print("\nTop 10 Loss-Making Products:")
print(loss_products)

# Chart 1: Monthly Sales Trend
plt.figure(figsize=(10, 6))
plt.plot(monthly_sales["Month"], monthly_sales["Sales"])
plt.title("Monthly Sales Trend")
plt.xlabel("Month")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.savefig("visuals/monthly_sales_trend.png")
plt.close()

# Chart 2: Discount vs Profit
plt.figure(figsize=(10, 6))
plt.scatter(df["Discount"], df["Profit"])
plt.title("Discount vs Profit")
plt.xlabel("Discount")
plt.ylabel("Profit")
plt.tight_layout()
plt.savefig("visuals/discount_vs_profit.png")
plt.close()

# Chart 3: Profit by Category
plt.figure(figsize=(8, 6))
plt.bar(category_analysis["Category"], category_analysis["Profit"])
plt.title("Profit by Category")
plt.xlabel("Category")
plt.ylabel("Profit")
plt.tight_layout()
plt.savefig("visuals/profit_by_category.png")
plt.close()

print("\nCharts saved successfully in visuals/ folder.")
