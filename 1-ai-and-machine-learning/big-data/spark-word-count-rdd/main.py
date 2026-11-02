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
