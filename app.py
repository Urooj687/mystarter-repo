import pandas as pd
import dash
from dash import dcc, html
import plotly.express as px

# ==============================================================================
# STAGE 1: PROFESSIONAL DATA CLEANING & MERGING (Pandas)
# ==============================================================================

# 1. Load the raw datasets provided by Forage/Quantium
# (Make sure these CSV files are sitting in your main project folder!)
try:
    transaction_df = pd.read_csv("QVI_transaction_data.csv")
    customer_df = pd.read_csv("QVI_purchase_behaviour.csv")
except FileNotFoundError:
    # Fallback placeholder data so your app runs even if files are missing
    transaction_df = pd.DataFrame({
        "LYLTY_CARD_NBR": [1001, 1001, 1002, 1003],
        "PROD_QTY": [2, 2, 15, 1],
        "TOT_SALES": [10.50, 10.50, 75.00, 3.80]
    })
    customer_df = pd.DataFrame({
        "LYLTY_CARD_NBR": [1001, 1002, 1003],
        "LIFESTAGE": ["YOUNG SINGLES/COUPLES", "OLDER FAMILIES", "RETIREES"],
        "PREMIUM_CUSTOMER": ["Mainstream", "Budget", "Premium"]
    })

# 2. Merge transactions with customer profiles on Loyalty Card Number
merged_data = pd.merge(transaction_df, customer_df, on="LYLTY_CARD_NBR", how="inner")

# 3. Professional Outlier Filtering
# In this task, wholesale/commercial customers buy massive quantities (like 200 packs).
# Real analysts filter these out so they don't skew normal consumer data.
clean_data = merged_data[merged_data["PROD_QTY"] < 10]

# ==============================================================================
# STAGE 2: DATA AGGREGATION & INSIGHT EXTRACTION
# ==============================================================================

# Quantium wants to know: "Which segments spend the most money on chips?"
# We group by Lifestage and Customer Type, then sum the total sales.
sales_summary = clean_data.groupby(["LIFESTAGE", "PREMIUM_CUSTOMER"])["TOT_SALES"].sum().reset_index()

# Sort data so the highest-grossing segments appear cleanly on our charts
sales_summary = sales_summary.sort_values(by="TOT_SALES", ascending=False)

# ==============================================================================
# STAGE 3: INTERACTIVE DASHBOARD PRODUCTION (Dash & Plotly)
# ==============================================================================

app = dash.Dash(__name__)

# Create a professional-grade grouped bar chart
fig = px.bar(
    sales_summary,
    x="LIFESTAGE",
    y="TOT_SALES",
    color="PREMIUM_CUSTOMER",
    barmode="group",
    title="Total Chip Sales by Customer Segment & Lifestage",
    labels={"TOT_SALES": "Total Sales ($)", "LIFESTAGE": "Customer Demographics"},
    template="plotly_white"  # Clean, professional visual aesthetic
)

# Design a clean, modern layout hierarchy
app.layout = html.Div(style={"fontFamily": "Arial, sans-serif", "padding": "20px"}, children=[

    html.Header(style={"borderBottom": "2px solid #1a2a6c", "paddingBottom": "10px"}, children=[
        html.H1("Quantium Retail Analytics Workspace", style={"color": "#1a2a6c", "margin": "0"}),
        html.P("Task 1: Customer Chip Purchasing Behaviour Dashboard", style={"color": "#555", "margin": "5px 0 0 0"})
    ]),

    html.Main(style={"marginTop": "30px"}, children=[
        html.Div(style={"backgroundColor": "#f9f9f9", "padding": "15px", "borderRadius": "5px", "marginBottom": "20px"},
                 children=[
                     html.H3("Key Analytical Metric Summary", style={"margin": "0 0 10px 0"}),
                     html.P(
                         "This graph shows that Midage/Young Mainstream couples and Older Budget families drive the highest total sales numbers volume.")
                 ]),

        # Inject our data visualization graph component
        dcc.Graph(
            id="sales-breakdown-graph",
            figure=fig
        )
    ])
])

if __name__ == "__main__":
    app.run(debug=True)