import pandas as pd

class KPIs:
    def __init__(self, df:pd.DataFrame):
        self.df = df

class SalesKPIs(KPIs):

    def total_revenue(self) -> float:
        return self.df['amount'].sum()
         
    def total_quantity(self) -> int:
        return self.df['quantity'].sum()
    
    def total_orders(self) -> int:
        return self.df['order_number'].nunique()
    
    def avg_order_value(self) -> float:
        return self.total_revenue() / self.total_orders()
    
    def avg_order_quantity(self) -> float:
        return self.total_quantity() / self.total_orders()

    def avg_shipping_time(self):
        return (self.df['ship_date'] - self.df['order_date']).mean()

    def avg_delivery_time(self):
        return (self.df['delivery_date'] - self.df['order_date']).mean()
    
    def avg_shipping_to_delivery_time(self):
        return (self.df['delivery_date'] - self.df['ship_date']).mean()

    def revenue_by_year(self) -> pd.DataFrame:
        return (
            self.df.groupby("year", as_index=False)["amount"]
            .sum()
            .rename(columns={"amount": "total_revenue"})
        ) # type: ignore
    
    def revenue_by_month(self) -> pd.DataFrame:
        return (
            pd.pivot_table(data=self.df, index= ['month','month_name'], columns=['year'], values='amount', aggfunc='sum')
            .reset_index()
            .drop('month', axis=1)
        ) # type: ignore
    
    def profit_by_year(self) -> pd.DataFrame:
        df = self.df.pivot_table(index=['year'], values=['cost', 'price'], aggfunc='sum')
        df.reset_index(inplace=True)
        df['profit'] = df['price'] - df['cost']
        return df[['year', 'profit']]

    def profit_by_month(self) -> pd.DataFrame:
        df = self.df.pivot_table(index=['month', 'month_name'], columns=['year'], values=['cost', 'price'], aggfunc='sum')
        df = df.reset_index()
        df1 = pd.DataFrame()
        df1['month_name'] = df['month_name']
        df1[2011] = df['price'][2011] - df['cost'][2011]
        df1[2012] = df['price'][2012] - df['cost'][2012]
        df1[2013] = df['price'][2013] - df['cost'][2013]
        return df1
    
    def last_year_mom_growth_r(self) -> pd.DataFrame:
        df = self.df.groupby(['year', 'month', 'month_name'], as_index=False)["amount"].sum()
        df = df[df['year'] == df['year'].max()-1][['month_name', 'amount']]
        df['mom'] = ((df['amount'] - df['amount'].shift(1))/df['amount'].shift(1)*100).round(2)
        df = df[['month_name', 'mom']]
        return df
    
    def yoy_growth_r(self) -> pd.DataFrame:

        # Count month per year 
        df = self.df.groupby('year', as_index=False)["month"].nunique()
        year = df['year'][df['month'] == 12] # type: ignore

        # Keep only complete years
        df = self.df.groupby('year', as_index=False)["amount"].sum()
        df = df[df['year'].isin(year)]

        # Calculate YoY Growth
        df['yoy'] = ((df['amount'] - df['amount'].shift(1))/df['amount'].shift(1)*100).round(2)
        df = df[['year', 'yoy']]
        return df

    def last_year_mom_growth_p(self):
        df = self.profit_by_month()
        df['mom'] = (df[2013]-df[2013].shift(1))/df[2013].shift(1)*100
        return df[['month_name', 'mom']]

    def yoy_growth_p(self):
        df = self.df.groupby('year', as_index=False)["month"].nunique()
        year = df['year'][df['month'] == 12] # type: ignore
        df = self.profit_by_year()
        df = df[df['year'].isin(year)]
        df['yoy'] = ((df['profit'] - df['profit'].shift(1))/df['profit'].shift(1)*100).round(2)
        return df[['year', 'yoy']]
    
    def revenue_profit_by_country(self) -> pd.DataFrame:
        df = self.df.groupby('country', as_index=False)[['cost', 'price', 'amount']].sum()
        df['profit'] = df['price'] - df['cost']
        return (
            df[['country', 'profit', 'amount']]
            .sort_values('amount', ascending=False)
            .rename(columns={'amount': 'revenue'})
        )

