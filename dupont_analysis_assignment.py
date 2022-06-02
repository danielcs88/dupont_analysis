# ---
# jupyter:
#   jupytext:
#     text_representation:
#       extension: .py
#       format_name: percent
#       format_version: '1.3'
#       jupytext_version: 1.13.8
#   kernelspec:
#     display_name: Python 3 (ipykernel)
#     language: python
#     name: python3
# ---

# %% [markdown] id="goN5BLi7Ukkm"
#  # Assignment 1
#
#  Daniel Cárdenas<br>
#  FIN6326<br>
#  `6102358`

# %% [markdown] id="lXSA5n44Ukko"
# <a href="https://colab.research.google.com/github/danielcs88/dupont_analysis/blob/master/dupont_analysis_assignment.ipynb" target="_parent"><img src="https://colab.research.google.com/assets/colab-badge.svg" alt="Open In Colab"/></a>

# %% colab={"base_uri": "https://localhost:8080/"} id="U1bplq9yUkko" outputId="d6a82cb9-53bb-4aa2-f852-135c32ae6632"
# # !pip install binarytree
# # !pip install sqlalchemy

# %% id="SrGQonIRUkkp"
# import re
from typing import Union

import matplotlib.pyplot as plt
import pandas as pd
from IPython.display import display

# from sqlalchemy import create_engine

# %% id="E1IOkRA4Ukkp"
plt.rcParams["figure.dpi"] = 125
get_ipython().run_line_magic("config", "InlineBackend.figure_format = 'retina'")

# %%
dollar_value = lambda x: f"${x:,.2f}"
rate_value = lambda x: f"{x:.2%}"

# %% id="xCDOsbEVUkkq"
r_james = pd.read_csv(
    "https://raw.githubusercontent.com/danielcs88/dupont_analysis/master/Call_Cert33893_123121.SDF",
    sep=";",
)
b_united = pd.read_csv(
    "https://raw.githubusercontent.com/danielcs88/dupont_analysis/master/Call_Cert58979_123121.SDF",
    sep=";",
)


# %% id="gfSlXrEnUkkq"
def financial_query(df: str, measure: str, measure_float=True) -> Union[float, str]:
    """
    Returns values from queried measure and specified bank DataFrame

    Parameters
    ----------
    df : str
        Name of bank pd.DataFrame which will be eval'ed
    measure : str
        Measure to be sought
    measure_float : TYPE, optional
        Return float result?. The default is True.

    Returns
    -------
    Union[float, str]
        DESCRIPTION.

    """

    df = eval(df)

    if measure_float:
        return float(
            df.loc[df["Short Definition"].str.startswith(measure)]["Value"].unique()[0]
            # sql_query(f"SELECT * FROM {df} WHERE `Short Definition` LIKE '{measure}%'")[
            #     "Value"
            # ].unique()[0]
        )
    else:
        return df.loc[df["Short Definition"].str.startswith(measure)]["Value"].iloc[0]
        # return sql_query(
        #     f"SELECT * FROM {df} WHERE `Short Definition` LIKE '{measure}%'"
        # )["Value"].iloc[0]


# %% id="5R9czhfQUkkr"
def roe(bank: str) -> float:
    """
    Parameters
    ----------
    bank : str
        Name of bank pd.DataFrame.

    Returns
    -------
    float
        Return on Equity.
    """
    return financial_query(bank, "Net income") / financial_query(bank, "Total equity")


# %% id="C3C_YGAZUkkr"
def roa(bank: str) -> float:
    """
    Parameters
    ----------
    bank : str
        Name of bank pd.DataFrame.

    Returns
    -------
    float
        Return on Assets.

    """
    return financial_query(bank, "Net income") / financial_query(
        bank, "Total balance sheet assets"
    )


# %% id="1r9zLaXhUkkr"
def equity_multiplier(bank: str) -> float:
    """
    Parameters
    ----------
    bank : str
        Name of bank pd.DataFrame.

    Returns
    -------
    float
        Equity Multiplier.

    """
    return financial_query(bank, "Total balance sheet assets") / financial_query(
        bank, "Total equity"
    )


# %% id="KioyNNDTUkks"
def operating_income(bank: str) -> float:
    """
    Parameters
    ----------
    bank : str
        Name of bank pd.DataFrame.

    Returns
    -------
    float
        Operating Income.

    """
    interest_income = financial_query(bank, "Total interest income")
    interest_expense = financial_query(bank, "Total interest expense")
    loan_loss_provision = financial_query(bank, "Provision for loan and lease losses")
    non_interest_income = financial_query(bank, "Total noninterest income")
    return sum(
        [
            interest_income,
            -interest_expense,
            -loan_loss_provision,
            non_interest_income,
        ]
    )


