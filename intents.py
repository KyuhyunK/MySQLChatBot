import plotly.express as px
from database import run_query

intents = [
    {
        "intent": "Get Total Revenue by SKU",
        "patterns": ["total revenue by SKU", "total revenue per SKU"]
    },
    {
        "intent": "Get Total Profit by SKU",
        "patterns": ["total profit by SKU", "total profit per SKU"]
    },
    {
        "intent": "Get Total Ordered Items by SKU",
        "patterns": ["total ordered items by SKU", "total items ordered per SKU"]
    },
    {
        "intent": "Compare Current and Previous Total Revenue",
        "patterns": ["compare current and previous total revenue", "current vs previous total revenue"]
    },
    {
        "intent": "Compare Current and Previous Total Profit",
        "patterns": ["compare current and previous total profit", "current vs previous total profit"]
    },
    {
        "intent": "Graph Total Revenue by SKU",
        "patterns": ["graph total revenue by SKU", "chart total revenue per SKU"]
    },
    {
        "intent": "Graph Total Profit by SKU",
        "patterns": ["graph total profit by SKU", "chart total profit per SKU"]
    },
    {
        "intent": "Calculate Average Revenue",
        "patterns": ["calculate average revenue", "average revenue"]
    },
    {
        "intent": "Calculate Total Revenue Difference",
        "patterns": ["calculate total revenue difference", "total revenue difference"]
    },
    {
        "intent": "SKU Details",
        "patterns": ["details for SKU", "SKU details"]
    },
    {
        "intent": "Revenue for a Specific Listing State",
        "patterns": ["revenue for listing state", "listing state revenue"]
    }
]

valid_columns = [
    "id", "sku", "asin", "listing_state", "cost", "quantity", "min_price", "max_price",
    "listed_price", "avg_selling_price", "total_revenue", "total_revenue_prev", "total_revenue_diff",
    "total_profit", "total_profit_prev", "total_profit_diff", "total_ordered_items", "profit_margin",
    "roi", "fba_inbound_quantity", "pkg_weight", "pkg_length", "pkg_width", "pkg_height", "pkg_volume",
    "return_rate", "profit_after_returns", "revenue_after_returns", "return_items", "cost_of_returns",
    "profit_margin_at_min", "profit_margin_at_max", "fulfillment_fee", "amazon_fees", "net_proceeds",
    "total_COGS", "total_fulfillment_fees", "total_return_processing_fees", "returned_items_cost",
    "cost_of_return", "total_referral_fees"
]

def handle_intent(intent, st):
    if intent == 'Get Total Revenue by SKU':
        df, _ = run_query("SELECT sku, total_revenue FROM aggregate_profit_data ORDER BY total_revenue DESC;")
        st.dataframe(df)
    
    elif intent == 'Get Total Profit by SKU':
        df, _ = run_query("SELECT sku, total_profit FROM aggregate_profit_data ORDER BY total_profit DESC;")
        st.dataframe(df)
    
    elif intent == 'Get Total Ordered Items by SKU':
        df, _ = run_query("SELECT sku, total_ordered_items FROM aggregate_profit_data ORDER BY total_ordered_items DESC;")
        st.dataframe(df)
    
    elif intent == 'Compare Current and Previous Total Revenue':
        df, _ = run_query("SELECT sku, total_revenue, total_revenue_prev FROM aggregate_profit_data ORDER BY total_revenue DESC;")
        st.dataframe(df)
    
    elif intent == 'Compare Current and Previous Total Profit':
        df, _ = run_query("SELECT sku, total_profit, total_profit_prev FROM aggregate_profit_data ORDER BY total_profit DESC;")
        st.dataframe(df)
    
    elif intent == 'Graph Total Revenue by SKU':
        df, _ = run_query("SELECT sku, total_revenue FROM aggregate_profit_data ORDER BY total_revenue DESC LIMIT 10;")
        fig = px.bar(df, x='sku', y='total_revenue', title='Total Revenue by SKU')
        st.plotly_chart(fig)
    
    elif intent == 'Graph Total Profit by SKU':
        df, _ = run_query("SELECT sku, total_profit FROM aggregate_profit_data ORDER BY total_profit DESC LIMIT 10;")
        fig = px.bar(df, x='sku', y='total_profit', title='Total Profit by SKU')
        st.plotly_chart(fig)
    
    elif intent == 'Calculate Average Revenue':
        df, _ = run_query("SELECT AVG(total_revenue) as average_revenue FROM aggregate_profit_data;")
        st.dataframe(df)
    
    elif intent == 'Calculate Total Revenue Difference':
        df, _ = run_query("SELECT sku, total_revenue_diff FROM aggregate_profit_data ORDER BY total_revenue_diff DESC;")
        st.dataframe(df)
    
    elif intent == 'SKU Details':
        df, _ = run_query("SELECT * FROM aggregate_profit_data WHERE sku = 'example_sku';")
        st.dataframe(df)
    
    elif intent == 'Revenue for a Specific Listing State':
        df, _ = run_query("SELECT listing_state, total_revenue FROM aggregate_profit_data WHERE listing_state = 'example_state';")
        st.dataframe(df)
