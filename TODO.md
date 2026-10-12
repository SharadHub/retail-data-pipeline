# TODO: Turn `retail-data-pipeline` into the "Hybrid Batch and Streaming E-commerce Data Platform"

**Done when** every word in the resume entry (*Python, SQL, Spark, Airflow, dbt, Kafka, Docker, AWS, GitHub Actions, eight phases*) points to working code in a public GitHub repo that runs with one `docker compose up` and passes CI.

The phases are in order, because each one builds on the one before it.

---

## 1. Foundations: fix and tidy what you already have
- [ ] Run `git init`, add a `.gitignore` (exclude `data/`, `*.zip`, `.venv`, `logs/`) and push to GitHub. This gives you the repo link the resume needs.
- [ ] Add `requirements.txt` or `pyproject.toml` and a `README.md` with an architecture diagram and the 8-phase table.
- [ ] Turn `extract.py` into a function and run seed → extract → transform → analytics from `run_pipeline.py`.
- [ ] Make a failed run exit with a non-zero code (`sys.exit(1)`).
- [ ] Replace relative paths with `pathlib` and a config or `.env` file.
- [ ] Fix the business-logic bugs:
  - [ ] Revenue currently counts canceled and unapproved orders.
  - [ ] Category revenue leaves out freight and isn't translated to English.
  - [ ] Missing categories become the literal `"null"`.
  - [ ] Missing dimensions are filled with 0 instead of the category median.
  - [ ] Zip codes lose their leading zeros.
  - [ ] The location report counts orders instead of `customer_unique_id`.
- [ ] Write the landing layer as Parquet instead of CSV.
- [ ] Add pytest unit tests on small sample data.

## 2. Batch ingestion: the S3 data lake (covers **SQL, Docker, AWS**)
- [ ] Replace SQLite with **Postgres** in Docker as the "production" database.
- [ ] Add **MinIO**, S3-compatible storage in Docker, as the bronze layer: Parquet partitioned by date, safe to re-run.
- [ ] Write the code with `boto3`/`s3fs` so pointing it at real **AWS S3** only means changing an env var.
- [ ] Run it against real S3 once (free tier) so the AWS claim is true.

## 3. Spark processing (covers **Spark**)
- [ ] Rewrite `transform.py` as **PySpark** jobs, bronze → silver: types, deduplication, and the null rules from `DATA_DICTIONARY.md`.
- [ ] Write silver back to MinIO/S3 as partitioned Parquet.

## 4. Warehouse + dbt (covers **dbt, SQL, data modeling**)
- [ ] Load silver into a **Postgres warehouse**.
- [ ] Create a dbt project:
  - [ ] `staging/` models
  - [ ] a star schema: `dim_customer`, `dim_product`, `dim_seller`, `dim_date`, `fct_orders`, `fct_order_items`
  - [ ] `marts/` that replace `analytics.py`: revenue, categories, locations, delivery performance
- [ ] Generate dbt docs with the lineage graph.

## 5. Data quality (backs up the "data quality checks" skill)
- [ ] Add dbt tests: `unique`, `not_null`, `relationships`, `accepted_values`.
- [ ] Add row-count checks between layers.
- [ ] Add a quarantine table for rejected rows.

## 6. Streaming (covers **Kafka**, the "hybrid" part)
- [ ] Run a single-node **Kafka** broker in KRaft mode in Docker.
- [ ] Write a Python producer that replays Olist orders as events (`order_created` → `paid` → `shipped` → `delivered`).
- [ ] Write a consumer with **Spark Structured Streaming** that sends events to bronze and Postgres.
- [ ] Build one near-real-time model or dashboard query, such as orders per minute or late shipments.

## 7. Orchestration (covers **Airflow**)
- [ ] Run **Airflow** in Docker with the LocalExecutor to keep it light on RAM.
- [ ] Build a DAG for the daily batch: ingest → spark → `dbt build` → `dbt test`, with retries, failure alerts and backfill.
- [ ] Add a DAG or sensor that monitors the streaming job.

## 8. CI/CD + containers (covers **Docker Compose, GitHub Actions**)
- [ ] One `docker-compose.yml` for the full stack, with profiles (`batch`, `streaming`, `airflow`) so it fits in 14 GB of RAM.
- [ ] GitHub Actions workflow: `ruff` lint, `pytest`, `dbt build` against a Postgres service container, and a Docker image build on every push and PR.
- [ ] Add a CI badge to the README.

---

## Final: make the resume match
- [ ] Replace `[GitHub repo link]` with the real URL.
- [ ] Add one measurable result, for example "processes 100k orders / 1.5M rows end-to-end in X min, with 40+ dbt tests".
- [ ] Switch "Building…" to "Built…" once all 8 phases are done.
- [ ] Be ready to explain in an interview:
  - [ ] why payments are aggregated before the join
  - [ ] the star schema grain
  - [ ] how the stream and batch data meet

---

**Rough effort:** 6–8 weeks part-time. Kafka, Spark streaming and Airflow are the heaviest parts. Try to have at least Phases 1–4 pushed to GitHub before you apply.
