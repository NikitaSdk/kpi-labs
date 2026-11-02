import pandas as pd

DEFAULT_TRANSACTIONS = [
    {"сливи", "салат", "помідори"},
    {"селера", "цукерки"},
    {"цукерки"},
    {"яблука", "морква", "помідори", "картопля", "цукерки"},
    {"яблука", "апельсини", "салат", "цукерки", "помідори"},
    {"персики", "апельсини", "селера", "помідори"},
    {"квасоля", "салат", "помідори"},
    {"апельсини", "салат", "морква", "помідори", "цукерки"},
    {"яблука", "банани", "сливи", "морква", "помідори", "цибуля", "цукерки"},
    {"яблука", "картопля"}
]


def support_itemset(X, transactions):
    return sum(1 for t in transactions if X.issubset(t))


def confidence(X, Y, transactions):
    sup_X = support_itemset(X, transactions)
    if sup_X == 0:
        return 0.0
    sup_XY = support_itemset(X.union(Y), transactions)
    return sup_XY / sup_X


def interest(X, Y, transactions):
    N = len(transactions)
    conf = confidence(X, Y, transactions)
    sup_Y = support_itemset(Y, transactions)
    return conf - sup_Y / N


def use_default_rules():
    return [
        ({"салат"}, {"помідори"}),
        ({"помідори"}, {"салат"}),
        ({"яблука"}, {"цукерки"}),
        ({"апельсини"}, {"помідори"}),
        ({"морква"}, {"цукерки"}),
        ({"селера"}, {"апельсини"}),
        ({"яблука", "морква"}, {"цукерки"}),
        ({"апельсини"}, {"помідори", "салат"}),
        ({"сливи", "яблука"}, {"морква", "помідори"})
    ]


def evaluate_rules(transactions, rules):
    results = []
    for X, Y in rules:
        rule_str = f"{','.join(X)} → {','.join(Y)}"
        sup = support_itemset(X.union(Y), transactions)
        conf = round(confidence(X, Y, transactions), 3)
        intr = round(interest(X, Y, transactions), 3)
        results.append((rule_str, sup, conf, intr))
    return results


def print_table(results):
    col_rule = max(len(r[0]) for r in results) + 3

    print("\nРезультати аналізу асоціативних правил\n")
    print(f"{'Правило'.ljust(col_rule)}Підтримка   Вірогідність   Цікавість")

    for rule, sup, conf, intr in results:
        print(f"{rule.ljust(col_rule)}"
              f"{str(sup).ljust(12)}"
              f"{str(conf).ljust(15)}"
              f"{intr}")



def main():
    transactions = DEFAULT_TRANSACTIONS
    rules = use_default_rules()

    print("Транзакції (вхідні дані)")
    for i, t in enumerate(transactions, 1):
        print(f"{i}. {', '.join(sorted(t))}")

    results = evaluate_rules(transactions, rules)

    print_table(results)


if __name__ == "__main__":
    main()
