
from pathlib import Path
from pyspark.sql import SparkSession

from reader.reader import Reader
from transformation.transformation import TrimTransformation
from writer.writer import Writer
from utils.logger import LoggerFactory


class ETLApplication:
    """Coordinates the reader, transformation and writer classes."""

    def __init__(self):
        self.logger = LoggerFactory.get_logger(
            "fiancedemo.app", "app.log"
        )
        self.reader = Reader()
        self.transformation = TrimTransformation()
        self.writer = Writer()

    def run(self) -> None:
        spark = (
            SparkSession.builder
            .appName("Fiancedemo-Orders-Trim")
            .getOrCreate()
        )

        spark.sparkContext.setLogLevel("WARN")

        try:
            self.logger.info("ETL pipeline started.")

            # Step 1: Read CSV
            source_df = self.reader.CSVreader(spark)
            self.logger.info(
                "Input schema: %s",
                source_df.schema.simpleString()
            )

            # Step 2: Trim all string columns
            transformed_df = self.transformation.transform(source_df)

            # Step 3: Write transformed CSV
            self.writer.CSVwriter(transformed_df)

            self.logger.info("ETL pipeline completed successfully.")

        except Exception:
            self.logger.exception("ETL pipeline failed.")
            raise

        finally:
            spark.stop()


def main():
    ETLApplication().run()


if __name__ == "__main__":
    main()
