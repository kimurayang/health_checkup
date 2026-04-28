# 🏥 健檢客戶明細助手 (Health Checkup Guest Detail Assistant)

![Version](https://img.shields.io/badge/version-v3.0.20260428-blue.svg)
![Python](https://img.shields.io/badge/python-3.11%20%7C%203.13-green.svg)
![Platform](https://img.shields.io/badge/platform-Windows-lightgrey.svg)

這是一個專為健檢中心設計的自動化報表工具，能協助同仁在數秒內生成客製化的健檢項目清單。系統支援中英文雙語切換、自動偵測勾選規則、以及非同步報表生成技術。

---

## ✨ 核心功能

*   **🌍 完整雙語支援**：一鍵切換中英文介面，PDF 與 Excel 報表均支援在地化翻譯。
*   **⚡ 極致效能優化**：採用資料快取 (Caching) 技術，方案切換毫秒級響應；非同步線程 (Threading) 確保生成報表時介面不凍結。
*   **🎯 智慧自動偵測 (Auto-presets)**：根據方案名稱或受檢者姓名關鍵字，自動勾選對應的建議項目 (如 PSA, CA-125, MRI 等)。
*   **💰 精準價格計算**：支援單項加選、主方案項目退選 (自動計算 80% 扣除額) 及選配項目配置。
*   **📄 專業報表輸出**：
    *   **PDF 報告**：排版精美，包含類別合併與自動換行。
    *   **Excel 表單**：包含完整的價格明細、加減項摘要與顏色標記。
*   **🛡️ 資料維護工具**：內建同步檢查工具，確保 Excel 結構與翻譯檔 100% 吻合。

---

## 📂 專案檔案結構

```text
D:\Python\health_checkup\
├── health_checkup_ui.py       # 主程式原始碼
├── sync_tool.py               # 資料同步與檢查工具 (新)
├── translations_en.json       # 中英文翻譯資料庫
├── msyh.ttf                   # 微软雅黑字型 (PDF 報表所需)
├── 健檢客戶明細助手.spec        # PyInstaller 打包設定檔
├── 中心全組套.xlsx              # 中文核心資料庫 (主控)
├── 中心全組套_EN.xlsx           # 英文對應資料庫 (結構須與中文一致)
└── 使用說明.txt                # 給終端使用者的簡易手冊
```

---

## 🛠️ 開發環境與安裝

### 環境需求
*   Windows 10/11 (64-bit)
*   Python 3.11 或 3.13

### 安裝依賴庫
```cmd
pip install pandas openpyxl reportlab pillow
```

### 執行程式
```cmd
python health_checkup_ui.py
```

---

## ⚙️ 維護指南

### 1. 更新健檢資料
直接編輯 `中心全組套.xlsx` 即可更新方案內容與價格。修改完成後，建議執行同步工具。

### 2. 使用同步工具 (`sync_tool.py`)
為了確保中英文 Excel 結構一致且翻譯完整，每次修改 Excel 後請執行：
```cmd
python sync_tool.py
```
該工具會自動檢查：
*   **翻譯完整性**：是否有新增加的中文項目尚未翻譯。
*   **結構一致性**：中英文 Excel 的行數與項目位置是否一一對應。

### 3. 打包執行檔 (.exe)
使用預設的 `.spec` 檔案進行打包，確保資源檔正確封裝：
```cmd
pyinstaller 健檢客戶明細助手.spec
```

---

## 💡 技術支援與維護
*   **版本記錄**：v3.0.20260428 (穩定版)
*   **核心技術**：Tkinter, Pandas, ReportLab, Threading, JSON Caching.
*   **開發者**：Yunotang

---
*Sugar, Spice, and Everything Nice!*
