import yaml
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
        "Customer Lifespan",
        "Purchase_Frequency",
        "Customer Lifetime Value",
        "Customer Repeat Rate",
    ]
    values = [
        co.format_number(ckpi.total_customer()),
        co.format_number(ckpi.avg_order_per_customer()),
        co.format_number(ckpi.avg_revenue_per_customer()),
        co.format_number(ckpi.customer_lifespan()) + " Month's",
        co.format_number(ckpi.purchase_frequency()),
        co.format_number(ckpi.customer_lifetime_value()),
        co.format_number(ckpi.customer_repeat_rate()) + "%",
    ]

    df = pd.DataFrame({"KPIs": kpis, "Values": values})

    return df


class PlotBase:
    def __init__(
        self,
        x,
        y1,
        y2=np.nan,
        y3=np.nan,
        title="Title",
        xlabel="",
        ylabel="",
        label1=None,
        label2=None,
        label3=None,
        legend=False,
        fsize: tuple = (6, 4),
    ):
        self.x = x
        self.y1 = y1
        self.y2 = y2
        self.y3 = y3
        self.title = title
        self.xlabel = xlabel
        self.ylabel = ylabel
        self.label1 = label1
        self.label2 = label2
        self.label3 = label3
        self.legend = legend
        self.fsize = fsize

    def decoration(self):

        cfg = self.config()
        font = cfg["fontname"]
        title = cfg["title"]
        xaxis = cfg["axis"]["xaxis"]
        yaxis = cfg["axis"]["yaxis"]
        tick = cfg["axis"]["tick"]
        legend = cfg["legend"]

        plt.figure(figsize=self.fsize)
        ax = plt.gca()
        ax.set_axisbelow(True)

        self.plot(
            self.x,
            self.y1,
            self.y2,
            self.y3,
            self.label1,
            self.label2,
            self.label3,
        )

        plt.grid(True, axis="y", color="gray", alpha=0.5)

        plt.title(
            self.title,
            loc=title["loc"],
            pad=title["pad"],
            fontdict=dict(
                size=title["size"],
                color=title["color"],
                weight=title["weight"],
                style=title["style"],
                fontname=font,
            ),
        )

        plt.gca().spines["top"].set_visible(False)
        plt.gca().spines["right"].set_visible(False)
        plt.gca().spines["left"].set_color("gray")
        plt.gca().spines["bottom"].set_color("gray")

        plt.gca().yaxis.set_major_formatter(formatter)

        plt.xlabel(
            self.xlabel,
            fontdict=dict(
                size=xaxis["label"]["size"],
                color=xaxis["label"]["color"],
                weight=xaxis["label"]["weight"],
                style=xaxis["label"]["style"],
                fontname=font,
            ),
        )

        plt.ylabel(
            self.ylabel,
            fontdict=dict(
                size=yaxis["label"]["size"],
                color=yaxis["label"]["color"],
                weight=yaxis["label"]["weight"],
                style=yaxis["label"]["style"],
                fontname=font,
            ),
        )

        plt.xticks(
            size=xaxis["ticks"]["size"],
            color=xaxis["ticks"]["color"],
            weight=xaxis["ticks"]["weight"],
            style=xaxis["ticks"]["style"],
            fontname=font,
            rotation=xaxis["ticks"]["rotation"],
        )
        plt.yticks(
            size=yaxis["ticks"]["size"],
            color=yaxis["ticks"]["color"],
            weight=yaxis["ticks"]["weight"],
            style=yaxis["ticks"]["style"],
            fontname=font,
            rotation=yaxis["ticks"]["rotation"],
        )

        plt.tick_params(size=tick["size"], color=tick["color"])

        if self.legend:
            plt.legend(
                loc=legend["loc"],
                framealpha=legend["framealpha"],
                fontsize=legend["fontsize"],
                edgecolor=legend["edgecolor"],
                facecolor=legend["facecolor"],
                frameon=legend["frameon"],
            )

        plt.savefig(f"../outputs/figures/{self.title}.jpg", dpi=300, bbox_inches="tight")
        plt.show()

    def config(self):
        with open("C:\\Users\\TUF\\OneDrive\\Documents\\Code\\Vs Code\\sales_analytics\\src\\config\\config.yaml") as f:
            cfg = yaml.full_load(f)
        return cfg

    @abstractmethod
    def plot(self, x, y1, y2, y3, label1, label2, label3):
        pass


class LinePlot(PlotBase):
    def plot(self, x, y1, y2, y3, label1, label2, label3):
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


class ColumnPlot(PlotBase):
    def plot(self, x, y1, y2, y3, label1, label2, label3):
        sns.barplot(x=x, y=y1, color="#111111", width=0.3, label=label1)
        sns.barplot(x=x, y=y2, color="#777777", width=0.15, label=label2)
        sns.barplot(x=x, y=y3, color="#BBBBBB", width=0.1, label=label3)



class StackedColumnPlot(PlotBase):
    def plot(self, x, y1, y2, y3, label1, label2, label3):
        ax = plt.gca()
        ax.set_axisbelow(True)
        sns.barplot(x=x, y=y1, color="black", width=0.3, label=label1)
        sns.barplot(x=x, y=y2, bottom=y1, color="gray", width=0.3, label=label2)
        ax.grid(True, axis="y", color="gray", alpha=0.5)



class CombinePlot(PlotBase):
    def plot(self, x, y1, y2, y3, label1, label2, label3):
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

