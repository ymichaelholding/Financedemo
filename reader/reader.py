from pathlib import Path
from pyspark.sql import DataFrame, SparkSession
from utils.logger import LoggerFactory


class Reader:
    """Reads the source orders CSV into a Spark DataFrame."""

    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    DEFAULT_INPUT_PATH = PROJECT_ROOT / "data" / "customer_transactions.csv"

    def __init__(self, input_path: str | Path | None = None):
        self.input_path = Path(input_path) if input_path else self.DEFAULT_INPUT_PATH
        self.logger = LoggerFactory.get_logger(
            "fiancedemo.reader", "reader.log"
        )

    def CSVreader(self, spark: SparkSession) -> DataFrame:
        self.logger.info("Starting CSV read: %s", self.input_path)

        if not self.input_path.exists():
            message = f"Input CSV not found: {self.input_path}"
            self.logger.error(message)
            raise FileNotFoundError(message)

        try:
            df = (
                spark.read
                .option("header", True)
                .option("inferSchema", True)
                .option("mode", "FAILFAST")
                .csv(str(self.input_path))
            )
            self.logger.info("CSV read completed. Columns=%s", df.columns)
            return df
        except Exception:
            self.logger.exception("Failed to read CSV: %s", self.input_path)
            raise
