import os
import polars as pl

RAW_DIR = "./data/raw"
SRC_SYS_DIR = "./data/source_systems"

# create a folder if not exist
os.makedirs(SRC_SYS_DIR, exist_ok=True)
print("-----------------Path is ready!!!-----------------")

# SQLite Logic (code that transform customers and order_payments datasets into database)
DB_URI = "sqlite:///data/source_systems/production.db"

customer_path = os.path.join(RAW_DIR, "customers.csv")
customerDF = pl.read_csv(customer_path)

customerDF.write_database(
    table_name="customers",
    connection=DB_URI,
    if_table_exists="replace",
    engine="adbc",
)
order_payments_path = os.path.join(RAW_DIR, "order_payments.csv")
orderPaymentsDF = pl.read_csv(order_payments_path)

orderPaymentsDF.write_database(
    table_name="order_payments",
    connection=DB_URI,
    if_table_exists="replace",
    engine="adbc",
)
print("Successfully transform csv files to production Database")

# keeping orders and order_items as csv files

# routing paths to variable
orders_path = os.path.join(RAW_DIR, "orders.csv")
order_items_path = os.path.join(RAW_DIR, "order_items.csv")

# reading datasets in dataframe
ordersDF = pl.read_csv(orders_path)
orderItemsDF = pl.read_csv(order_items_path)

# routing them to destined folder
orders_dest = os.path.join(SRC_SYS_DIR, "orders.csv")
order_items_dest = os.path.join(SRC_SYS_DIR, "order_items.csv")

# writing into destined folder
ordersDF.write_csv(orders_dest)
orderItemsDF.write_csv(order_items_dest)

print("Successfully routed CSV event logs to active source storage!")

# Simulating csv files(products, sellers, order_reviews) into parquet files

# mapping out paths
products_path = os.path.join(RAW_DIR, "products.csv")
sellers_path = os.path.join(RAW_DIR, "sellers.csv")
order_reviews_path = os.path.join(RAW_DIR, "order_reviews.csv")

# Reading datasets into unique Polars DataFrames
productsDF = pl.read_csv(products_path)
sellersDF = pl.read_csv(sellers_path)
orderReviewsDF = pl.read_csv(order_reviews_path)

# Create\ing destination file paths
products_dest = os.path.join(SRC_SYS_DIR, "products.parquet")
sellers_dest = os.path.join(SRC_SYS_DIR, "sellers.parquet")
order_reviews_dest = os.path.join(SRC_SYS_DIR, "order_reviews.parquet")

# write on each DataFrame to save them to their destinations
productsDF.write_parquet(products_dest)
sellersDF.write_parquet(sellers_dest)
orderReviewsDF.write_parquet(order_reviews_dest)

print("Successfully compiled compressed columnar Parquet datasets!")

# verifying process

generated_files = os.listdir(SRC_SYS_DIR)
for index, item in enumerate(generated_files, start=1):
    print(f"{index}. {item}")