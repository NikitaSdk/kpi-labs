import time
from datetime import datetime

import pandas as pd
import requests


START_DATE = "1996-01-01"
END_DATE = datetime.today().strftime("%Y-%m-%d")
OUTPUT_FILE = "currency_monthly.csv"


def get_rate(date_str: str, currency: str, retries: int = 3, pause: float = 1.5):
    url = "https://bank.gov.ua/NBUStatService/v1/statdirectory/exchange"
    params = {
        "date": date_str,
        "valcode": currency.upper(),
        "json": ""
    }

    for attempt in range(1, retries + 1):
        try:
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()

            data = response.json()

            if not isinstance(data, list) or len(data) == 0:
                return None

            return float(data[0]["rate"])

        except Exception as e:
            if attempt < retries:
                time.sleep(pause)
            else:
                print(f"⚠ Не вдалося отримати {currency} на {date_str}: {e}")

    return None


def build_monthly():
    dates = pd.date_range(start=START_DATE, end=END_DATE, freq="MS")

    rows = []

    for d in dates:
        date_str = d.strftime("%Y%m%d")

        usd = get_rate(date_str, "USD")
        gbp = get_rate(date_str, "GBP")


        usd_gbp = None
        if usd is not None and gbp is not None and gbp != 0:
            usd_gbp = usd / gbp

        rows.append({
            "date": d.strftime("%Y-%m-%d"),
            "year": d.year,
            "month": d.month,
            "USD_UAH": usd,
            "USD_GBP": usd_gbp
        })

        print(f"Завантажено: {d.strftime('%Y-%m')}")

    df = pd.DataFrame(rows)

    # заповнення пропусків
    df["USD_UAH"] = pd.to_numeric(df["USD_UAH"], errors="coerce").ffill().bfill()
    df["USD_GBP"] = pd.to_numeric(df["USD_GBP"], errors="coerce").ffill().bfill()

    # округлення
    df["USD_UAH"] = df["USD_UAH"].round(4)
    df["USD_GBP"] = df["USD_GBP"].round(6)

    return df


if __name__ == "__main__":
    try:
        df = build_monthly()
        df.to_csv(OUTPUT_FILE, index=False, encoding="utf-8-sig")

        print("\nГОТОВО!")
        print(f"Файл створено: {OUTPUT_FILE}")
        print(f"Кількість рядків: {len(df)}")

        print("\nПерші 10 рядків:")
        print(df.head(10).to_string(index=False))

    except Exception as e:
        print("Помилка:")
        print(str(e))