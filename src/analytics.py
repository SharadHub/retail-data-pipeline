import os
import polars as pl

STAGING_DIR = "data/staging"
REPORTS_DIR = "data/reports"
os.makedirs(REPORTS_DIR, exist_ok=True)

def generate_analytics():
    fact_orders_path = os.path.join(STAGING_DIR, "fact_orders.parquet")
    fact_order_items_path = os.path.join(STAGING_DIR, "fact_order_items.parquet")

    fact_orders = pl.read_parquet(fact_orders_path)
    fact_order_items = pl.read_parquet(fact_order_items_path)

    total_revenue = fact_orders.select(pl.col("total_payment").sum())
    total_revenue = total_revenue.item()
    print(f"Total Revenue: ${total_revenue:,.2f}")

    fact_order_items_revenue = (
        fact_order_items
        .group_by("product_category_name")
        .agg(pl.col("price").sum().alias("total_category_revenue"))
        .sort("total_category_revenue", descending=True)
    )
    print(fact_order_items_revenue.head())

    biggest_customer_base = (
        fact_orders
        .group_by("customer_location")
        .agg(pl.len().alias("order_count"))
        .sort("order_count", descending=True)
    )
    print(biggest_customer_base.head())

    fact_order_items_revenue.write_csv(os.path.join(REPORTS_DIR, "category_revenue_report.csv"))
    biggest_customer_base.write_csv(os.path.join(REPORTS_DIR, "location_orders_report.csv"))

if __name__ == "__main__":
    generate_analytics()