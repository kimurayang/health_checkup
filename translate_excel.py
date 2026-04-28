import pandas as pd
import json
import os
from openpyxl import load_workbook

def translate_excel():
    source_file = '中心全組套.xlsx'
    output_file = '中心全組套_EN.xlsx'
    dict_file = 'translations_en.json'
    
    if not os.path.exists(dict_file):
        print(f"Error: {dict_file} not found.")
        return

    with open(dict_file, 'r', encoding='utf-8') as f:
        trans_dict = json.load(f)
    
    # 建立一個清理後的字典用於匹配
    clean_dict = {k.replace("\n", "").replace(" ", ""): v for k, v in trans_dict.items()}

    def get_trans(val):
        if not val or pd.isna(val): return val
        s_val = str(val).strip()
        # 1. 精確匹配
        if s_val in trans_dict: return trans_dict[s_val]
        # 2. 清理後匹配
        c_val = s_val.replace("\n", "").replace(" ", "")
        if c_val in clean_dict: return clean_dict[c_val]
        # 3. 關鍵字處理
        m = {"男": "Male", "女": "Female", "方案": "Pkg"}
        res = s_val
        for k, v in m.items():
            if k in res: res = res.replace(k, v)
        return res

    print(f"Translating {source_file}...")
    
    # 使用 pd.ExcelWriter 處理多個工作表
    with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
        xl = pd.ExcelFile(source_file)
        for sheet_name in xl.sheet_names:
            df = pd.read_excel(xl, sheet_name=sheet_name, header=None)
            # 遍歷所有單元格進行翻譯
            translated_df = df.map(get_trans)
            translated_df.to_excel(writer, sheet_name=sheet_name, index=False, header=False)
            
    print(f"Success! English version saved as {output_file}")

if __name__ == "__main__":
    translate_excel()
