import pandas as pd
from sqlalchemy import create_engine

user = "root"
password = "1234"
host = "localhost"
database = "gold"

engine = create_engine(f"mysql+mysqlconnector://{user}:{password}@{host}/{database}")

def load_gold() -> None:
    """
    Load data from SQL Database
    """
    tables = [('dim_customer', 'customer'), ('dim_product', 'product'), ('fact_sales', 'sales')]

    for tbl, tbl_name in tables:
        df = pd.read_sql(f"SELECT * FROM {tbl}", con=engine)
        df.to_csv(f"data/{tbl_name}.csv")
   
if __name__ == '__main__':
    load_gold()