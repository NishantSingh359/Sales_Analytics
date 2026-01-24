import pandas as pd

def create_date_dimension(start_date:str, end_date:str) -> pd.DataFrame:
    dates = pd.date_range(start=start_date, end=end_date, freq='D')

    df = pd.DataFrame({'full_date': dates})

    df['date_key'] = df['full_date'].dt.strftime('%Y%m%d').astype(int) #type: ignore
    df['year'] = df['full_date'].dt.year #type: ignore
    df['quarter'] = df['full_date'].dt.quarter #type: ignore
    df['month'] = df['full_date'].dt.month #type: ignore
    df['month_name'] = df['full_date'].dt.month_name() #type: ignore
    df['week'] = df['full_date'].dt.isocalendar().week #type: ignore
    df['day'] = df['full_date'].dt.day #type: ignore
    df['day_name'] = df['full_date'].dt.day_name() #type: ignore
    df['is_weekend'] = df['day_name'].isin(['Saturday', 'Sunday'])

    return df

if __name__ == '__main__':
    sales = pd.read_csv(r"data\sales.csv")
    start_date:str = sales['order_date'].min()
    end_date:str = sales['order_date'].max()
    df = create_date_dimension(start_date, end_date)
    df.to_csv(r"data\dim_date.csv", index=False)