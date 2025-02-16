import pandas as pd
import json
import  re

def load_database(file_path="products.json"):
    try:
        with open(file_path, "r", encoding="utf-8") as file:
            return json.load(file)
    except FileNotFoundError:
        print("⚠️ فایل JSON وجود ندارد، ایجاد یک فایل جدید...")
        with open(file_path, "w", encoding="utf-8") as file:
            file.write("[]")
        return []
    except Exception as e:
        print(f"Error loading JSON file: {e}")
        return []

def excel_to_json(file_path):
    try:
        df = pd.read_excel(file_path)
        df.columns = [str(col).strip() for col in df.columns]  # حذف فضای اضافی از عناوین ستون‌ها
        data = df.to_dict(orient="records")
        with open("products.json", "w", encoding="utf-8") as file:
            json.dump(data, file, ensure_ascii=False, indent=4)
        return True
    except Exception as e:
        print(f"Error converting Excel to JSON: {e}")
        return False



def clean_query(query):
    return re.sub(r"[^a-zA-Z0-9آ-ی ]", "", query).strip()


def search_product(query, database, max_results=20):


    if database is None:
        return None

    query = clean_query(query)
    query_words = query.split()

    results = []

    for item in database:
        match = True
        for word in query_words:
            if word.isdigit():
                if not any(str(value) == word for value in item.values()):
                    match = False
                    break
            else:
                if not any(word.lower() in str(value).lower() for value in item.values()):
                    match = False
                    break
        if match:
            results.append(item)

    if not results:
        return None

    results = results[:max_results]

    header = "✅ کالای درخواستی شما با مشخصات زیر موجود می‌باشد:\n"

    response = "\n\n".join(["\n".join([f"{key}: {value}" for key, value in item.items()]) for item in results])

    store_info = "\n\n🏪 فروشگاه: صفرزاده\n📞 تلفن‌های تماس:\n📌 02133944061\n📌 02133993282\n📌 02133993283\n📌 02133945943"

    return header + response + store_info

