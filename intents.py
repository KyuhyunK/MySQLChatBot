import plotly.express as px
from database import run_query
import re


def extract_year_and_quarter(question):
    year_match = re.search(r'202\d+', question)
    quarter_match = re.search(r'Q[1-4]', question)
    
    year = year_match.group(0) if year_match else None
    quarter = quarter_match.group(0)[1] if quarter_match else None  # Extract number only
    
    return year, quarter

intents = [
    {
        "tag": "total_revenue_by_state",
        "patterns": [
            "What is the total revenue by listing state?",
            "Show me the revenue for each state.",
            "How much revenue did each state generate?"
        ],
        "responses": [
            "The total revenue by listing state can be obtained by summing up the total_revenue column grouped by listing_state.",
            "You can find the revenue for each state by aggregating the total_revenue for each listing_state.",
            "To know the revenue generated by each state, you need to group the total_revenue by listing_state."
        ],
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
        "tag": "top_skus_by_profit",
        "patterns": [
            "Which are the top 10 SKUs by total profit?",
            "Show me the most profitable SKUs.",
            "Top SKUs in terms of profit."
        ],
        "responses": [
            "The top 10 SKUs by total profit can be found by ordering the total_profit column in descending order and limiting the result to 10.",
            "To see the most profitable SKUs, sort the total_profit in descending order and take the top 10 results.",
            "Identify the top SKUs by profit by ordering the total_profit column from highest to lowest and selecting the first 10 entries."
        ],
        "intent": "Compare Current and Previous Total Revenue",
        "patterns": ["compare current and previous total revenue", "current vs previous total revenue"]
    },
    {
        "tag": "monthly_revenue_trend",
        "patterns": [
            "Can you show me the monthly revenue trend?",
            "What is the revenue trend over the months?",
            "Revenue trend per month."
        ],
        "responses": [
            "The monthly revenue trend can be visualized by grouping total_revenue by each month.",
            "To see the revenue trend over the months, aggregate total_revenue by month and plot it.",
            "For a monthly revenue trend, sum up total_revenue for each month and display it as a time series."
        ],
        "intent": "Compare Current and Previous Total Profit",
        "patterns": ["compare current and previous total profit", "current vs previous total profit"]
    },
    {
        "tag": "top_asins_by_ordered_items",
        "patterns": [
            "What are the top 5 ASINs by total ordered items?",
            "Most ordered ASINs.",
            "Top ASINs by orders."
        ],
        "responses": [
            "The top 5 ASINs by total ordered items can be found by summing up the total_ordered_items column grouped by ASIN and selecting the top 5.",
            "To find the most ordered ASINs, aggregate total_ordered_items by ASIN and pick the top 5.",
            "The ASINs with the highest number of orders can be identified by grouping total_ordered_items by ASIN and taking the top 5 results."
        ],
        "intent": "Graph Total Revenue by SKU",
        "patterns": ["graph total revenue by SKU", "chart total revenue per SKU"]
    },
    {
        "tag": "revenue_diff_by_state",
        "patterns": [
            "Show the difference in revenue by listing state.",
            "Revenue change per state.",
            "Compare revenue differences among states."
        ],
        "responses": [
            "The difference in revenue by state can be calculated by summing the total_revenue_diff column grouped by listing_state.",
            "To compare revenue changes among states, aggregate the total_revenue_diff for each listing_state.",
            "You can see the revenue difference by state by summing up the total_revenue_diff grouped by listing_state."
        ],
        "intent": "Graph Total Profit by SKU",
        "patterns": ["graph total profit by SKU", "chart total profit per SKU"]
    },
    {
        "tag": "avg_selling_price_by_sku",
        "patterns": [
            "What is the average selling price by SKU?",
            "Show me the average price for each SKU.",
            "Average selling price for SKUs."
        ],
        "responses": [
            "The average selling price by SKU can be calculated by averaging the avg_selling_price column grouped by SKU.",
            "To find the average price for each SKU, group by SKU and take the average of avg_selling_price.",
            "You can determine the average selling price for each SKU by calculating the mean of avg_selling_price for each SKU."
        ],
        "intent": "Calculate Average Revenue",
        "patterns": ["calculate average revenue", "average revenue"]
    },
    {
        "tag": "profit_margin_analysis",
        "patterns": [
            "What is the profit margin for each SKU?",
            "Show me the profit margins.",
            "Analyze the profit margins."
        ],
        "responses": [
            "The profit margin for each SKU can be analyzed by averaging the profit_margin column grouped by SKU.",
            "To see the profit margins, group by SKU and calculate the average of profit_margin.",
            "Analyze the profit margins by calculating the mean of the profit_margin for each SKU."
        ],
        "intent": "Calculate Total Revenue Difference",
        "patterns": ["calculate total revenue difference", "total revenue difference"]
    },
    {
        "tag": "return_rate_by_sku",
        "patterns": [
            "What is the return rate by SKU?",
            "Show me the return rates for each SKU.",
            "Return rate analysis."
        ],
        "responses": [
            "The return rate by SKU can be found by averaging the return_rate column grouped by SKU.",
            "To see the return rates for each SKU, group by SKU and calculate the average of return_rate.",
            "You can analyze the return rate by calculating the mean of return_rate for each SKU."
        ],
        "intent": "SKU Details",
        "patterns": ["details for SKU", "SKU details"]
    },
    {
        "intent": "Revenue for a Specific Listing State",
        "patterns": ["revenue for listing state", "listing state revenue"]
    },
    {
        "tag": "evaluate_products",
        "patterns": [
            "Which products are worth buying again?",
            "Evaluate products based on return rates and profitability.",
            "Should I restock these products?"
        ],
        "responses": [
            "Evaluating products based on return rate and profitability.",
            "Let me analyze the return rates and profitability to determine the best products to restock.",
            "Analyzing products to see which are worth buying again based on returns and profits."
        ]
    },
    {
        "tag": "analyze_return_rate",
        "patterns": [
            "What is the optimal return rate threshold?",
            "Analyze return rates to find the optimal threshold.",
            "Determine the return rate threshold for profitability."
        ],
        "responses": [
            "Analyzing return rates to determine the optimal threshold.",
            "Let me calculate the return rate threshold for profitability.",
            "Calculating the best return rate threshold based on profitability."
        ]
    },
    {
        "tag": "compare_top_products",
        "patterns": [
            "Compare top products for 2023 and 2024",
            "Show me the top products for 2023 and 2024",
            "Which products were the best in 2023 and 2024?"
        ],
        "responses": [
            "Comparing the top products for 2023 and 2024 based on profit after returns, ordered items, and return items."
        ],
        "intent": "Compare Top Products for 2023 and 2024",
        "patterns": ["compare top products", "top products 2023 and 2024"]
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
    "cost_of_return", "total_referral_fees", "year", "quarter"
]

def handle_intent(intent, st):

    year, quarter = extract_year_and_quarter(question)

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

    elif intent == 'evaluate_products':
        df, _ = run_query("SELECT year, sku, SUM(total_profit) as total_profit, AVG(return_rate) as return_rate, SUM(profit_after_returns) as profit_after_returns FROM aggregate_profit_data GROUP BY year, sku;")
        df['profitability_score'] = df['profit_after_returns'] - (df['return_rate'] * df['total_profit'] / 100)
        threshold = df['profitability_score'].mean()
        st.write(f"Automatically determined profitability score threshold: {threshold:.2f}")
        df = df[df['profitability_score'] > threshold]
        st.dataframe(df)
        fig = px.scatter(df, x='return_rate', y='profit_after_returns', color='profitability_score', title='Return Rate vs Profit After Returns')
        st.plotly_chart(fig)

        st.subheader("Sentiment Analysis on Product Feedback")
        df['sentiment'] = df['feedback_text'].apply(lambda text: sentiment_analyzer(text)[0]['label'])
        st.dataframe(df[['sku', 'feedback_text', 'sentiment']])

    elif intent == 'analyze_return_rate':
        df, _ = run_query("SELECT year, sku, return_rate, SUM(total_profit) as total_profit FROM aggregate_profit_data GROUP BY year, sku;")
        df['return_rate_threshold'] = df['total_profit'] / df['return_rate']
        optimal_threshold = df['return_rate_threshold'].mean()
        st.write(f"Automatically determined return rate threshold: {optimal_threshold:.2f}")
        df = df[df['return_rate'] < optimal_threshold]
        st.dataframe(df)
        fig = px.scatter(df, x='return_rate', y='total_profit', color='return_rate_threshold', title='Return Rate vs Total Profit')
        st.plotly_chart(fig)

        st.subheader("Sentiment Analysis on Product Feedback")
        df['sentiment'] = df['feedback_text'].apply(lambda text: sentiment_analyzer(text)[0]['label'])
        st.dataframe(df[['sku', 'feedback_text', 'sentiment']])

    elif intent == 'Compare Top Products for 2023 and 2024':
        query_2023 = """
            SELECT 
                sku, 
                SUM(profit_after_returns::numeric) AS total_profit_after_returns_2023,
                SUM(total_ordered_items::numeric) AS total_ordered_items_2023,
                SUM(return_items::numeric) AS return_items_2023
            FROM 
                aggregate_profit_data
            WHERE 
                year = '2023' AND quarter IN ('1', '2')
            GROUP BY 
                sku
            ORDER BY 
                total_profit_after_returns_2023 DESC
            LIMIT 100;
        """
        
        query_2024 = """
            SELECT 
                sku, 
                SUM(profit_after_returns::numeric) AS total_profit_after_returns_2024,
                SUM(total_ordered_items::numeric) AS total_ordered_items_2024,
                SUM(return_items::numeric) AS return_items_2024
            FROM 
                aggregate_profit_data
            WHERE 
                year = '2024' AND quarter IN ('1', '2')
            GROUP BY 
                sku
            ORDER BY 
                total_profit_after_returns_2024 DESC
            LIMIT 100;
        """

        df_2023, _ = run_query(query_2023)
        df_2024, _ = run_query(query_2024)

        st.write("### Top 100 SKUs for 2023")
        st.dataframe(df_2023)

        st.write("### Top 100 SKUs for 2024")
        st.dataframe(df_2024)

        st.write("### Comparison of Top 100 SKUs for 2023 and 2024")
        fig = px.bar(df_2023, x='sku', y='total_profit_after_returns_2023', title='Top 100 SKUs for 2023')
        st.plotly_chart(fig)

        fig = px.bar(df_2024, x='sku', y='total_profit_after_returns_2024', title='Top 100 SKUs for 2024')
        st.plotly_chart(fig)