# %% id="CrNvYsxHUkks"
def return_on_sales(bank: str) -> float:
    """
    Calculates Return On Sales

    Parameters
    ----------
    bank : str
        Name of bank pd.DataFrame.

    Returns
    -------
    float
        Return On Sales.

    """
    return financial_query(bank, "Net income") / operating_income(bank)


# %% id="ZYuWfO6aUkks"
def asset_turnover(bank: str) -> float:
    """
    Returns Asset Turnover Rate

    Parameters
    ----------
    bank : str
        Name of bank pd.DataFrame.

    Returns
    -------
    float
        Returns Asset Turnover Rate.

    """
    return operating_income(bank) / financial_query(bank, "Total balance sheet assets")


# %% id="9qGf6XSjUkks"
from binarytree import build


def dupont_analysis(bank: str) -> None:
    """
    Prints a DuPont Analysis of bank.

    Parameters
    ----------
    bank : str
        Name of bank pd.DataFrame to be eval'ed.

    """
    values = [
        f"Return on Equity: {rate_value(roe(bank))}",
        f"Equity Multiplier: {equity_multiplier(bank):.2f}",
        f"Return on Assets: {rate_value(roa(bank))}",
        "",
        "",
        f"Asset Turnover: {rate_value(asset_turnover(bank))}",
        f"Return on Sales: {rate_value(return_on_sales(bank))}",
    ]
    root = build(values)
    print(financial_query(bank, "Legal title of bank", measure_float=False))
    print(root)


# %% colab={"base_uri": "https://localhost:8080/"} id="ALPFgcUTUkks" outputId="87df2a0d-c9c3-4e1b-8220-a1617a160a51"
print(*map(dupont_analysis, ["r_james", "b_united"]))


# %% id="8Ho-LvJVUkkt"
def bank_series(bank: str) -> pd.Series:
    bank_dict = {
        "Name": financial_query(bank, "Legal title of bank", measure_float=False),
        "Return on Equity": roe(bank),
        "Equity Multiplier": equity_multiplier(bank),
        "Return on Assets": roa(bank),
        "Asset Turnover": asset_turnover(bank),
        "Return on Sales": return_on_sales(bank),
    }
    return pd.Series(bank_dict)


# %% id="1D-q8nmOUkkt"
banks_df = pd.concat(list(map(bank_series, ["r_james", "b_united"])), axis=1)
banks_df.columns = banks_df.loc["Name"]
banks_df.drop("Name", axis=0, inplace=True)

# %% colab={"base_uri": "https://localhost:8080/", "height": 143} id="1mk_aAuIUkkt" outputId="1d478885-71e4-4290-81b6-0f0b1f058517"
display(
    banks_df.T.style.format(
        {
            "Return on Equity": "{:.2%}",
            "Equity Multiplier": "{:.2f}",
            "Return on Assets": "{:.2%}",
            "Asset Turnover": "{:.2%}",
            "Return on Sales": "{:.2%}",
        }
    )
)

# %% colab={"base_uri": "https://localhost:8080/", "height": 1000} id="-5z-HF8GUkkt" outputId="3b0ecbb4-7470-4970-a4b1-59ac88876c08"
banks_df.T.plot(
    title="Dupont Analysis",
    subplots=True,
    kind="barh",
    figsize=(16, 9),
    sharex=False,
    grid=True,
)
plt.tight_layout()
plt.show()


# %%
def operating_income_analysis(bank: str) -> float:
    """
    Parameters
    ----------
    bank : str
        Name of bank pd.DataFrame.

    Returns
    -------
    float
        Operating Income.

    """
    interest_income = financial_query(bank, "Total interest income")
    interest_expense = financial_query(bank, "Total interest expense")
    loan_loss_provision = financial_query(bank, "Provision for loan and lease losses")
    non_interest_income = financial_query(bank, "Total noninterest income")
    return pd.Series({
        "Name": financial_query(bank, "Legal title of bank", measure_float=False),
        "Total interest income": float(interest_income),
        "Total interest expense": float(-interest_expense),
        "Provision for loan and lease losses": float(-loan_loss_provision),
        "Total noninterest income": float(non_interest_income),
    })


# %%
operating_df = pd.concat(list(map(operating_income_analysis, ["r_james", "b_united"])), axis=1)
operating_df.columns = operating_df.loc["Name"]
operating_df.drop("Name", axis=0, inplace=True)

# %%
import matplotlib.ticker as mtick



operating_df.T.plot(
    title="Operating Income Analysis",
    subplots=True,
    kind="barh",
    figsize=(16, 9),
    sharex=False,
    grid=True,
)

plt.gca().xaxis.set_major_formatter('${x:,.0f}')

# plt.gcf().xaxis.set_major_formatter('${x:1.2f}')
# plt.gcf().xaxis.set_major_formatter(mtick.StrMethodFormatter("${x:,.0f}"))
plt.tight_layout()
plt.show()

# %%
