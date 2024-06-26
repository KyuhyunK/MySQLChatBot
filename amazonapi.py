import requests
import json
from config import RAPIDAPI_KEY


def validate_sql_columns(sql_query, valid_columns):
    sql_keywords = {'SELECT', 'AS', 'FROM', 'WHERE', 'GROUP', 'BY', 'ORDER', 'DESC', 'LIMIT', 'SUM', 'AVG', 'COUNT'}
    sql_query_columns = [word.strip('`,') for word in sql_query.split() if word.strip('`,').isalpha() and word.upper() not in sql_keywords]
    invalid_columns = [col for col in sql_query_columns if col.lower() not in [col.lower() for col in valid_columns]]
    corrected_query = sql_query
    for invalid_col in invalid_columns:
        if invalid_col == 'revenue':
            corrected_query = corrected_query.replace('revenue', 'total_revenue')
        # Add more replacements if necessary
    return corrected_query


def invoke_amazon_api(endpoint, params):
    url = f"https://ai-query2.p.rapidapi.com/{endpoint}"
    headers = {
        "X-RapidAPI-Key": RAPIDAPI_KEY,
        "X-RapidAPI-Host": "ai-query2.p.rapidapi.com",
        "Content-Type": "application/json"
    }
    data = {
    "prompt": "Show me the listing state, cost, quantity, and revenue-related metrics for all products in the past quarter",
    "model": "oa_v3_16k",
    "data_source_type": "postgresql",
    "data_schema": [
        {
            "table_name": "products",
            "columns": [
                {"name": "id", "type": "text", "description": "Unique identifier for each record"},
                {"name": "sku", "type": "text", "description": "Stock Keeping Unit, unique identifier for each product"},
                {"name": "asin", "type": "text", "description": "Amazon Standard Identification Number, unique identifier for Amazon products"},
                {"name": "listing_state", "type": "text", "description": "State of the listing (e.g., active, inactive)"},
                {"name": "cost", "type": "text", "description": "Cost of the item"},
                {"name": "quantity", "type": "text", "description": "Number of units available"},
                {"name": "min_price", "type": "text", "description": "Minimum price of the item"},
                {"name": "max_price", "type": "text", "description": "Maximum price of the item"},
                {"name": "listed_price", "type": "text", "description": "Price at which the item is listed"},
                {"name": "avg_selling_price", "type": "text", "description": "Average selling price of the item"},
                {"name": "total_revenue", "type": "text", "description": "Total revenue generated by the item"},
                {"name": "total_revenue_prev", "type": "text", "description": "Previous period total revenue"},
                {"name": "total_revenue_diff", "type": "text", "description": "Difference in revenue between periods"},
                {"name": "total_profit", "type": "text", "description": "Total profit generated by the item"},
                {"name": "total_profit_prev", "type": "text", "description": "Previous period total profit"},
                {"name": "total_profit_diff", "type": "text", "description": "Difference in profit between periods"},
                {"name": "total_ordered_items", "type": "text", "description": "Total number of items ordered"},
                {"name": "profit_margin", "type": "text", "description": "Profit margin for the item"},
                {"name": "roi", "type": "text", "description": "Return on investment"},
                {"name": "fba_inbound_quantity", "type": "text", "description": "Quantity of items inbound to FBA (Fulfillment by Amazon)"},
                {"name": "pkg_weight", "type": "text", "description": "Package weight"},
                {"name": "pkg_length", "type": "text", "description": "Package length"},
                {"name": "pkg_width", "type": "text", "description": "Package width"},
                {"name": "pkg_height", "type": "text", "description": "Package height"},
                {"name": "pkg_volume", "type": "text", "description": "Package volume"},
                {"name": "return_rate", "type": "text", "description": "Rate of item returns"},
                {"name": "profit_after_returns", "type": "text", "description": "Profit after accounting for returns"},
                {"name": "revenue_after_returns", "type": "text", "description": "Revenue after accounting for returns"},
                {"name": "return_items", "type": "text", "description": "Number of items returned"},
                {"name": "cost_of_returns", "type": "text", "description": "Cost associated with returns"},
                {"name": "profit_margin_at_min", "type": "text", "description": "Profit margin at minimum price"},
                {"name": "profit_margin_at_max", "type": "text", "description": "Profit margin at maximum price"},
                {"name": "fulfillment_fee", "type": "text", "description": "Fee for fulfillment services"},
                {"name": "amazon_fees", "type": "text", "description": "Fees charged by Amazon"},
                {"name": "net_proceeds", "type": "text", "description": "Net proceeds after fees"},
                {"name": "total_COGS", "type": "text", "description": "Total cost of goods sold"},
                {"name": "total_fulfillment_fees", "type": "text", "description": "Total fulfillment fees"},
                {"name": "total_return_processing_fees", "type": "text", "description": "Total return processing fees"},
                {"name": "returned_items_cost", "type": "text", "description": "Cost of returned items"},
                {"name": "cost_of_return", "type": "text", "description": "Cost incurred for returning items"},
                {"name": "total_referral_fees", "type": "text", "description": "Total referral fees"},
                {"name": "year", "type": "text", "description": "Year that data was pulled from"},
                {"name": "quarter", "type": "text", "description": "Quarter that data was pulled from"}
            ]
        }
    ]
}
    response = requests.post(url, headers=headers, json=params)
    response.raise_for_status() 
    return response.json()

def invoke_amazon_response(prompt):
    endpoint = "optimize_sql_query"
    params = {"prompt": prompt, "model": "oa_v3_16k", "data_source_type": "postgresql"}
    data = invoke_amazon_api(endpoint, params)
    return data



def invoke_chain(user_question, valid_columns):
    # Prepare the prompt for generating the SQL query
    sql_query_prompt = f"Generate a SQL query for the following question: {user_question}. The default table name is 'aggregate_profit_data', unless specified otherwise use this table name. Ensure the query includes the table name and the 'FROM' keyword. Use only valid columns from the following list: {', '.join(valid_columns)}. Keep your response concise and easy to understand."
    
    # Use the Amazon API to generate the SQL query
    params = {
        "prompt": sql_query_prompt,
        "model": "oa_v3_16k",
        "data_source_type": "postgresql"
    }
    response = invoke_amazon_api("generate_sql", params)
    
    generated_sql_query = response.get('result', '')

    print("Generated SQL Query:", generated_sql_query)

    # Validate and correct the SQL query if needed
    corrected_sql_query = validate_sql_columns(generated_sql_query, valid_columns)

    return corrected_sql_query


