import random
import string

import pytest

from langchain.docstore.document import Document
from langchain.document_loaders.pyspark_dataframe import PySparkDataFrameLoader


class TestPySparkDocumentLoader:
    # Checking basic pyspark reader functionality
    @pytest.mark.requires("pyspark")
    def test_pyspark_loader_load_valid_data(self) -> None:
        from pyspark.sql import SparkSession

        spark = SparkSession.builder.getOrCreate()
        data = [
            (random.choice(string.ascii_letters), random.randint(0, 1))
            for _ in range(3)
        ]
        df = spark.createDataFrame(data, ["text", "label"])

        expected_docs = [
            Document(
                page_content=data[0][0],
                metadata={"label": data[0][1]},
            ),
            Document(
                page_content=data[1][0],
                metadata={"label": data[1][1]},
            ),
            Document(
                page_content=data[2][0],
                metadata={"label": data[2][1]},
            ),
        ]

        loader = PySparkDataFrameLoader(
            spark_session=spark, df=df, page_content_column="text"
        )
        result = loader.load()

        assert result == expected_docs
