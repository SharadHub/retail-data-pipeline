import os
import polars as pl
LANDING_DIR = "data/landing"
STAGING_DIR = "data/staging"
os.makedirs(STAGING_DIR, exist_ok=True)

def run_transformation():
    # mapping path from data/landing to variables
    customers_path = os.path.join(LANDING_DIR, "customers.csv")
    order_items_path = os.path.join(LANDING_DIR, "order_items.csv")
    order_payments_path = os.path.join(LANDING_DIR, "order_payments.csv")
    order_reviews_path = os.path.join(LANDING_DIR, "order_reviews.csv")
    orders_path = os.path.join(LANDING_DIR, "orders.csv")
    products_path = os.path.join(LANDING_DIR, "products.csv")
    sellers_path = os.path.join(LANDING_DIR, "sellers.csv")

    # transforming plain csv files into polars dataframes
    customersDF = pl.read_csv(customers_path)
    orderItemsDF = pl.read_csv(order_items_path)
    orderPaymentsDF = pl.read_csv(order_payments_path)
    orderReviewsDF = pl.read_csv(order_reviews_path)
    ordersDF = pl.read_csv(orders_path)
    productsDF = pl.read_csv(products_path)
    sellersDF = pl.read_csv(sellers_path)

    # converting each date and time columns data type from string to datetime.

    orders_datetime_cols = [
        "order_purchase_timestamp",
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
        "order_estimated_delivery_date",
    ]

    orderReviews_dateTime_cols = [
        "review_creation_date",
        "review_answer_timestamp",
    ]

    ordersDF = ordersDF.with_columns(
        [pl.col(col).str.to_datetime() for col in orders_datetime_cols]
    )

    orderReviewsDF = orderReviewsDF.with_columns(
        [pl.col(col).str.to_datetime() for col in orderReviews_dateTime_cols]
    )

    # filling missing values in the dataframes

    orders_datetime_cols = [
        "order_approved_at",
        "order_delivered_carrier_date",
        "order_delivered_customer_date",
    ]

    orderReviews_null_cols = [
        "review_comment_title",
        "review_comment_message",
    ]

    # we do not need to fill null values in ordersDF as it is date and time columns and we cannot mess with date and time.

    productsDF = productsDF.with_columns(
        pl.col("product_category_name").fill_null(pl.lit("null")),
        pl.col([
            "product_name_lenght",
            "product_description_lenght",
            "product_photos_qty",
            "product_weight_g",
            "product_length_cm",
            "product_height_cm",
            "product_width_cm",
        ]).fill_null(pl.lit(0))
    )

    orderReviewsDF = orderReviewsDF.with_columns(
        pl.col(orderReviews_null_cols).fill_null(pl.lit("no comment"))
    )

    # removing data redundancy and keeping records consistent
    order_payments_summary = orderPaymentsDF.group_by("order_id").agg(
        pl.col("payment_value").sum().alias("total_payment")
    )

    # Left Join two tables
    fact_orders = ordersDF.join(order_payments_summary, on="order_id", how="left")

    # print(fact_orders.head())

    # finding location with biggest base of customer
    customers_location = customersDF.select([
        "customer_id",
        pl.concat_str(
            [pl.col("customer_city"), pl.col("customer_state")],
            separator=", "
        ).alias("customer_location")
    ])

    fact_orders = fact_orders.join(customers_location, on="customer_id", how="left")

    product_details = productsDF.select(["product_id", "product_category_name"])

    fact_order_items = orderItemsDF.join(product_details, on="product_id", how="left")
    # print(fact_order_items.head())

    fact_orders_dest = os.path.join(STAGING_DIR, "fact_orders.parquet")
    fact_order_items_dest = os.path.join(STAGING_DIR, "fact_order_items.parquet")

    fact_orders.write_parquet(fact_orders_dest)
    fact_order_items.write_parquet(fact_order_items_dest)

if __name__ == "__main__":
    run_transformation()
