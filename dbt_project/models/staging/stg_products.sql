with source_data as (
    select * from {{ source('ecommerce_raw', 'stg_products') }}
)
select * from source_data