# Code extracted from the lab report (report.pdf)

# ---- fragment 1 ----
from pyspark import SparkConf, SparkContext
import os
import re
import warnings

warnings.filterwarnings("ignore")

def create_spark(app_name="WordCount-RDD"):
    conf = SparkConf().setAppName(app_name).setMaster("local[*]")
    sc = SparkContext(conf=conf)
    sc.setLogLevel("ERROR")
    return sc

def count_words_in_order(sc, file_path):
    text_rdd = sc.textFile(file_path)
    token_re = re.compile(r"[A-Za-zА-Яа-яІіЇїЄєҐґ0-9]+")

    words_with_index = (
        text_rdd
        .flatMap(lambda line: token_re.findall(line.lower()))
        .zipWithIndex()
        .map(lambda wc: (wc[1], wc[0]))  # (index, word)
    )

    words_list = [w for _, w in sorted(words_with_index.collect(), key=lambda x: x[0])]

    counts = {}
    for w in words_list:
        if w not in counts:
            counts[w] = 1
        else:
            counts[w] += 1

    ordered_results = [(w, counts[w]) for w in counts.keys()]
    return ordered_results

def print_result(filepath, results):
    filename = os.path.basename(filepath)
    print(f"\n{filename}")
    for word, count in results:
        print(f"{word} - {count}")

def main():
    sc = create_spark()
    files = [
        r"C:\Users\user\PycharmProjects\BD_Lab_1WC\data\A.txt",
        r"C:\Users\user\PycharmProjects\BD_Lab_1WC\data\B.txt"
    ]
    for f in files:
        result = count_words_in_order(sc, f)
        print_result(f, result)

    sc.stop()

if __name__ == "__main__":
    main()

# ---- fragment 2 ----
from pyspark import SparkConf, SparkContext
import os, re, sys

def prepare_spark(app_name="InvertedIndexRDD", master="local[*]"):
    conf = (
        SparkConf()
        .setAppName(app_name)
        .setMaster(master)
        .set("spark.pyspark.python", sys.executable)
        .set("spark.pyspark.driver.python", sys.executable)
    )
    sc = SparkContext(conf=conf)
    sc.setLogLevel("ERROR")
    return sc

def tokenize_line(line):
    token_pattern = re.compile(r"[A-Za-zА-Яа-яІіЇїЄєҐґ0-9]+")
    return token_pattern.findall(line.lower())

def map_document(filename, text):
    pairs = []
    offset = 0

    for line in text.splitlines(keepends=True):
        line_clean = line.rstrip("\r\n").lower()

        for match in re.finditer(r"[A-Za-zА-Яа-яІіЇїЄєҐґ0-9]+", line_clean):
            word = match.group(0)
            start = offset + match.start()
            pairs.append((word, f"{filename}@offset{start}"))

        offset += len(line.encode("utf-8"))

    return pairs

def reduce_documents(file_list):
    unique_files = sorted(set(file_list))
    return ", ".join(unique_files)

def build_inverted_index(input_dir):
    sc = prepare_spark()
    all_files = [
        (fname, open(os.path.join(input_dir, fname), encoding="utf-8").read())
        for fname in os.listdir(input_dir)
        if fname.endswith(".txt")
    ]

    docs_rdd = sc.parallelize(all_files)
    mapped_rdd = docs_rdd.flatMap(lambda kv: map_document(kv[0], kv[1]))
    inverted_index = (
        mapped_rdd.groupByKey()
        .mapValues(reduce_documents)
        .sortByKey()
        .collect()
    )
    sc.stop()
    return inverted_index

def show_results(results):
    print("=== Inverted Index ===")
    for word, files in results:
        print(f"{word:<10} {files}")

if __name__ == "__main__":
    data_dir = r"C:\Users\user\PycharmProjects\BD_Lab_1IN\data"
    result = build_inverted_index(data_dir)
    show_results(result)
