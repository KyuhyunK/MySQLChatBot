import pandas as pd

def extract_price_from_notes(note):
    match = re.search(r'\$\d+(\.\d{2})?', note)
    return float(match.group().replace('$', '')) if match else None

def evaluate_product(data, return_rate_threshold=5):
    recommendations = []
    
    for index, row in data.iterrows():
        if row['return_rate'] < return_rate_threshold and row['profit_after_returns'] > 0:
            recommendations.append({
                'sku': row['sku'],
                'asin': row['asin'],
                'total_profit': row['total_profit'],
                'profit_after_returns': row['profit_after_returns'],
                'return_rate': row['return_rate'],
                'profit_margin': row['profit_margin'],
                'roi': row['roi']
            })
    
    return recommendations

def find_critical_return_rate(data):
    for rate in range(1, 21):  # Checking return rates from 1% to 20%
        recommendations = evaluate_product(data, return_rate_threshold=rate)
        if not recommendations:
            return rate - 1
    return 20  # All products are worth it until 20% return rate

def process_csv(file_path):
    data = pd.read_csv(file_path)
    
    # Apply evaluation logic
    recommendations = evaluate_product(data)
    critical_return_rate = find_critical_return_rate(data)
    
    return recommendations, critical_return_rate

def evaluate_products_intent():
    file_path = config.FILE_PATH  # Update with the actual path
    recommendations, critical_return_rate = process_csv(file_path)
    
    response = f"The critical return rate threshold is {critical_return_rate}%. Based on the analysis, here are the products worth buying again:\n"
    if recommendations:
        for rec in recommendations:
            response += (f"SKU: {rec['sku']}, ASIN: {rec['asin']}, Total Profit: {rec['total_profit']}, "
                         f"Profit After Returns: {rec['profit_after_returns']}, Return Rate: {rec['return_rate']}%, "
                         f"Profit Margin: {rec['profit_margin']}%, ROI: {rec['roi']}\n")
    else:
        response += "No products meet the criteria for re-purchase."
    
    return response
