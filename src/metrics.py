import pandas as pd


class KPIs:
    def __init__(self, df: pd.DataFrame):
        self.df = df


class SalesKPIs(KPIs):

    def total_orders(self) -> int:
        return self.df["order_number"].nunique()

    def total_revenue(self) -> float:
        return self.df["revenue"].sum()

    def total_profit(self) -> float:
        return self.df["profit"].sum()

    def total_unit_sold(self) -> int:
        return self.df["quantity"].sum()

    def avg_selling_price(self) -> float:
        return self.df["revenue"].sum() / self.df["quantity"].sum()

    def avg_unit_per_order(self) -> float:
        return self.df.groupby("order_number")["quantity"].sum().mean()

    def orders_by_year(self) -> pd.DataFrame:
        df = (
            self.df.groupby("year", as_index=False)["order_number"]
            .nunique()
            .rename(columns={"order_number": "total_order"})
        )  # type: ignore
        df["growth_rate"] = df["total_order"].pct_change() * 100
        return df

    def revenue_by_year(self) -> pd.DataFrame:
        df = self.df.groupby("year", as_index=False)["revenue"].sum()  # type: ignore
        df["growth_rate"] = df["revenue"].pct_change() * 100
        return df

    def avg_order_value(self) -> pd.DataFrame:
        df = pd.merge(
            self.revenue_by_year(), self.orders_by_year(), how="left", on="year"
        )
        df["aov"] = df["revenue"] / df["total_order"]
        return df[["year", "aov"]]

    def revenue_by_month(self) -> pd.DataFrame:
        return pd.pivot_table(
            data=self.df,
            index=["month", "month_name"],
            columns=["year"],
            values="amount",
            aggfunc="sum",
        ).reset_index()

    def profit_by_year(self) -> pd.DataFrame:
        df = self.df.groupby("year", as_index=False)["profit"].sum()
        df['growth_rate'] = df['profit'].pct_change() * 100
        return df

    def profit_by_month(self) -> pd.DataFrame:
        return (
            pd.pivot_table(
                data=self.df,
                index=["month", "month_name"],
                columns=["year"],
                values="profit",
                aggfunc="sum",
            )
            .reset_index()
            .drop("month", axis=1)
        )  # type: ignore

    def last_year_mom_growth_r(self) -> pd.DataFrame:
        df = self.df.groupby(["year", "month", "month_name"], as_index=False)[
            "amount"
        ].sum()
        df = df[df["year"] == df["year"].max() - 1][["month_name", "amount"]]
        df["mom"] = (
            (df["amount"] - df["amount"].shift(1)) / df["amount"].shift(1) * 100
        ).round(2)
        df = df[["month_name", "mom"]]
        return df

    def yoy_growth_r(self) -> pd.DataFrame:
        df = self.df.groupby("year", as_index=False)["amount"].sum()

        df["yoy"] = (
            (df["amount"] - df["amount"].shift(1)) / df["amount"].shift(1) * 100
        ).round(2)
        df = df[["year", "yoy"]]
        return df

    def yoy_growth_p(self):
        df = self.df.groupby("year", as_index=False)["profit"].sum()

        df["yoy"] = (
            (df["profit"] - df["profit"].shift(1)) / df["profit"].shift(1) * 100
        ).round(2)
        df = df[["year", "yoy"]]
        return df

    def revenue_and_profit_by_country(self) -> pd.DataFrame:
        df = self.df.groupby("country", as_index=False)[
            ["cost", "price", "amount"]
        ].sum()
        df["profit"] = df["price"] - df["cost"]
        return (
            df[["country", "profit", "amount"]]
            .sort_values("amount", ascending=False)
            .rename(columns={"amount": "revenue"})
        )

    def monthly_revenue(self) -> pd.Series:
        return self.df.groupby(self.df["order_date"].dt.to_period("M"))["revenue"].sum()


