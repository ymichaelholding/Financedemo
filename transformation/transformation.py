from pyspark.sql import DataFrame, functions as F
from pyspark.sql.types import StringType
from utils.logger import LoggerFactory


class TrimTransformation:
    """Trims leading and trailing whitespace from all string columns."""

    def __init__(self):
        self.logger = LoggerFactory.get_logger(
            "fiancedemo.transformation", "transformation.log"
        )

    def transform(self, df: DataFrame) -> DataFrame:
        try:
            string_columns = [
                field.name for field in df.schema.fields
                if isinstance(field.dataType, StringType)
            ]
            self.logger.info(
                "Starting trim transformation. String columns=%s",
                string_columns
            )

            result = df
            for name in string_columns:
                # Escaping supports column names that contain spaces, dots or backticks.
                escaped_name = name.replace("`", "``")
                result = result.withColumn(
                    name,
                    F.trim(F.col(f"`{escaped_name}`"))
                )

            self.logger.info("Trim transformation completed.")
            return result
        except Exception:
            self.logger.exception("Trim transformation failed.")
            raise
