from pyspark.sql import SparkSession
from pyspark.sql.functions import (
    col, explode, split, lower, input_file_name,
    concat_ws, collect_set, monotonically_increasing_id, row_number
)
from pyspark.sql.window import Window

def create_spark(app_name="InvertedIndex-Final-Fixed"):
    return (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .getOrCreate()
    )

def build_inverted_index(spark, files):
    df = (
        spark.read.text(files)
        .withColumnRenamed("value", "line")
        .withColumn("filename", input_file_name())
    )

    df = df.withColumn("line_id", monotonically_increasing_id())

    window = Window.partitionBy("filename").orderBy("line_id")
    df = df.withColumn("offset", row_number().over(window) - 1)

    words = (
        df.select(
            explode(split(lower(col("line")), r"\W+")).alias("word"),
            col("filename"), col("offset")
        )
        .where(col("word") != "")
    )

    words = words.withColumn("file_offset", concat_ws("@", col("filename"), col("offset")))

    inverted = (
        words.groupBy("word")
             .agg(collect_set("file_offset").alias("locations"))
             .orderBy("word")
    )

    return inverted.collect()

def print_res(results, label="ALL FILES"):
    print(f"\n=== {label} ===")
    if not results:
        print("Порожній результат.")
        return

    for row in results:
        word = row["word"]
        locations = row["locations"]

        short_locations = [loc.split("/")[-1] for loc in locations]
        print(f"{word:<8} {', '.join(sorted(short_locations))}")

def main():
    spark = create_spark()

    files = [
        "file:///C:/Users/user/PycharmProjects/BigData1_2INV/data/A.txt",
        "file:///C:/Users/user/PycharmProjects/BigData1_2INV/data/B.txt"
    ]

    results = build_inverted_index(spark, files)
    print_res(results, "ALL FILES")

    spark.stop()

if __name__ == "__main__":
    main()
