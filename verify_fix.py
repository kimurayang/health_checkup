import pandas as pd
import os
import re

def clean_cat_name(n):
    if not n or str(n).lower() == 'nan': return ""
    return str(n).replace("(", "").replace(")", "").replace(" ", "").replace("　", "").strip()

def safe_parse_price(v):
    if pd.isna(v) or not str(v).strip(): return 0
    try:
        c = re.sub(r'[^\d]', '', str(v))
        return int(c) if c else 0
    except: return 0

excel_path = '中心全組套.xlsx'
xl = pd.ExcelFile(excel_path)
df_main = pd.read_excel(xl, sheet_name=xl.sheet_names[0], header=None)

# 1. 載入主方案
packages = {}
sc, ec = 3, min(51, len(df_main.columns))
ns, ps = df_main.iloc[0, sc:ec], df_main.iloc[1, sc:ec]
last_n = ""
for i in range(len(ns)):
    n, p = str(ns.iloc[i]).strip(), str(ps.iloc[i]).strip()
    if n == 'nan' or not n: n = last_n
    else: last_n = n
    if n and n != 'nan':
        g = "男" if "(男)" in p else "女" if "(女)" in p else ""
        k = f"{n} ({g})" if g else f"{n} (方案{i+1})"
        packages[k] = {"price": p, "col_idx": sc + i}

# 2. 載入單項加選
add_on_items = []
if len(xl.sheet_names) > 1:
    df_addon = pd.read_excel(xl, sheet_name=xl.sheet_names[1], header=None)
    carrying_cat = ""
    for idx in range(1, len(df_addon)):
        c_val = str(df_addon.iloc[idx, 0]).strip()
        if c_val and c_val.lower() != 'nan': carrying_cat = c_val
        item = str(df_addon.iloc[idx, 1]).strip()
        if item and item.lower() != 'nan':
            add_on_items.append({"cat": carrying_cat, "item": item})

# 3. 模擬選擇 "全面型白金防癌護心(男)"
target_pkg = "全面型白金防癌護心(男)"
# 尋找最接近的 Key
pkg_key = next((k for k in packages.keys() if "全面型" in k and "(男)" in k), None)
print(f"Target Package Key: {pkg_key}")

if not pkg_key:
    print("Could not find the package. Available packages starting with 全面:")
    print([k for k in packages.keys() if "全面" in k])
    exit()

col_idx = packages[pkg_key]["col_idx"]
items_df = df_main.iloc[3:].copy()

# 4. 執行過濾邏輯 (與 health_checkup_ui.py 同步)
main_items_clean = []
for idx, row in items_df.iterrows():
    val = str(row.iloc[col_idx]).strip().lower()
    if val != 'nan' and val != "":
        item_name = str(row.iloc[1]).strip().replace("\n", "").replace(" ", "")
        if item_name:
            main_items_clean.append(item_name)

print(f"Main items count in package: {len(main_items_clean)}")

filtered = []
for i, info in enumerate(add_on_items):
    ad_item_raw = str(info['item']).strip()
    ad_item_clean = ad_item_raw.replace("\n", "").replace(" ", "")
    
    is_duplicate = False
    for m_item in main_items_clean:
        if ad_item_clean in m_item or m_item in ad_item_clean:
            is_duplicate = True
            matched_with = m_item
            break
    
    if is_duplicate:
        if "脊椎" in ad_item_raw or "主動脈" in ad_item_raw:
            print(f"SUCCESS: Filtered out '{ad_item_raw}' because it matched with '{matched_with}' in main package.")
        continue
        
    filtered.append(ad_item_raw)

# 檢查是否還有遺漏
for item in filtered:
    if "脊椎" in item or "主動脈" in item:
        print(f"FAILURE: '{item}' is still in the filtered list!")

print("Verification completed.")
