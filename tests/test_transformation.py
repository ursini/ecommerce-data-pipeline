import pandas as pd
import pytest

from src.transformation.validate_data import (
    validate_customers,
    validate_products,
    validate_orders,
    validate_order_items,
    validate_relationships,
)

from src.transformation.transform_data import (
    transform_products,
    transform_orders,
    transform_order_items,
)


def test_validate_customers_accepts_valid_data():
    customers = pd.DataFrame({
        "customer_id": [1, 2],
        "customer_name": ["Ana Silva", "Carlos Oliveira"],
        "email": ["ana@email.com", "carlos@email.com"],
    })

    validate_customers(customers)


def test_validate_customers_rejects_missing_customer_id():
    customers = pd.DataFrame({
        "customer_id": [1, None],
        "customer_name": ["Ana Silva", "Carlos Oliveira"],
        "email": ["ana@email.com", "carlos@email.com"],
    })

    with pytest.raises(
        ValueError,
        match="customer_id contains null values",
    ):
        validate_customers(customers)


def test_validate_customers_rejects_duplicate_emails():
    customers = pd.DataFrame({
        "customer_id": [1, 2],
        "customer_name": ["Ana Silva", "Carlos Oliveira"],
        "email": ["ana@email.com", "ana@email.com"],
    })

    with pytest.raises(
        ValueError,
        match="Duplicate customer emails found",
    ):
        validate_customers(customers)


def test_validate_products_accepts_valid_data():
    products = pd.DataFrame({
        "product_id": [1, 2],
        "product_name": ["Notebook", "Mouse"],
        "price": [4500.00, 120.50],
        "stock_quantity": [10, 20],
    })

    validate_products(products)


def test_validate_products_rejects_negative_price():
    products = pd.DataFrame({
        "product_id": [1],
        "product_name": ["Notebook"],
        "price": [-100.00],
        "stock_quantity": [10],
    })

    with pytest.raises(
        ValueError,
        match="Negative product prices found",
    ):
        validate_products(products)


def test_validate_products_rejects_negative_stock():
    products = pd.DataFrame({
        "product_id": [1],
        "product_name": ["Notebook"],
        "price": [4500.00],
        "stock_quantity": [-1],
    })

    with pytest.raises(
        ValueError,
        match="Negative stock quantities found",
    ):
        validate_products(products)


def test_validate_orders_accepts_valid_data():
    orders = pd.DataFrame({
        "order_id": [1, 2],
        "customer_id": [1, 2],
        "order_date": [
            "2026-02-01 10:15:00",
            "2026-02-02 14:30:00",
        ],
        "status": ["completed", "processing"],
    })

    validate_orders(orders)


def test_validate_orders_rejects_missing_customer_id():
    orders = pd.DataFrame({
        "order_id": [1],
        "customer_id": [None],
        "order_date": ["2026-02-01 10:15:00"],
        "status": ["completed"],
    })

    with pytest.raises(
        ValueError,
        match="customer_id contains null values",
    ):
        validate_orders(orders)


def test_validate_orders_rejects_invalid_status():
    orders = pd.DataFrame({
        "order_id": [1],
        "customer_id": [1],
        "order_date": ["2026-02-01 10:15:00"],
        "status": ["invalid_status"],
    })

    with pytest.raises(
        ValueError,
        match="Invalid order statuses found",
    ):
        validate_orders(orders)


def test_validate_order_items_accepts_valid_data():
    order_items = pd.DataFrame({
        "order_item_id": [1, 2],
        "order_id": [1, 1],
        "product_id": [1, 2],
        "quantity": [1, 2],
        "unit_price": [4500.00, 120.50],
    })

    validate_order_items(order_items)


def test_validate_order_items_rejects_invalid_quantity():
    order_items = pd.DataFrame({
        "order_item_id": [1],
        "order_id": [1],
        "product_id": [1],
        "quantity": [0],
        "unit_price": [4500.00],
    })

    with pytest.raises(
        ValueError,
        match="Order item quantities must be greater than zero",
    ):
        validate_order_items(order_items)


def test_validate_order_items_rejects_negative_unit_price():
    order_items = pd.DataFrame({
        "order_item_id": [1],
        "order_id": [1],
        "product_id": [1],
        "quantity": [1],
        "unit_price": [-100.00],
    })

    with pytest.raises(
        ValueError,
        match="Negative unit prices found",
    ):
        validate_order_items(order_items)


def test_validate_relationships_accepts_valid_data():
    customers = pd.DataFrame({
        "customer_id": [1, 2],
    })

    products = pd.DataFrame({
        "product_id": [1, 2],
    })

    orders = pd.DataFrame({
        "order_id": [1, 2],
        "customer_id": [1, 2],
    })

    order_items = pd.DataFrame({
        "order_id": [1, 2],
        "product_id": [1, 2],
    })

    validate_relationships(
        customers,
        products,
        orders,
        order_items,
    )


