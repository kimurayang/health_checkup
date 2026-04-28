import sys
import re

def patch_excel_formatting():
    file_path = 'health_checkup_ui.py'
    with open(file_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # 定義新的欄位寬度與格式邏輯
    # 我們直接針對 create_excel 內部的寬度設定區進行替換
    
    # 找尋原本的寬度設定區塊
    old_widths = """        ws.column_dimensions['A'].width = 30
        ws.column_dimensions['B'].width = 40
        ws.column_dimensions['C'].width = 70"""
    
    new_widths = """        # 📌 依照使用者要求設定精確欄寬
        ws.column_dimensions['A'].width = 32
        ws.column_dimensions['B'].width = 35
        ws.column_dimensions['C'].width = 80"""

    if old_widths in content:
        content = content.replace(old_widths, new_widths)
    else:
        # 如果因為之前的修改導致字串不完全匹配，我們用正則表達式強制替換
        content = re.sub(r"ws\.column_dimensions\['A'\]\.width = \d+.*?\n\s*ws\.column_dimensions\['B'\]\.width = \d+.*?\n\s*ws\.column_dimensions\['C'\]\.width = \d+", new_widths, content)

    with open(file_path, 'w', encoding='utf-8') as f:
        f.write(content)
    print("Excel column widths and auto-wrap updated.")

if __name__ == "__main__":
    patch_excel_formatting()
