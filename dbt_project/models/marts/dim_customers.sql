with customers as (
    select * from {{ ref('stg_customers') }}
)
select distinct * from customers