import os, json, csv
from datetime import datetime

# Step 1: Reading the CSV File
def read_csv(file_path):
    data = []
    with open(file_path, mode='r', encoding='utf-8') as file:
        reader = csv.DictReader(file)
        for row in reader:
            data.append(row)
    return data

csv_file_path = os.path.join(os.getcwd(), "acw_user_data.csv")
csv_data = read_csv(csv_file_path)

# Step 2: Structuring Data
def nest_data(row):
    dependants = row.get("Dependants", "").strip()
    if not dependants.isdigit():
        dependants = None

    retired = row.get("Retired", "").strip().lower() == "true"

    return {
        "first_name": row.get("First Name"),
        "second_name": row.get("Last Name"),
        "age": int(row.get("Age (Years)", 0)),
        "sex": row.get("Sex"),
        "retired": retired,
        "marital_status": row.get("Marital Status"),
        "dependants": dependants,
        "salary": int(row.get("Yearly Salary (Dollar)", 0)),
        "pension": int(row.get("Yearly Pension (Dollar)", 0)),
        "company": row.get("Employer Company"),
        "commute_distance": float(row.get("Distance Commuted to Work (Km)", 1.0)),
        "Vehicle": {
            "make": row.get("Vehicle Make"),
            "model": row.get("Vehicle Model"),
            "year": row.get("Vehicle Year"),
            "category": row.get("Vehicle Type")
        },
        "Credit Card": {
            "start_date": row.get("Credit Card Start Date"),
            "end_date": row.get("Credit Card Expiry Date"),
            "number": row.get("Credit Card Number"),
            "ccv": row.get("Credit Card CVV"),
            "iban": row.get("Bank IBAN")
        },
        "Address": {
            "street": row.get("Address Street"),
            "city": row.get("Address City"),
            "postcode": row.get("Address Postcode")
        }
    }


# Step 3: Handling Missing Data and Tracking Problematic Rows
def process_data(data):
    _processed_data = []
    problematic_rows = []
    for idx, row in enumerate(data):
        nested_row = nest_data(row)
        if nested_row["dependants"] is None:
            problematic_rows.append(idx)
            nested_row["dependants"] = 0
        _processed_data.append(nested_row)
    print("Problematic rows for dependants:", problematic_rows)
    return _processed_data

# Step 4: Saving Processed Data to JSON
def save_to_json(data, file_name="processed.json"):
    with open(file_name, "w", encoding="utf-8") as file:
        json.dump(data, file, ensure_ascii=False, indent=4)

processed_data = process_data(csv_data)
save_to_json(processed_data, "processed.json")


# Step 5: Separation by Retirement Status
def separate_by_retirement(data):
    retired = [entry for entry in data if entry["retired"] is True]
    employed = [entry for entry in data if entry["retired"] is False]
    with open("retired.json", "w", encoding="utf-8") as file:
        json.dump(retired, file, ensure_ascii=False, indent=4)
    with open("employed.json", "w", encoding="utf-8") as file:
        json.dump(employed, file, ensure_ascii=False, indent=4)

separate_by_retirement(processed_data)


# Step 6: Flagging Outdated Credit Cards
def flag_outdated_credit_cards(data):
    outdated_cards = []

    for entry in data:
        start_date = entry["Credit Card"]["start_date"]
        end_date = entry["Credit Card"]["end_date"]

        if start_date and end_date:
            start_year = int(start_date.split("/")[-1])
            end_year = int(end_date.split("/")[-1])

            start_year += 2000 if start_year < 100 else 0
            end_year += 2000 if end_year < 100 else 0

            if (end_year - start_year) > 10:
                outdated_cards.append(entry)

    with open("remove_ccard.json", "w", encoding="utf-8") as file:
        json.dump(outdated_cards, file, ensure_ascii=False, indent=4)

flag_outdated_credit_cards(processed_data)


# Step 7: Salary-Commute Calculation and Sorting
def calculate_salary_commute(data):
    for entry in data:
        commute_distance = entry["commute_distance"]
        if commute_distance > 1:
            entry["SalaryCommute"] = entry["salary"] / commute_distance
        else:
            entry["SalaryCommute"] = entry["salary"]

    sorted_data = sorted(data, key=lambda x: x["SalaryCommute"], reverse=True)

    with open("commute.json", "w", encoding="utf-8") as file:
        json.dump(sorted_data, file, ensure_ascii=False, indent=4)

calculate_salary_commute(processed_data)
