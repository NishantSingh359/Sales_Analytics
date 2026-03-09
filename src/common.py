import pandas as pd

def standardize_dates(df:pd.DataFrame, date_cols:list[str]) -> pd.DataFrame:
    """Change object type date to datetime type.
    """
    for col in date_cols:
        df[col] = pd.to_datetime(df[col], errors='coerce')
    return df

def fact_sales() -> pd.DataFrame:
    """Left join tables.
       (sales, customer, product, dim_date)
    """
    sales = pd.read_csv(r"C:\Users\TUF\OneDrive\Documents\Code\Vs Code\sales_analytics\data\gold\sales.csv")
    customer = pd.read_csv(r"C:\Users\TUF\OneDrive\Documents\Code\Vs Code\sales_analytics\data\gold\customer.csv")
    product = pd.read_csv(r"C:\Users\TUF\OneDrive\Documents\Code\Vs Code\sales_analytics\data\gold\product.csv")
    dim_date = pd.read_csv(r"C:\Users\TUF\OneDrive\Documents\Code\Vs Code\sales_analytics\data\dim\dim_date.csv")

    df = sales.merge(customer, on='customer_key', how='left')
    df = df.merge(product, on='product_key', how='left')
    df = df.merge(dim_date, on='date_key', how='left')

    df['revenue'] = df['amount']
    df['profit'] = df['revenue'] - (df['cost'] * df['quantity'])
    
    return standardize_dates(df, ['order_date', 'ship_date', 'delivery_date'])

def format_number(value):
    if value >= 1000000000:
        return f"{value/1000000000:.1f}B"
    elif value >= 1000000:
        return f"{value/1000000:.1f}M"
    elif value >= 1000:
        return f"{value/1000:.1f}K"
    else:
        return f"{value:.1f}"
    
def chart_format_number(value, pos):
    if value >= 1000000000:
        return f"{value/1000000000:.1f}B"
    elif value >= 1000000:
        return f"{value/1000000:.1f}M"
    elif value >= 1000:
        return f"{value/1000:.1f}K"
    else:
        return f"{value:.1f}"