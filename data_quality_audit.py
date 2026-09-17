import pandas as pd

FILE = "Superstore_Product_Count_Analysis.xlsx"

df = pd.read_excel(FILE, sheet_name="Superstore Data")

print("DATA QUALITY AUDIT")
print("=" * 50)
print("Rows:", len(df))
print("Columns:", len(df.columns))

# 1. Missing values
print("\n1. MISSING VALUES")
print(df.isna().sum())

# 2. Duplicate rows and IDs
print("\n2. DUPLICATES")
print("Duplicate rows:", df.duplicated().sum())
print("Duplicate Product IDs:", df["Product ID"].duplicated().sum())

# 3. Product ID format
print("\n3. PRODUCT ID FORMAT")
bad_id = ~df["Product ID"].astype(str).str.fullmatch(r"PROD-\d{4}", na=False)
print("Invalid Product IDs:", bad_id.sum())

# 4. Date validation
print("\n4. DATE VALIDATION")
dates = pd.to_datetime(df["Order Date"], errors="coerce")
print("Invalid dates:", dates.isna().sum())
print("Outside 2025:", ((dates < "2025-01-01") | (dates > "2025-12-31")).sum())

# 5. Range checks
print("\n5. RANGE CHECKS")
print("Invalid Quantity:",
      ((df["Quantity"] <= 0) | (df["Quantity"] % 1 != 0)).sum())
print("Invalid Discount:",
      ((df["Discount"] < 0) | (df["Discount"] > 1)).sum())
print("Invalid Sales:", (df["Sales"] <= 0).sum())

# 6. Allowed values
print("\n6. ALLOWED VALUES")
print("Invalid Category:",
      (~df["Category"].isin(["Furniture", "Office Supplies", "Technology"])).sum())
print("Invalid Region:",
      (~df["Region"].isin(["Central", "East", "South", "West"])).sum())
print("Invalid Segment:",
      (~df["Segment"].isin(["Consumer", "Corporate", "Home Office"])).sum())

# 7. Category/Sub-Category consistency
valid_map = {
    "Furniture": {"Tables", "Furnishings", "Chairs", "Bookcases"},
    "Office Supplies": {"Art", "Binders", "Labels", "Paper", "Storage"},
    "Technology": {"Phones", "Copiers", "Accessories", "Machines", "Computers"},
}
bad_cat_sub = df.apply(
    lambda r: r["Sub-Category"] not in valid_map.get(r["Category"], set()),
    axis=1
)
print("\n7. CATEGORY/SUB-CATEGORY CONSISTENCY")
print("Inconsistent records:", bad_cat_sub.sum())

# 8. Product consistency
conflicts = (
    df.groupby("Product Name")[["Category", "Sub-Category"]]
      .nunique()
)
print("\n8. PRODUCT CONSISTENCY")
print("Product names with conflicting mappings:",
      ((conflicts["Category"] > 1) | (conflicts["Sub-Category"] > 1)).sum())

# Clean and export
cleaned = df.drop_duplicates().copy()
cleaned["Order Date"] = pd.to_datetime(cleaned["Order Date"], errors="coerce")
cleaned.to_csv("cleaned_sample.csv", index=False)

print("\nAudit complete. cleaned_sample.csv created.")
