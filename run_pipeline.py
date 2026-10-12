import os
import time
import logging

# 1. Configure Production Logging
os.makedirs("logs", exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s [%(levelname)s] %(message)s",
    handlers=[
        logging.FileHandler("logs/pipeline.log"),
        logging.StreamHandler()
    ]
)

# 2. Import Module Functions
try:
    from src.transform import run_transformation
    from src.analytics import generate_analytics
except ImportError:
    # Fallback if scripts are in the root directory
    from transform import run_transformation
    from analytics import generate_analytics


def main():
    logging.info("STARTING RETAIL DATA PIPELINE EXECUTION")
    
    start_time = time.time()

    try:
        # Step 1: Run Transformation & Staging Layer (Phase 4)
        logging.info("--> Executing Phase 4: Data Transformation & Staging...")
        run_transformation()
        
        # Step 2: Run Analytics & Metrics Layer (Phase 5)
        logging.info("--> Executing Phase 5: Analytics & Metrics Reporting...")
        generate_analytics()

        elapsed_time = time.time() - start_time
        logging.info(f"🎉 PIPELINE COMPLETED SUCCESSFULLY IN {elapsed_time:.2f} SECONDS")

    except Exception as e:
        logging.error(f"PIPELINE FAILED WITH ERROR: {str(e)}", exc_info=True)


if __name__ == "__main__":
    main()