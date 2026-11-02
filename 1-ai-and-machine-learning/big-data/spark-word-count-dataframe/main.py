from pyspark.sql import SparkSession
from pyspark.sql.functions import col, explode, split, lower
from pathlib import Path

def create_spark(app_name="WordCount-DF"):
    return (
        SparkSession.builder
        .appName(app_name)
        .master("local[*]")
        .getOrCreate()
    )

def count_filewords(spark, input_path: str):
    df = spark.read.text("file:///" + Path(input_path).as_posix())
    words = (
        df.select(explode(split(lower(col("value")), r"\W+")).alias("word"))
        .where(col("word") != "")
    )
    counts = words.groupBy("word").count().orderBy(col("count").desc(), col("word").asc())
    return counts.collect()

def print_res(filename: str, results):
    print(f"\n{filename}")
    if not results:
        print("Порожній результат.")
        return
    for row in results:
        print(f"{row['word']} - {row['count']}")

def main():
    spark = create_spark()
    res_a = count_filewords(spark, r"C:\Users\user\PycharmProjects\BigData_1WC\data\A.txt")
    res_b = count_filewords(spark, r"C:\Users\user\PycharmProjects\BigData_1WC\data\B.txt")
    print_res("File A", res_a)
    print_res("File B", res_b)
    spark.stop()

if __name__ == "__main__":
    main()
