import pandas as pd
import json
import os
import sys

# ==========================================
# 🏥 健檢資料同步與檢查工具 (v1.0)
# ==========================================

CONFIG = {
    "ZH_EXCEL": "中心全組套.xlsx",
    "EN_EXCEL": "中心全組套_EN.xlsx",
    "TRANS_JSON": "translations_en.json"
}

def load_data():
    """載入 Excel 與 JSON 資料"""
    results = {}
    try:
        results['zh_df'] = pd.read_excel(CONFIG["ZH_EXCEL"], header=None)
        results['en_df'] = pd.read_excel(CONFIG["EN_EXCEL"], header=None)
        with open(CONFIG["TRANS_JSON"], 'r', encoding='utf-8') as f:
            results['trans'] = json.load(f)
        return results
    except Exception as e:
        print(f"❌ 錯誤: 無法載入必要檔案 - {e}")
        return None

def check_translations(data):
    """檢查翻譯檔是否包含所有 Excel 中的項目"""
    zh_df = data['zh_df']
    trans = data['trans']
    
    # 提取第 2 欄 (項目名稱)，從第 4 行開始
    items = set(zh_df.iloc[3:, 1].dropna().astype(str).str.strip())
    missing = [i for i in items if i not in trans]
    
    print("\n--- 🔍 [1/2] 翻譯完整性檢查 ---")
    if not missing:
        print("✅ 所有項目皆已存在於翻譯檔中。")
    else:
        print(f"⚠️ 發現 {len(missing)} 個項目缺漏翻譯：")
        for i, item in enumerate(missing, 1):
            print(f"  {i}. \"{item}\": \"\"")
        print("\n💡 提示：您可以將上述內容直接複製到 translations_en.json 中補全。")

def check_excel_alignment(data):
    """檢查中英文 Excel 結構是否對齊"""
    zh_df = data['zh_df']
    en_df = data['en_df']
    
    print("\n--- ⚖️ [2/2] 中英文 Excel 對齊檢查 ---")
    
    # 1. 檢查行數是否相同
    if len(zh_df) != len(en_df):
        print(f"❌ 行數不一致：中文版有 {len(zh_df)} 行，英文版有 {len(en_df)} 行。")
    else:
        print("✅ 行數一致。")
        
    # 2. 逐行比對項目名稱 (第 2 欄)
    mismatches = []
    for i in range(min(len(zh_df), len(en_df))):
        zh_val = str(zh_df.iloc[i, 1]).strip()
        en_val = str(en_df.iloc[i, 1]).strip()
        
        # 排除掉 nan 或標題行
        if zh_val.lower() == 'nan' and en_val.lower() == 'nan':
            continue
            
        # 比對 (由於英文版內容可能是翻譯過的，這裡我們主要檢查是否有結構性位移)
        # 如果兩邊都不為空，但某一邊為空，則視為不對齊
        if (zh_val == 'nan') != (en_val == 'nan'):
            mismatches.append((i + 1, zh_val, en_val))
            
    if not mismatches:
        print("✅ 檔案結構看起來已對齊。")
    else:
        print(f"⚠️ 發現 {len(mismatches)} 處結構不對齊 (行號參考 Excel)：")
        for line, zh, en in mismatches[:10]:
            print(f"  Row {line}: 中文='{zh}', 英文='{en}'")
        if len(mismatches) > 10:
            print(f"  ... 還有 {len(mismatches) - 10} 處未列出。")

def main():
    print("🚀 啟動健檢資料同步檢查...")
    data = load_data()
    if not data:
        return
        
    check_translations(data)
    check_excel_alignment(data)
    print("\n✨ 檢查完畢。")

if __name__ == "__main__":
    main()
