with source_data as (
    select * from {{ source('ecommerce_raw', 'stg_orders') }}
)
select * from source_data