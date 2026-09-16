with source_data as (
    select * from {{ source('ecommerce_raw', 'stg_order_items') }}
)
select * from source_data