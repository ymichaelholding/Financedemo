from pathlib import Path
from pyspark.sql import DataFrame
from utils.logger import LoggerFactory


class Writer:
    """Writes a Spark DataFrame as CSV into an output directory."""

    PROJECT_ROOT = Path(__file__).resolve().parents[1]
    DEFAULT_OUTPUT_PATH = PROJECT_ROOT / "output"

    def __init__(self, output_path: str | Path | None = None):
        self.output_path = Path(output_path) if output_path else self.DEFAULT_OUTPUT_PATH
        self.logger = LoggerFactory.get_logger(
            "fiancedemo.writer", "writer.log"
        )

    def CSVwriter(self, df: DataFrame) -> None:
        self.logger.info("Starting CSV write to: %s", self.output_path)

        try:
            self.output_path.parent.mkdir(parents=True, exist_ok=True)
            (
                df.write
                .mode("overwrite")
                .option("header", True)
                .csv(str(self.output_path))
            )
            self.logger.info("CSV write completed: %s", self.output_path)
        except Exception:
            self.logger.exception("CSV write failed: %s", self.output_path)
            raise
