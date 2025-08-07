import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from prophet import Prophet
import plotly.express as px
from geopy.geocoders import Nominatim
import time


# exploratory data :
DF = pd.read_csv('train.csv')
print(DF.shape)
print(DF.head())
print(DF.describe())
print(DF.info())
print(DF.isnull().sum())
print(DF.duplicated().sum())
print(DF.nunique())
geo = Nominatim(user_agent="anyname")

def get_code(city, country):
    try:
        place = geo.geocode(city + ", " + country)
        if place:
            back = geo.reverse((place.latitude, place.longitude))
            if back and 'postcode' in back.raw['address']:
                return back.raw['address']['postcode']
    except:
        return None
for i in DF.index:
    if pd.isna(DF.at[i, 'Postal Code']):
        city = DF.at[i, 'City']
        country = DF.at[i, 'Country']
        code = get_code(city, country)
        DF.at[i, 'Postal Code'] = code
        time.sleep(1)


print(DF['Postal Code'])




# # Data preprocessing:
# DF.drop_duplicates(inplace=True)

DF['Order Date'] = pd.to_datetime(DF['Order Date'], format="%d/%m/%Y")
df_sorted_by_date = DF.sort_values(by='Order Date', ascending=True)
print(df_sorted_by_date.head(10))


DF['Year'] = DF['Order Date'].dt.year
DF['Month'] = DF['Order Date'].dt.month
DF['Day'] = DF['Order Date'].dt.day
DF['Weekday'] = DF['Order Date'].dt.day_name()
DF['Quarter'] = DF['Order Date'].dt.quarter
Quartery_sales = DF.groupby(["Year" ,"Quarter" ])["Sales"].sum().reset_index()
print(Quartery_sales)



# months - sales -> 1
sales_by_month = DF.groupby('Month')['Sales'].sum()
sales_by_month.plot(kind='bar', title='Total Sales by Month', xlabel='Month', ylabel='Sales ($)', figsize=(8,5))
plt.show()

# Category - Sales - 2 
sales_by_category = DF.groupby('Category')['Sales'].sum()
sales_by_category.plot(kind='bar', title='Sales by Category', xlabel='Category', ylabel='Sales ($)', figsize=(8,5))
plt.show()

# sub-Category - Sales - 3
sales_by_sub = DF.groupby('Sub-Category')['Sales'].sum().sort_values()
sales_by_sub.plot(kind='barh', title='Sales by Sub-Category', xlabel='Sales ($)', figsize=(8,8))
plt.show()


# City - sales - 4
top_cities = DF.groupby('City')['Sales'].sum().sort_values(ascending=False).head(10)
top_cities.plot(kind='bar', title='Top 10 Cities by Sales', xlabel='City', ylabel='Sales ($)', figsize=(8,5))
plt.show()



# Region - Sales - 5 
sales_by_region = DF.groupby('Region')['Sales'].sum()
sales_by_segment = DF.groupby('Segment')['Sales'].sum()

fig, axes = plt.subplots(1, 2, figsize=(14, 5))
sales_by_region.plot(kind='bar', ax=axes[0], title='Sales by Region')
sales_by_segment.plot(kind='bar', ax=axes[1], title='Sales by Segment')
plt.tight_layout()
plt.show()


# plt.figure(figsize=(8,5))
# sns.histplot(DF['Sales'], bins=50, kde=True)
# plt.title("Sales Distribution")
# plt.xlabel("Sales")
# plt.ylabel("Frequency")
# plt.xlim(0, 1000) 
# plt.show()




# sales - year -6
sales_by_year = DF.groupby('Year')['Sales'].sum()
sales_by_year.plot(title='yearly sales', xlabel='year' , ylabel ='sales ($)')
plt.show()




# top 10 cusomers by sales :-7
custme_sales = DF.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False)
# print(custme_sales)
top_customers = custme_sales.head(10)
plt.figure(figsize=(10,6))
plt.scatter(top_customers.index, top_customers.values)
plt.title("Top 10 Customers by Sales")
plt.xlabel("Customer Name")
plt.ylabel("Sales")
plt.xticks(rotation=45)
plt.tight_layout()
plt.show()


# "Difference between Ship Date and Order Date (Days) - 8
DF['Order Date'] = pd.to_datetime(DF['Order Date'], format="%d/%m/%Y")
DF['Ship Date'] = pd.to_datetime(DF['Ship Date'], format="%d/%m/%Y")
DF['Ship_Diff_Days'] = (DF['Ship Date'] - DF['Order Date']).dt.days

plt.figure(figsize=(8,5))
sns.histplot(DF['Ship_Diff_Days'], bins=20, kde=True)
plt.title("Difference between Ship Date and Order Date (Days)")
plt.xlabel("Days Difference")
plt.ylabel("Frequency")
plt.show()




# Category - Month - 9 
sales_pivot = DF.pivot_table(index='Category', columns='Month', values='Sales', aggfunc='sum', fill_value=0)
plt.figure(figsize=(10, 6))
sns.heatmap(sales_pivot, annot=True, fmt=".0f", cmap="YlGnBu")
plt.title('Heatmap: Sales by Month and Category')
plt.xlabel('Month')
plt.ylabel('Category')
plt.show()

# Sub-Category - Month - 10
sales_pivot = DF.pivot_table(index='Sub-Category', columns='Month', values='Sales', aggfunc='sum', fill_value=0)
plt.figure(figsize=(14, 10))
sns.heatmap(sales_pivot, annot=True, fmt=".0f", cmap="YlOrRd")
plt.title('Heatmap: Sales by Month and Sub-Category')
plt.xlabel('Month')
plt.ylabel('Sub-Category')
plt.show()


# Quartery_sales - 11
Quartery_sales.plot(kind='bar' , title = "Quartery_sales" , x='Quarter', y='Sales')
plt.show()



sales_month = DF.pivot_table(index='Year', columns='Month', values='Sales', aggfunc='sum', fill_value=0)
sales_month.plot(kind='bar', title='Total Sales Yearly by Month', xlabel='Month', ylabel='Sales ($)', figsize=(8,5))
plt.show()