import pandas as pd
import pytest

from src.loading.load_postgres import (
    load_customers,
    load_products,
    load_orders,
    load_order_items,
)


def test_load_customers_rejects_empty_dataframe():
    customers = pd.DataFrame()

    with pytest.raises(
        ValueError,
        match="Customers dataframe is empty",
    ):
        load_customers(customers)


def test_load_products_rejects_empty_dataframe():
    products = pd.DataFrame()

    with pytest.raises(
        ValueError,
        match="Products dataframe is empty",
    ):
        load_products(products)


def test_load_orders_rejects_empty_dataframe():
    orders = pd.DataFrame()

    with pytest.raises(
        ValueError,
        match="Orders dataframe is empty",
    ):
        load_orders(orders)


def test_load_order_items_rejects_empty_dataframe():
    order_items = pd.DataFrame()

    with pytest.raises(
        ValueError,
        match="Order items dataframe is empty",
    ):
        load_order_items(order_items)