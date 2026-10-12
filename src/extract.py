import os
import polars as pl

# DATA EXTRACTION

# directory to the respective folders
RAW_DIR = "data/raw"
SRC_SYS_DIR = "data/source_systems"
LANDING_DIR = "data/landing"

# create a folder if not exist
os.makedirs(LANDING_DIR, exist_ok=True)

# connection string
DB_URI = f"sqlite:///{os.path.join(SRC_SYS_DIR, 'production.db')}"

# reading from production database
customerDF = pl.read_database_uri(
    query="SELECT * FROM customers",
    uri=DB_URI,
    engine="adbc"
)

orderPaymentsDF = pl.read_database_uri(
    query="SELECT * FROM order_payments",
    uri=DB_URI,
    engine="adbc"
)
print("Successfully extracted relational tables from production database!")

# EVENT LOG INGESTION

# mapping file path to variable
orders_path = os.path.join(SRC_SYS_DIR, "orders.csv")
order_items_path = os.path.join(SRC_SYS_DIR, "order_items.csv")

# reading files
ordersDF = pl.read_csv(orders_path)
orderItemsDF = pl.read_csv(order_items_path)
print("Successfully ingested transaction logs into active pipeline storage!")

# ANALYTICAL LAKE PULL

# mapping out source path to variable
order_reviews_path = os.path.join(SRC_SYS_DIR, "order_reviews.parquet")
products_path = os.path.join(SRC_SYS_DIR, "products.parquet")
sellers_path = os.path.join(SRC_SYS_DIR, "sellers.parquet")

# reading data as DataFrame
orderReviewsDF = pl.read_parquet(order_reviews_path)
productsDF = pl.read_parquet(products_path)
sellersDF = pl.read_parquet(sellers_path)
print("Successfully pulled analytical Parquet data into central ingestion layer!")

# STANDARDIZED LANDING

#  mapping path inside landing
customer_dest = os.path.join(LANDING_DIR, "customers.csv")
order_payments_dest = os.path.join(LANDING_DIR, "order_payments.csv")
order_items_dest = os.path.join(LANDING_DIR, "order_items.csv")
orders_dest = os.path.join(LANDING_DIR, "orders.csv")
order_reviews_dest = os.path.join(LANDING_DIR, "order_reviews.csv")
products_dest = os.path.join(LANDING_DIR, "products.csv")
sellers_dest = os.path.join(LANDING_DIR, "sellers.csv")

# saving all files as plain csv text format
customerDF.write_csv(customer_dest)
orderPaymentsDF.write_csv(order_payments_dest)
orderItemsDF.write_csv(order_items_dest)
ordersDF.write_csv(orders_dest)
orderReviewsDF.write_csv(order_reviews_dest)
productsDF.write_csv(products_dest)
sellersDF.write_csv(sellers_dest)