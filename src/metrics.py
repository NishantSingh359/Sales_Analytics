import pandas as pd

class KPIs:
    def __init__(self, df:pd.DataFrame):
        self.df = df

class SalesKPIs(KPIs):

    def total_orders(self) -> int:
        return self.df['order_number'].nunique()
    
    def total_revenue(self) -> float:
        return self.df['revenue'].sum()
             
    def total_profit(self) -> float:
        return self.df['profit'].sum()
    
    def total_unit_sold(self) -> int:
        return self.df['quantity'].sum()
    
    def avg_order_value(self) -> float:
        return self.total_revenue() / self.total_orders()
    
    def avg_selling_price(self) -> float:
        return self.df['revenue'].sum() / self.df['quantity'].sum()

    def avg_unit_per_order(self) -> float:
        return self.df.groupby('order_number')['quantity'].sum().mean()

    def profit_margin(self) -> float:
        return  self.total_profit() / self.total_revenue() * 100

    def avg_delivery_time(self):
        return (self.df['delivery_date'] - self.df['order_date']).mean()
    
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
    
    def revenue_and_profit_by_country(self) -> pd.DataFrame:
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
    
    def avg_order_per_customer(self) -> float:
        return self.df.groupby('customer_key', as_index= False)['customer_key'].count().mean()
    
    def avg_revenue_per_customer(self) -> float:
        return self.df.groupby('customer_key', as_index=False)['revenue'].sum().mean()

    def customer_lifetime_value(self) -> float:
        return self.df.groupby('customer_key')['revenue'].sum().mean()

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
    
class ProductKPIs(KPIs):

# Product-Level Metrics

    def revenue_per_product(self) -> pd.DataFrame:
        return (
            self.df.groupby('product_key', as_index=False)['revenue']
            .sum()
            .sort_values('revenue', ascending=False)
        ) #type:ignore

    def units_sold_per_product(self):
        return (
            self.df.groupby('product_key', as_index=False)['quantity']
            .sum()
            .sort_values('quantity', ascending=False)
        ) #type:ignore
    
    def profit_per_product(self):
        return (
            self.df.groupby('product_key', as_index=False)['profit']
            .sum()
            .sort_values('profit', ascending=False)
        ) #type:ignore
    
    def avg_product_price(self):
        return (
            self.df.groupby('product_key', as_index=False)['price']
            .mean()
            .sort_values('price', ascending=False)
        ) #type:ignore
    
# Product Popularity Metrics

    def order_per_product(self):
        return (
            self.df.groupby('product_key', as_index=False)['order_number']
            .nunique()
            .sort_values('order_number', ascending=False)
        ) #type:ignore

    def customer_per_product(self):
        return (
            self.df.groupby('product_key', as_index=False)['customer_key']
            .unique()
            .sort_values('customer_key', ascending=False)
        ) #type:ignore

# Category-Level Metrics

    def category_revenue(self) -> pd.DataFrame:
        return (
            self.df.groupby('category', as_index=False)['revenue']
            .sum()
            .sort_values('revenue', ascending=False) #type:ignore             
        ) 

    def category_profit(self) -> pd.DataFrame:
        return (
            self.df.groupby('category', as_index=False)['profit']
            .sum()
            .sort_values('profit', ascending=False)
        ) #type:ignore

    def category_units(self) -> pd.DataFrame:
        return (
            self.df.groupby('category', as_index=False)['quantity']
            .sum()
            .sort_values('quantity', ascending=False)
        ) #type:ignore

    

    def top_products_by_revenue(self, n: int = 10) -> pd.DataFrame:
        return (
            self.df.groupby("product_name", as_index=False)["amount"]
            .sum()
            .sort_values("amount", ascending=False) # type: ignore
            .head(n)
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


