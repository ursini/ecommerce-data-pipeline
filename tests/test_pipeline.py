import pandas as pd

import src.main as pipeline


def test_main_executes_pipeline(monkeypatch):
    calls = []

    data = {
        "customers": pd.DataFrame({"customer_id": [1]}),
        "products": pd.DataFrame({"product_id": [1]}),
        "orders": pd.DataFrame({"order_id": [1]}),
        "order_items": pd.DataFrame({"order_item_id": [1]}),
    }

    def fake_extract_data():
        calls.append("extract")
        return data

    def fake_transform_customers(df):
        calls.append("transform_customers")
        return df

    def fake_transform_products(df):
        calls.append("transform_products")
        return df

    def fake_transform_orders(df):
        calls.append("transform_orders")
        return df

    def fake_transform_order_items(df):
        calls.append("transform_order_items")
        return df

    def fake_validate_customers(df):
        calls.append("validate_customers")

    def fake_validate_products(df):
        calls.append("validate_products")

    def fake_validate_orders(df):
        calls.append("validate_orders")

    def fake_validate_order_items(df):
        calls.append("validate_order_items")

    def fake_validate_relationships(
        customers,
        products,
        orders,
        order_items,
    ):
        calls.append("validate_relationships")

    def fake_load_customers(df):
        calls.append("load_customers")

    def fake_load_products(df):
        calls.append("load_products")

    def fake_load_orders(df):
        calls.append("load_orders")

    def fake_load_order_items(df):
        calls.append("load_order_items")

    def fake_load_final_tables():
        calls.append("load_final_tables")

    monkeypatch.setattr(
        pipeline,
        "extract_data",
        fake_extract_data,
    )

    monkeypatch.setattr(
        pipeline,
        "transform_customers",
        fake_transform_customers,
    )

    monkeypatch.setattr(
        pipeline,
        "transform_products",
        fake_transform_products,
    )

    monkeypatch.setattr(
        pipeline,
        "transform_orders",
        fake_transform_orders,
    )

    monkeypatch.setattr(
        pipeline,
        "transform_order_items",
        fake_transform_order_items,
    )

    monkeypatch.setattr(
        pipeline,
        "validate_customers",
        fake_validate_customers,
    )

    monkeypatch.setattr(
        pipeline,
        "validate_products",
        fake_validate_products,
    )

    monkeypatch.setattr(
        pipeline,
        "validate_orders",
        fake_validate_orders,
    )

    monkeypatch.setattr(
        pipeline,
        "validate_order_items",
        fake_validate_order_items,
    )

    monkeypatch.setattr(
        pipeline,
        "validate_relationships",
        fake_validate_relationships,
    )

    monkeypatch.setattr(
        pipeline,
        "load_customers",
        fake_load_customers,
    )

    monkeypatch.setattr(
        pipeline,
        "load_products",
        fake_load_products,
    )

    monkeypatch.setattr(
        pipeline,
        "load_orders",
        fake_load_orders,
    )

    monkeypatch.setattr(
        pipeline,
        "load_order_items",
        fake_load_order_items,
    )

    monkeypatch.setattr(
        pipeline,
        "load_final_tables",
        fake_load_final_tables,
    )

    pipeline.main()

    assert calls == [
        "extract",
        "transform_customers",
        "transform_products",
        "transform_orders",
        "transform_order_items",
        "validate_customers",
        "validate_products",
        "validate_orders",
        "validate_order_items",
        "validate_relationships",
        "load_customers",
        "load_products",
        "load_orders",
        "load_order_items",
        "load_final_tables",
    ]


def test_main_propagates_pipeline_error(monkeypatch):
    def fake_extract_data():
        raise RuntimeError("Extraction failed")

    monkeypatch.setattr(
        pipeline,
        "extract_data",
        fake_extract_data,
    )

    try:
        pipeline.main()
        assert False, "Expected RuntimeError"
    except RuntimeError as error:
        assert str(error) == "Extraction failed"