class CustomerKPIs(KPIs):

    def total_customer(self) -> int:
        return self.df["customer_key"].nunique()

    def avg_order_per_customer(self) -> float:
        return self.df.groupby("customer_key")["order_number"].count().mean()

    def ARPU(self) -> float:
        df = self.df.groupby(["year", "customer_key"], as_index=False)["revenue"].sum()
        return df.groupby("year", as_index=False)["revenue"].mean()

    def customer_repeat_rate(self) -> float:
        df = self.df.groupby(["year", "customer_key"], as_index=False)[
            "customer_key"
        ].count()
        repeat_customer = df[df["customer_key"] > 1]
        repeat_customer_by_year = repeat_customer.groupby("year", as_index=False)[
            "customer_key"
        ].count()
        total_customer_by_year = self.df.groupby("year", as_index=False)[
            "customer_key"
        ].nunique()
        repeat_customer_by_year["repeat_rate"] = (
            repeat_customer_by_year["customer_key"]
            / total_customer_by_year["customer_key"]
        ) * 100
        return repeat_customer_by_year

    def purchase_frequency(self) -> pd.DataFrame:
        df = self.df.groupby("year", as_index=False)[
            ["order_number", "customer_key"]
        ].nunique()
        df["purchase_frequency"] = round(df["order_number"] / df["customer_key"], 2)
        return df[["year", "purchase_frequency"]]

    def customer_growth_rate(self):
        df = self.df.groupby("year", as_index=False)["customer_key"].nunique()
        df["growth_rate"] = df["customer_key"].pct_change() * 100
        return df

    def CLV(self):
        customer_year_revenue = (
            self.df.groupby(["customer_key", "year"])["revenue"].sum().reset_index()
        )

        customer_year_revenue = customer_year_revenue.sort_values(
            ["customer_key", "year"]
        )
        customer_year_revenue["clv"] = customer_year_revenue.groupby("customer_key")[
            "revenue"
        ].cumsum()

        clv_year = customer_year_revenue.groupby("year")["clv"].mean().reset_index()
        return clv_year

    def customer_across_country(self) -> pd.DataFrame:
        return (
            self.df.groupby("country", as_index=False)["customer_key"]
            .nunique()
            .sort_values("customer_key", ascending=False)  # type:ignore
            .rename(columns={"customer_key": "total_customer"})
        )

    def revenue_and_profit_by_age_group(self) -> pd.DataFrame:
        return (
            self.df.groupby("age_group", as_index=False)[["revenue", "profit"]]
            .sum()
            .sort_values("revenue", ascending=False)  # type: ignore
        )

    def revenue_by_customer(self) -> pd.DataFrame:
        return (
            self.df.groupby("customer_key", as_index=False)["revenue"]
            .sum()
            .sort_values("revenue", ascending=False)
        )  # type: ignore


class ProductKPIs(KPIs):

    # Product-Level Metrics

    def revenue_per_product(self) -> pd.DataFrame:
        return (
            self.df.groupby(["product_key", "product_name"], as_index=False)["revenue"]
            .sum()
            .sort_values("revenue", ascending=False)
        )  # type:ignore

    def units_sold_per_product(self):
        return (
            self.df.groupby(["product_key", "product_name"], as_index=False)["quantity"]
            .sum()
            .sort_values("quantity", ascending=False)
        )  # type:ignore

    def profit_per_product(self):
        return (
            self.df.groupby(["product_key", "product_name"], as_index=False)["profit"]
            .sum()
            .sort_values("profit", ascending=False)
        )  # type:ignore

    def avg_product_price(self):
        return (
            self.df.groupby(["product_key", "product_name"], as_index=False)["price"]
            .mean()
            .sort_values("price", ascending=False)
        )  # type:ignore

    # Product Popularity Metrics

    def order_per_product(self):
        return (
            self.df.groupby(["product_key", "product_name"], as_index=False)[
                "order_number"
            ]
            .nunique()
            .sort_values("order_number", ascending=False)
        )  # type:ignore

    def customer_per_product(self):
        return (
            self.df.groupby(["product_key", "product_name"], as_index=False)[
                "customer_key"
            ]
            .nunique()
            .sort_values("customer_key", ascending=False)
        )  # type:ignore

    # Category-Level Metrics

    def category_revenue(self) -> pd.DataFrame:
        return (
            self.df.groupby("category", as_index=False)["revenue"]
            .sum()
            .sort_values("revenue", ascending=False)  # type:ignore
        )

    def category_profit(self) -> pd.DataFrame:
        return (
            self.df.groupby("category", as_index=False)["profit"]
            .sum()
            .sort_values("profit", ascending=False)
        )  # type:ignore

    def category_units(self) -> pd.DataFrame:
        return (
            self.df.groupby("category", as_index=False)["quantity"]
            .sum()
            .sort_values("quantity", ascending=False)
        )  # type:ignore
