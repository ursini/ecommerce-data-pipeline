with products as (
    select * from {{ ref('stg_products') }}
)
select distinct * from products