with source_data as (
    select * from {{ source('ecommerce_raw', 'stg_customers') }}
)
select * from source_data