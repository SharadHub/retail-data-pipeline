# Master Data Dictionary: Olist E-Commerce Ecosystem

This document provides a single reference point for the structural schemas, relationship constraints, and business rules governing the source subsystems of the retail ETL pipeline.

---

## 1. Subsystem Index & Target Storage Architecture

| Table/Entity Name | Primary Key (PK) | Foreign Key (FK) | Storage Format | Business Purpose |
| :--- | :--- | :--- | :--- | :--- |
| `customers` | customer_unique_id | None | SQLite Database | Maps unique users to per-order identifiers (`customer_id`). |
| `order_items` | order_item_id | order_id, product_id, seller_id | CSV File | Granular details of items purchased within each order. |
| `order_payments` | Composite | order_id | SQLite Database | Ledger tracking transaction split configurations. |
| `order_reviews` | review_id | order_id | Parquet File | Customer reviews and ratings for specific orders. |
| `orders` | order_id | customer_id | CSV File | Master transaction lifecycle tracker. |
| `products` | product_id | None | Parquet File | Master catalog containing physical dimensions. |
| `sellers` | seller_id | None | Parquet File | Registered sellers information on the platform. |

---

## 2. Detailed Table Schemas & Business Rules

### Table: customers
* **Description:** Contains customer data, mapping unique users (`customer_unique_id`) to per-order identifiers (`customer_id`).
* **Storage Format:** SQLite Database
* **Data Type Handling Rules:** 
  * `customer_zip_code_prefix` must be converted to string.

### Table: orders
* **Description:** Tracks order statuses, purchase timelines, and logistics delivery checkpoints.
* **Storage Format:** CSV File

| Column Name | Source Type | Target Type | Nullable? | Business Description / Handling Rules |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | str | str | No | Unique transaction identifier. |
| `customer_id` | str | str | No | Foreign key linking back to a specific customer checkout session. |
| `order_status` | str | Categorical | No | Current status (`delivered`, `shipped`, `canceled`). |
| `order_purchase_timestamp` | str | Datetime | No | Date and time the customer clicked "Buy Now". |
| `order_approved_at` | str | Datetime | Yes | **Null Rule:** Keep for drop-off analysis, filter out for financial revenue calculations. |
| `order_delivered_carrier_date` | str | Datetime | Yes | **Null Rule:** Treat as unfulfilled or backordered. |
| `order_delivered_customer_date` | str | Datetime | Yes | **Null Rule:** Exclude when calculating delivery performance metrics. |

* **Data Type Notes:** All timestamps in `orders` are originally strings and must be converted to Datetime.

### Table: order_items
* **Description:** Details individual products purchased within an order.
* **Storage Format:** CSV File
* **Data Type Handling Rules:**
  * `order_item_id` must be converted from integer to string.
  * `shipping_limit_date` must be converted to datetime.

### Table: order_payments
* **Description:** Details how an order was financed, supporting multi-payment splits (e.g., splitting a cost between a voucher and a credit card).
* **Storage Format:** SQLite Database (`production.db`)

| Column Name | Source Type | Target Type | Nullable? | Business Description / Handling Rules |
| :--- | :--- | :--- | :--- | :--- |
| `order_id` | str | str | No | Foreign key linking payment details back to the parent order. |
| `payment_sequential` | i64 | Int64 | No | Index number tracking payment sequences. Requires review to confirm type. |
| `payment_type` | str | Categorical | No | Method utilized (`credit_card`, `boleto`, `voucher`, `debit_card`). |
| `payment_installments` | i64 | Int64 | No | Number of monthly installments chosen by the customer. |
| `payment_value` | f64 | Float64 | No | Total monetary value processed by this specific transaction method. |

### Table: order_reviews
* **Description:** Contains customer feedback, ratings, and comments for orders.
* **Storage Format:** Parquet File
* **Data Type Handling Rules:**
  * `review_creation_date` and `review_answer_timestamp` must be converted to datetime.
* **Business Rules for Handling Nulls:**
  * `review_comment_title`: If missing, fill with empty string or "No Title" to prevent text indexing errors.
  * `review_comment_message`: If missing (purely quantitative review), bypass for sentiment analysis but utilize for average review scores.

### Table: products
* **Description:** Master catalog containing product names, categories, and physical dimensions.
* **Storage Format:** Parquet File
* **Data Type Handling Rules:**
  * All measurement-related columns must be converted from integer to float or double.
* **Business Rules for Handling Nulls:**
  * `product_category_name`, `product_name_lenght`, `product_description_lenght`: If missing, fill with "Unknown" or zero respectively for catalog grouping.
  * `product_weight_g`, `product_length_cm`, `product_height_cm`, `product_width_cm`: If missing, impute with category median values before computing shipping costs.

### Table: sellers
* **Description:** Details about sellers registered on the platform.
* **Storage Format:** Parquet File
* **Data Type Handling Rules:** 
  * All column types are correct natively.