def test_validate_relationships_rejects_unknown_customer():
    customers = pd.DataFrame({
        "customer_id": [1],
    })

    products = pd.DataFrame({
        "product_id": [1],
    })

    orders = pd.DataFrame({
        "order_id": [1],
        "customer_id": [999],
    })

    order_items = pd.DataFrame({
        "order_id": [1],
        "product_id": [1],
    })

    with pytest.raises(
        ValueError,
        match="Orders reference unknown customers",
    ):
        validate_relationships(
            customers,
            products,
            orders,
            order_items,
        )


def test_validate_relationships_rejects_unknown_order():
    customers = pd.DataFrame({
        "customer_id": [1],
    })

    products = pd.DataFrame({
        "product_id": [1],
    })

    orders = pd.DataFrame({
        "order_id": [1],
        "customer_id": [1],
    })

    order_items = pd.DataFrame({
        "order_id": [999],
        "product_id": [1],
    })

    with pytest.raises(
        ValueError,
        match="Order items reference unknown orders",
    ):
        validate_relationships(
            customers,
            products,
            orders,
            order_items,
        )


def test_validate_relationships_rejects_unknown_product():
    customers = pd.DataFrame({
        "customer_id": [1],
    })

    products = pd.DataFrame({
        "product_id": [1],
    })

    orders = pd.DataFrame({
        "order_id": [1],
        "customer_id": [1],
    })

    order_items = pd.DataFrame({
        "order_id": [1],
        "product_id": [999],
    })

    with pytest.raises(
        ValueError,
        match="Order items reference unknown products",
    ):
        validate_relationships(
            customers,
            products,
            orders,
            order_items,
        )


def test_transform_products_cleans_text():
    products = pd.DataFrame({
        "product_id": [1],
        "product_name": [" Notebook "],
        "category": [" Eletronicos "],
        "price": ["4500.00"],
        "stock_quantity": ["25"],
        "created_at": ["2026-01-03 09:00:00"],
    })

    result = transform_products(products)

    assert result.loc[0, "product_name"] == "Notebook"
    assert result.loc[0, "category"] == "Eletronicos"


def test_transform_products_converts_types():
    products = pd.DataFrame({
        "product_id": [1],
        "product_name": ["Notebook"],
        "category": ["Eletronicos"],
        "price": ["4500.00"],
        "stock_quantity": ["25"],
        "created_at": ["2026-01-03 09:00:00"],
    })

    result = transform_products(products)

    assert pd.api.types.is_numeric_dtype(result["price"])
    assert pd.api.types.is_numeric_dtype(result["stock_quantity"])
    assert pd.api.types.is_datetime64_any_dtype(result["created_at"])


def test_transform_orders_converts_order_date():
    orders = pd.DataFrame({
        "order_id": [1],
        "customer_id": [1],
        "order_date": ["2026-02-01 10:15:00"],
        "status": ["COMPLETED"],
    })

    result = transform_orders(orders)

    assert pd.api.types.is_datetime64_any_dtype(
        result["order_date"]
    )


def test_transform_orders_normalizes_status():
    orders = pd.DataFrame({
        "order_id": [1],
        "customer_id": [1],
        "order_date": ["2026-02-01 10:15:00"],
        "status": [" COMPLETED "],
    })

    result = transform_orders(orders)

    assert result.loc[0, "status"] == "completed"


def test_transform_order_items_converts_numeric_types():
    order_items = pd.DataFrame({
        "order_item_id": [1],
        "order_id": [1],
        "product_id": [1],
        "quantity": ["2"],
        "unit_price": ["120.50"],
    })

    result = transform_order_items(order_items)

    assert pd.api.types.is_numeric_dtype(result["quantity"])
    assert pd.api.types.is_numeric_dtype(result["unit_price"])


def test_transform_order_items_removes_invalid_rows():
    order_items = pd.DataFrame({
        "order_item_id": [1, 2],
        "order_id": [1, 2],
        "product_id": [1, 2],
        "quantity": ["2", None],
        "unit_price": ["120.50", "350.00"],
    })

    result = transform_order_items(order_items)

    assert len(result) == 1


def test_transform_order_items_calculates_item_total():
    order_items = pd.DataFrame({
        "order_item_id": [1],
        "order_id": [1],
        "product_id": [1],
        "quantity": [2],
        "unit_price": [120.50],
    })

    result = transform_order_items(order_items)

    assert result.loc[0, "item_total"] == 241.00


def test_transform_order_items_calculates_multiple_item_totals():
    order_items = pd.DataFrame({
        "order_item_id": [1, 2],
        "order_id": [1, 2],
        "product_id": [1, 2],
        "quantity": [2, 3],
        "unit_price": [120.50, 350.00],
    })

    result = transform_order_items(order_items)

    assert result["item_total"].tolist() == [241.00, 1050.00]