class CustomerKPIs(KPIs):
    def total_customer(self) -> int:
        return self.df['customer_key'].nunique()
    
    def customer_avg_order(self) -> float:
        df = self.df.groupby('customer_key', as_index= False)['customer_key'].count()
        return df['customer_key'].mean()
    
    def customer_avg_order_value(self) -> float:
        df = self.df.groupby('customer_key', as_index=False)['amount'].sum()
        return df['amount'].mean()

    def customer_repeat_rate(self) -> float:
        df = self.df.groupby('customer_key', as_index=False)['customer_key'].count()
        repeat_customer = df[df['customer_key'] >1]
        return len(repeat_customer)/self.total_customer()*100 # type: ignore

    def purchase_frequency(self) -> float:
        return SalesKPIs(self.df).total_orders()/self.total_customer()

    def customer_across_country(self) -> pd.DataFrame:
        return (
                self.df.groupby('country', as_index=False)['customer_key']
                .nunique()
                .sort_values('customer_key', ascending=False) #type:ignore
                .rename(columns={'customer_key':'total_customer'})
        ) 
    
    def revenue_by_customer_age_group(self) -> pd.DataFrame:
        return (
            self.df.groupby('age_group', as_index=False)['amount']
            .sum()
            .sort_values("amount", ascending=False) #type: ignore
            .rename(columns={'amount':'revenue'})
        ) 

    def customer_by_gender(self) -> pd.DataFrame:
        df = self.df.groupby('gender', as_index=False)['customer_key'].nunique()
        df['percentage'] = df['customer_key']/self.total_customer()*100
        return  df[['gender', 'percentage']] # type:ignore


    def revenue_by_gender_marital_status(self):
        return (
            self.df.pivot_table(index='gender', columns='marital_status', values='amount', aggfunc='sum')
        )
    
    def customer_revenue(self) -> pd.DataFrame:
        return (
            self.df.groupby("customer_key", as_index=False)["amount"]
            .sum()
            .sort_values("amount", ascending=False) # type: ignore
            .rename(columns={"amount": "customer_revenue"})
        ) 

    def customer_order_counts(self) -> pd.DataFrame:
        return (
            self.df.groupby("customer_key", as_index=False)["order_number"]
            .nunique()
            .rename(columns={"order_number": "order_count"})
        ) # type: ignore
    
class ProductKPIs(KPIs):

    def top_products_by_revenue(self, n: int = 10) -> pd.DataFrame:
        return (
            self.df.groupby("product_name", as_index=False)["amount"]
            .sum()
            .sort_values("amount", ascending=False) # type: ignore
            .head(n)
        ) 
    
    def category_by_revenue(self) -> pd.DataFrame:
        return (
            self.df.groupby('category', as_index=False)['amount']
            .sum()
            .sort_values('amount', ascending=False) # type: ignore
            .rename(columns={'amount':'revenue'})               
        ) 
    
    def product_sales_volume(self) -> pd.DataFrame:
        return (
            self.df.groupby("product_name", as_index=False)["quantity"]
            .sum()
            .rename(columns={"quantity": "total_quantity"})
        ) # type: ignore
    
    def category_and_subcategory_by_revenue(self) -> pd.DataFrame:
        return (
            self.df.groupby(['category', 'subcategory'], as_index=False)['amount']
            .sum()
            .sort_values(['category', 'amount']) # type: ignore
            .rename(columns={'amount': 'revenue'})
        )

    def top_product_by_cost(self) -> pd.DataFrame:
        return (
            self.df.groupby(['product_name'], as_index=False)['amount']
            .sum()
            .sort
        )

    def product_by_profit(self) -> pd.DataFrame:
        df = self.df.groupby('product_name', as_index=False)[['cost', 'price']].max()
        df['profit'] = df['price'] - df['cost']
        df = df.sort_values('profit', ascending=False)
        return df[['product_name', 'profit']]


