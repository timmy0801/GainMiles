# GainMiles Employee Data Importer

讀取 Excel 員工資料表，驗證每一筆資料，並透過 REST API 批次建立員工記錄。

## 功能

- 從 `interview_employee_data.xlsx` 的 `Employee Data` 工作表讀取資料
- 對每欄位進行格式與內容驗證
- 驗證通過的資料列逐筆 POST 至 API
- 失敗的資料列記錄至 log，不中斷整體流程

## 驗證規則

| 欄位 | 規則 |
|------|------|
| `employee_id` | 必填，在整份檔案中必須唯一 |
| `name` | 必填，長度 1–50 字元 |
| `email` | 必填，須符合 email 格式 |
| `department` | 必填，不可為空白字串 |
| `salary` | 必填，須為正整數 |
| `join_date` | 必填，格式為 `YYYY-MM-DD` |

## 專案結構

```
GainMiles/
├── main.py                        # 主程式
├── test_main.py                   # 單元測試
├── interview_employee_data.xlsx   # 輸入資料（Excel）
├── requirements.txt               # Python 套件依賴
└── .gitignore
```

## 安裝

```bash
python3 -m venv venv
source venv/bin/activate
pip install -r requirements.txt
```

## 執行

確認 API server 已在 `http://localhost:8000` 啟動，然後執行：

```bash
python main.py
```

## 測試

```bash
python -m pytest test_main.py -v
```

## API 規格

**Endpoint:** `POST http://localhost:8000/api/employees`

**Request body:**
```json
{
  "employee_id": "E001",
  "name": "John Chan",
  "email": "john.chan@company.com",
  "department": "IT",
  "salary": 50000,
  "join_date": "2022-03-15"
}
```

**Response:**
- `201 Created` — `{"id": "E001", "status": "created"}`
- `422 Unprocessable Entity` — `{"detail": "..."}`
