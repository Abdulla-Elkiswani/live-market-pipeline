---
title: Raisin Data Gateway Analytics
---

Welcome to the data ingestion monitoring portal. Below is the live analysis compiled directly from the gateway's processed database storage layer.

```sql salary_summary
select 
    job_title,
    round(avg(salary_in_usd), 2) as avg_salary_usd,
    count(*) as total_records
from production_data.market_data
group by job_title
order by avg_salary_usd desc
limit 10;