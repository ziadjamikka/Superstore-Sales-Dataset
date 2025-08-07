import pandas as pd
import plotly.express as px
from dash import Dash, dcc, html
import dash_bootstrap_components as dbc 
from datetime import datetime

#data preprocessing
DF = pd.read_csv('train.csv')
DF['Order Date'] = pd.to_datetime(DF['Order Date'], format='%d/%m/%Y')
DF['Ship Date'] = pd.to_datetime(DF['Ship Date'], format='%d/%m/%Y')

DF['Year'] = DF['Order Date'].dt.year
DF['Month'] = DF['Order Date'].dt.month
DF['Day'] = DF['Order Date'].dt.day
DF['Weekday'] = DF['Order Date'].dt.day_name()
DF['Quarter'] = DF['Order Date'].dt.quarter
DF['Ship_Diff_Days'] = (DF['Ship Date'] - DF['Order Date']).dt.days

# Figures
fig1 = px.bar(DF.groupby('Month')['Sales'].sum().reset_index(),
              x='Month', y='Sales', title='Total Sales by Month',
              color='Month', color_continuous_scale='Viridis')

fig2 = px.bar(DF.groupby('Category')['Sales'].sum().reset_index(),
              x='Category', y='Sales', title='Sales by Category',
              color='Category', color_discrete_sequence=px.colors.qualitative.Dark24)

fig3 = px.bar(DF.groupby('Sub-Category')['Sales'].sum().sort_values().reset_index(),
              x='Sales', y='Sub-Category', orientation='h', title='Sales by Sub-Category',
              color='Sub-Category', color_discrete_sequence=px.colors.qualitative.Pastel)

fig4 = px.bar(DF.groupby('City')['Sales'].sum().sort_values(ascending=False).head(10).reset_index(),
              x='City', y='Sales', title='Top 10 Cities by Sales',
              color='City', color_discrete_sequence=px.colors.qualitative.Bold)

fig5a = px.bar(DF.groupby('Region')['Sales'].sum().reset_index(),
               x='Region', y='Sales', title='Sales by Region',
               color='Region', color_discrete_sequence=px.colors.qualitative.Set2)

fig5b = px.bar(DF.groupby('Segment')['Sales'].sum().reset_index(),
               x='Segment', y='Sales', title='Sales by Segment',
               color='Segment', color_discrete_sequence=px.colors.qualitative.Set1)

fig6 = px.bar(DF.groupby('Year')['Sales'].sum().reset_index(),
              x='Year', y='Sales', title='Yearly Sales',
              color='Year', color_continuous_scale=px.colors.sequential.Plasma)

top_customers = DF.groupby('Customer Name')['Sales'].sum().sort_values(ascending=False).head(10).reset_index()
fig7 = px.scatter(top_customers,
                  x='Customer Name', y='Sales', title='Top 10 Customers by Sales',
                  color='Sales', color_continuous_scale=px.colors.sequential.Viridis, size='Sales')

fig8 = px.histogram(DF, x='Ship_Diff_Days', nbins=20, title='Shipping Delay (Days)', marginal='rug',
                    color_discrete_sequence=["#353CA1"])

fig9 = px.imshow(
    DF.pivot_table(index='Category', columns='Month', values='Sales', aggfunc='sum', fill_value=0).values,
    labels=dict(x="Month", y="Category", color="Sales"),
    x=list(range(1,13)),
    y=DF['Category'].unique(),
    title='Sales by Month and Category',
    color_continuous_scale='Viridis', text_auto=True)

fig10 = px.imshow(
    DF.pivot_table(index='Sub-Category', columns='Month', values='Sales', aggfunc='sum', fill_value=0).values,
    labels=dict(x="Month", y="Sub-Category", color="Sales"),
    x=list(range(1,13)),
    y=DF['Sub-Category'].unique(),
    title='Sales by Month and Sub-Category',
    color_continuous_scale='Cividis', text_auto=True)

quarter_sales = DF.groupby(["Year" ,"Quarter"])["Sales"].sum().reset_index()
fig11 = px.bar(quarter_sales, x='Quarter', y='Sales', color='Year', title='Quarterly Sales',
               color_continuous_scale=px.colors.sequential.Agsunset)

monthly_sales_year = DF.pivot_table(index='Year', columns='Month', values='Sales', aggfunc='sum', fill_value=0)
fig12 = px.bar(monthly_sales_year, barmode='group', title='Monthly Sales per Year',
               color_continuous_scale=px.colors.sequential.Agsunset)

# Dash App
app = Dash(__name__, external_stylesheets=[dbc.themes.FLATLY])

# Compute KPIs
date_range_text = f"From {DF['Order Date'].min().date()} to {DF['Order Date'].max().date()}"
total_sales = DF['Sales'].sum()
avg_ship_delay = DF['Ship_Diff_Days'].mean() if not DF.empty else 0
total_orders = len(DF)

app.layout = dbc.Container([
    html.H1('Sales Dashboard', style={'textAlign': 'center', 'marginBottom': '25px'}),
    html.H5(date_range_text, style={'textAlign': 'center', 'marginBottom': '30px', 'color': '#666'}),
    
    dbc.Row([
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3('Total Sales', className='card-title'),
                    html.H4(f"${total_sales:,.2f}", className='card-text', style={'fontWeight': 'bold'})
                ])
            ], color="primary", inverse=True, className="shadow-sm")
        ], md=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3('Avg Shipping Delay (Days)', className='card-title'),
                    html.H4(f"{avg_ship_delay:.1f}", className='card-text', style={'fontWeight': 'bold'})
                ])
            ], color="info", inverse=True, className="shadow-sm")
        ], md=4),
        dbc.Col([
            dbc.Card([
                dbc.CardBody([
                    html.H3('Total Orders', className='card-title'),
                    html.H4(f"{total_orders:,}", className='card-text', style={'fontWeight': 'bold'})
                ])
            ], color="success", inverse=True, className="shadow-sm")
        ], md=4),
    ], className="mb-4 justify-content-center"),

    dcc.Graph(figure=fig1),
    dcc.Graph(figure=fig2),
    dcc.Graph(figure=fig3),
    dcc.Graph(figure=fig4),
    html.Div([
        dcc.Graph(figure=fig5a, style={'display': 'inline-block', 'width': '49%'}),
        dcc.Graph(figure=fig5b, style={'display': 'inline-block', 'width': '49%'}),
    ]),
    dcc.Graph(figure=fig6),
    dcc.Graph(figure=fig7),
    dcc.Graph(figure=fig8),
    html.Div([
        dcc.Graph(figure=fig9, style={'display': 'inline-block', 'width': '49%'}),
        dcc.Graph(figure=fig10, style={'display': 'inline-block', 'width': '49%'}),
    ]),
    dcc.Graph(figure=fig11),
    dcc.Graph(figure=fig12),
], fluid=True)

if __name__ == '__main__':
    app.run(debug=True)

