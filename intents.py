import plotly.express as px
from database import run_query
import re


def extract_year_and_quarter(question):
    year_match = re.findall(r'202\d+', question)
    quarter_match = re.findall(r'Q[1-4]', question)
    
    years = year_match if year_match else []
    quarters = [q[1] for q in quarter_match] if quarter_match else ['1', '2', '3', '4'] 
    
    return years, quarters

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
            "Compare top products for different years and quarters",
            "Show me the top products for various periods",
            "Which products were the best over different times?",
            "compare top products", 
            "compare the top products of 2023 and 2024"
        ],
        "responses": [
            "Comparing the top products based on profit after returns, ordered items, and return items."
        ]
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

def generate_best_sellers_query(years, quarters):
    queries = []
    performance_queries = []
    for i in range(len(years)):
        year = years[i]
        quarter = quarters[i]

        queries.append(f"""
            Best_Sellers_{year}_Q{quarter} AS (
                SELECT 
                    sku, 
                    SUM(profit_after_returns::numeric) AS total_profit_after_returns_{year},
                    SUM(total_ordered_items::numeric) AS total_ordered_items_{year},
                    SUM(return_items::numeric) AS return_items_{year}
                FROM 
                    aggregate_profit_data
                WHERE 
                    year = '{year}' AND quarter = '{quarter}'
                GROUP BY 
                    sku
                ORDER BY 
                    total_ordered_items_{year} DESC
                LIMIT 100
            )
        """)

        if i < len(years) - 1:
            next_year = years[i + 1]
            next_quarter = quarters[i + 1]

            performance_queries.append(f"""
                Performance_{year}_in_{next_year}_Q{next_quarter} AS (
                    SELECT 
                        s.sku, 
                        SUM(s.profit_after_returns::numeric) AS total_profit_after_returns_{next_year},
                        SUM(s.total_ordered_items::numeric) AS total_ordered_items_{next_year},
                        SUM(s.return_items::numeric) AS return_items_{next_year}
                    FROM 
                        aggregate_profit_data s
                    WHERE 
                        s.year = '{next_year}' AND s.quarter = '{next_quarter}' 
                        AND s.sku IN (SELECT sku FROM Best_Sellers_{year}_Q{quarter})
                    GROUP BY 
                        s.sku
                )
            """)

    combined_query = f"""
        WITH {', '.join(queries + performance_queries)}
        SELECT 
            b.sku,
            {', '.join([f"b.total_profit_after_returns_{years[j]} AS total_profit_after_returns_{years[j]}" for j in range(len(years))])},
            {', '.join([f"b.total_ordered_items_{years[j]} AS total_ordered_items_{years[j]}" for j in range(len(years))])},
            {', '.join([f"b.return_items_{years[j]} AS return_items_{years[j]}" for j in range(len(years))])},
            {', '.join([f"COALESCE(p.total_profit_after_returns_{years[j+1]}, 0) AS total_profit_after_returns_{years[j+1]}" for j in range(len(years)-1)])},
            {', '.join([f"COALESCE(p.total_ordered_items_{years[j+1]}, 0) AS total_ordered_items_{years[j+1]}" for j in range(len(years)-1)])},
            {', '.join([f"COALESCE(p.return_items_{years[j+1]}, 0) AS return_items_{years[j+1]}" for j in range(len(years)-1)])}
        FROM 
            Best_Sellers_{years[0]}_Q{quarters[0]} b
        LEFT JOIN 
            {', '.join([f"Performance_{years[j]}_in_{years[j+1]}_Q{quarters[j+1]} p ON b.sku = p.sku" for j in range(len(years)-1)])}
        ORDER BY 
            b.sku;
    """

    return combined_query

def handle_intent(intent, st, question):
    years, quarters = extract_year_and_quarter(question)
    if not years:
        st.write("Please specify the years in the question.")
        return

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
        df, _ = run_query("SELECT AVG(total_revenue::numeric) as average_revenue FROM aggregate_profit_data;")
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
        df, _ = run_query("SELECT year, sku, SUM(total_profit::numeric) as total_profit, AVG(return_rate::numeric) as return_rate, SUM(profit_after_returns::numeric) as profit_after_returns FROM aggregate_profit_data GROUP BY year, sku;")
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
        df, _ = run_query("SELECT year, sku, return_rate::numeric, SUM(total_profit::numeric) as total_profit FROM aggregate_profit_data GROUP BY year, sku;")
        positive_profit_df = df[df['total_profit'] > 0]
        avg_return_rate = positive_profit_df['return_rate'].mean()
        df['return_rate_label'] = df['return_rate'].apply(lambda x: 'Below Threshold' if x < avg_return_rate else 'Above Threshold')
        st.write(f"Automatically determined average return rate threshold: {avg_return_rate:.2f}")
        st.dataframe(df)
        fig = px.scatter(df, x='return_rate', y='total_profit', color='return_rate_label', title='Return Rate vs Total Profit')
        st.plotly_chart(fig)

    elif intent == 'compare_top_products':
        if len(years) >= 2 and len(quarters) <= 4:
            query = generate_best_sellers_query()
            df, _ = run_query(query)
            st.write(f"### Comparison of Best Sellers for Specified Years and Quarters")
            st.dataframe(df)
            
            for year in years:
                for quarter in quarters:
                    if f'total_profit_after_returns_{year}' in df.columns and f'total_ordered_items_{year}' in df.columns:
                        fig = px.bar(df, x='sku', y=[f'total_profit_after_returns_{year}', f'total_ordered_items_{year}'], title=f'Comparison for {year} Q{quarter}')
                        st.plotly_chart(fig)
                        fig = px.bar(df, x='sku', y=[f'return_items_{year}'], title=f'Return Items Comparison for {year} Q{quarter}')
                        st.plotly_chart(fig)
        else:
            st.write("Please specify at least two years and up to four quarters in the question.")
    else:
        st.write("Unsupported intent")