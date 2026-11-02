import io
import requests
import pandas as pd
from datetime import date

# =========================
# Налаштування
# =========================
START_DATE = "1996-06-01"
END_DATE = date.today().isoformat()
OUTPUT_FILE = "currency_database_usd_uah_usd_eur.csv"

# =========================
# 1. Завантаження USD-UAH з НБУ
# =========================
def load_nbu_usd_uah(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Завантажує курс USD -> UAH з НБУ за період.
    НБУ підтримує параметри start, end, valcode, json.
    """
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"

    params = {
        "valcode": "USD",
        "start": pd.to_datetime(start_date).strftime("%Y%m%d"),
        "end": pd.to_datetime(end_date).strftime("%Y%m%d"),
        "json": ""
    }

    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()

    data = response.json()
    if not data:
        raise ValueError("НБУ не повернув дані для USD.")

    df = pd.DataFrame(data)

    # Очікувані поля: rate, cc, exchangedate
    df["date"] = pd.to_datetime(df["exchangedate"], format="%d.%m.%Y")
    df = df.rename(columns={"rate": "USD_UAH"})

    df = df[["date", "USD_UAH"]].copy()
    df = df.sort_values("date").reset_index(drop=True)

    return df


# =========================
# 2. Завантаження USD-EUR з ECB
# =========================
def load_ecb_usd_eur(start_date: str, end_date: str) -> pd.DataFrame:
    """
    Завантажує курс USD/EUR з ECB через офіційний Data API у CSV-форматі.
    Серія: EXR.D.USD.EUR.SP00.A
    """
    url = "https://data-api.ecb.europa.eu/service/data/EXR/D.USD.EUR.SP00.A"

    params = {
        "startPeriod": max(start_date, "1999-01-04"),  # офіційний ряд для EUR стартує з епохи євро
        "endPeriod": end_date,
        "format": "csvdata"
    }

    response = requests.get(url, params=params, timeout=60)
    response.raise_for_status()

    # ECB повертає CSV
    csv_text = response.text
    df = pd.read_csv(io.StringIO(csv_text))

    # Зазвичай дата в TIME_PERIOD, значення в OBS_VALUE
    if "TIME_PERIOD" not in df.columns or "OBS_VALUE" not in df.columns:
        raise ValueError(f"Неочікуваний формат відповіді ECB. Колонки: {list(df.columns)}")

    df["date"] = pd.to_datetime(df["TIME_PERIOD"])
    df["USD_EUR"] = pd.to_numeric(df["OBS_VALUE"], errors="coerce")

    df = df[["date", "USD_EUR"]].copy()
    df = df.sort_values("date").reset_index(drop=True)

    return df


# =========================
# 3. Формування єдиної бази
# =========================
def build_currency_database(start_date: str, end_date: str) -> pd.DataFrame:
    # Повний календар дат
    all_dates = pd.DataFrame({
        "date": pd.date_range(start=start_date, end=end_date, freq="D")
    })

    # Дані з джерел
    nbu_df = load_nbu_usd_uah(start_date, end_date)
    ecb_df = load_ecb_usd_eur(start_date, end_date)

    # Об'єднання
    result = all_dates.merge(nbu_df, on="date", how="left")
    result = result.merge(ecb_df, on="date", how="left")

    # Додаткові службові поля
    result["year"] = result["date"].dt.year
    result["month"] = result["date"].dt.month
    result["day"] = result["date"].dt.day

    # Для зручності можна додати текстову пару
    result["pair_1"] = "USD-UAH"
    result["pair_2"] = "USD-EUR"

    # Порядок колонок
    result = result[
        ["date", "year", "month", "day", "USD_UAH", "USD_EUR", "pair_1", "pair_2"]
    ]

    return result


# =========================
# 4. Запуск
# =========================
if __name__ == "__main__":
    df = build_currency_database(START_DATE, END_DATE)

    df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

    print("Файл успішно створено:", OUTPUT_FILE)
    print("Кількість рядків:", len(df))
    print("\nПерші 10 рядків:")
    print(df.head(10).to_string(index=False))

    print("\nОстанні 10 рядків:")
    print(df.tail(10).to_string(index=False))