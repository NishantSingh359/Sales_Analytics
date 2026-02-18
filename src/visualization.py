import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from abc import ABC, abstractmethod
from . import metrics as mt
from . import common as co
from matplotlib.ticker import FuncFormatter

formatter = FuncFormatter(co.chart_format_number)


def sales_kpis(df: pd.DataFrame) -> pd.DataFrame:
    skpi = mt.SalesKPIs(df)
    kpis = [
        "Total Orders",
        "Total Revenue",
        "Total Profit",
        "Total Unit Sold",
        "Profit Margin",
        "Average Order Value",
        "Average Selling Price",
        "Average Delivery Time",
    ]

    values = [
        co.format_number(skpi.total_orders()),
        co.format_number(skpi.total_revenue()),
        co.format_number(skpi.total_profit()),
        co.format_number(skpi.total_unit_sold()),
        (co.format_number(skpi.profit_margin()) + "%"),
        co.format_number(skpi.avg_order_value()),
        co.format_number(skpi.avg_selling_price()),
        skpi.avg_delivery_time(),
    ]

    df = pd.DataFrame({"KPIs": kpis, "Values": values})

    return df


def customer_kpis(df: pd.DataFrame) -> pd.DataFrame:
    ckpi = mt.CustomerKPIs(df)
    kpis = [
        "Total Customer",
        "Avg Order Per Customer",
        "Avg Revenue Per Customer",
        "Customer Lifetime Value",
        "Customer Repeat Rate",
        "Purchase_Frequency",
    ]
    values = [
        co.format_number(ckpi.total_customer()),
        co.format_number(ckpi.avg_order_per_customer()),
        co.format_number(ckpi.avg_revenue_per_customer()),
        co.format_number(ckpi.customer_lifetime_value()),
        co.format_number(ckpi.customer_repeat_rate()),
        co.format_number(ckpi.purchase_frequency()),
    ]
    return pd.DataFrame({"KPIs": kpis, "Values": values})



class PlotBase:
    def __init__(
        self,
        x,
        y1,
        y2=np.nan,
        y3=np.nan,
        title=None,
        xlable=None,
        ylable=None,
        label1=np.nan,
        label2=np.nan,
        label3=np.nan,
        legend=False,
        fsize: tuple = (6, 4),
    ):
        self.x = x
        self.y1 = y1
        self.y2 = y2
        self.y3 = y3
        self.title = title
        self.xlable = xlable
        self.ylable = ylable
        self.label1 = label1
        self.label2 = label2
        self.label3 = label3
        self.legend = legend
        self.fsize = fsize

    def decoration(self):
        plt.figure(figsize=self.fsize)
        self.plot(
            self.x,
            self.y1,
            self.y2,
            self.y3,
            self.label1,
            self.label2,
            self.label3,
            self.legend,
        )
        plt.title(self.title, fontdict=dict(size=18, color="gray"), loc="left", pad=30)
        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        plt.gca().spines["left"].set_color("gray")
        plt.gca().spines["bottom"].set_color("gray")
        plt.xlabel(self.xlable, fontdict=dict(size=15, color="gray"))
        plt.ylabel(self.ylable, fontdict=dict(size=12, color="gray"))
        plt.tick_params(color="gray")

        plt.xticks(size=12, rotation=90, color="gray")
        plt.yticks(size=12, color="gray")

    @abstractmethod
    def plot(self, x, y1, y2, y3, label1, label2, label3, legend):
        pass


class LinePlotLabel(PlotBase):
    def plot(self, x, y1, y2, y3, label1, label2, label3, legend):
        sns.lineplot(
            x=x,
            y=y1,
            color="#111111",
            marker="o",
            ms=9,
            markeredgecolor="#111111",
            markerfacecolor="white",
            markeredgewidth=2,
            linewidth=2,
        )
        plt.gca().axes.get_yaxis().set_visible(False) # type: ignore
        plt.gca().spines["left"].set_visible(False)
        for i in range(len(y1)):
            plt.text(
                i - y2,
                y1.iloc[i] + y3,
                co.format_number(y1.iloc[i]),
                fontdict=dict(color="#242424", size=11),
            )


class LinePlot(PlotBase):
    def plot(self, x, y1, y2, y3, label1, label2, label3, legend):
        ax = plt.gca()
        ax.set_axisbelow(True)
        sns.lineplot(
            x=x,
            y=y1,
            color="#111111",
            marker="o",
            ms=9,
            markeredgecolor="#111111",
            markerfacecolor="white",
            markeredgewidth=2,
            linewidth=2,
            label=label1,
        )
        sns.lineplot(
            x=x,
            y=y2,
            color="#777777",
            marker="o",
            ms=9,
            markeredgecolor="#777777",
            markerfacecolor="white",
            markeredgewidth=2,
            linewidth=2,
            label=label2,
        )
        sns.lineplot(
            x=x,
            y=y3,
            color="#BBBBBB",
            marker="o",
            ms=9,
            markeredgecolor="#BBBBBB",
            markerfacecolor="white",
            markeredgewidth=2,
            linewidth=2,
            label=label3,
        )
        ax.grid(True, axis="y", color="gray", alpha=0.5)
        plt.gca().yaxis.set_major_formatter(formatter)
        plt.legend().set_visible(legend)


class ColumnPlotLabel(PlotBase):
    def plot(self, x, y1, y2, y3, label1, label2, label3, legend):
        colors = ["black" if i > 0 else "gray" for i in y1]
        plt.bar(x, y1, color=colors, width=0.5)
        plt.gca().axes.get_yaxis().set_visible(False)
        plt.gca().spines["left"].set_visible(False)
        for i in range(len(y1)):
            plt.text(
                i - y2,
                y1.iloc[i] + y3,
                co.format_number(y1.iloc[i]),
                fontdict=dict(color="#242424", size=11),
            )


class ColumnPlot(PlotBase):
    def plot(self, x, y1, y2, y3, label1, label2, label3, legend):
        ax = plt.gca()
        ax.set_axisbelow(True)
        sns.barplot(x=x, y=y1, color="#111111", width=0.3, label=label1)
        sns.barplot(x=x, y=y2, color="#777777", width=0.3, label=label2)
        sns.barplot(x=x, y=y3, color="#BBBBBB", width=0.3, label=label3)
        ax.grid(True, axis="y", color="gray", alpha=0.5)
        plt.gca().yaxis.set_major_formatter(formatter)
        plt.legend().set_visible(legend)


class StackedColumnPlot(PlotBase):
    def plot(self, x, y1, y2, y3, label1, label2, label3, legend):
        ax = plt.gca()
        ax.set_axisbelow(True)
        sns.barplot(x=x, y=y1, color="black", width=0.3, label=label1)
        sns.barplot(x=x, y=y2, bottom=y1, color="gray", width=0.3, label=label2)
        ax.grid(True, axis="y", color="gray", alpha=0.5)
        plt.gca().yaxis.set_major_formatter(formatter)
        plt.legend().set_visible(legend)


class CombinePlot(PlotBase):
    def plot(self, x, y1, y2, y3, label1, label2, label3, legend):
        ax = plt.gca()
        ax.set_axisbelow(True)
        sns.barplot(x=x, y=y1, color="black", width=0.4, label=label1)
        sns.lineplot(
            x=x,
            y=y2,
            color="gray",
            marker="o",
            ms=9,
            markeredgecolor="#11111100",
            markerfacecolor="gray",
            linewidth=2,
            label=label2,
        )
        ax.grid(True, axis="y", color="gray", alpha=0.5)
        plt.gca().yaxis.set_major_formatter(formatter)
        plt.legend().set_visible(legend)
