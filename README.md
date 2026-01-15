# Sales Analytics System

A complete Python-based sales analytics project that processes raw sales data, performs validations and advanced analytics, integrates external product data using a public API, enriches transactions, and generates a comprehensive business report.

This project is structured exactly as per the assignment requirements and follows modular, production-style Python coding practices.

---

## Project Overview

The Sales Analytics System performs the following end-to-end workflow:

1. Reads raw sales data from a pipe-delimited text file
2. Parses and cleans transaction records
3. Validates and filters incorrect transactions
4. Performs detailed sales analytics (region, product, customer, date-based)
5. Fetches product information from DummyJSON API
6. Enriches sales data using API information
7. Saves enriched data to a new file
8. Generates a comprehensive formatted sales report

---

## Project Structure

```
sales-analytics-system/
│
├── main.py                     # Main execution script
├── requirements.txt            # Project dependencies
             
│
├── utils/
│   ├── report_generator.py
│   ├── file_handler.py         # File reading, parsing, validation (Task 1)
│   ├── data_processor.py       # Sales analytics (Task 2)
│   ├── api_handler.py          # API integration & enrichment (Task 3)
│
├── data/
│   └── sales_data.txt          # Input sales data file
    └── enriched_sales_data.txt # Enriched output file (auto-generated)
│
├── output/
│   └── sales_report.txt        # Final analytics report (auto-generated)
│
└── README.md                   # Project documentation
```

---

## Technologies & Tools Used

| Tool / Library    | Purpose                         |
| ----------------- | ------------------------------- |
| Python 3.10+      | Core programming language       |
| requests          | API calls to DummyJSON          |
| DummyJSON API     | External product enrichment     |
| Standard Library  | os, datetime, collections, math |
| VS Code / Jupyter | Development & testing           |

---

##  Installation & Setup

### 1. Clone or Download the Project

Place all files in a single project directory.

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Verify Input File

Ensure `sales_data.txt` exists in the project data folder.

---

## How to Run the Project

Run the system using:

```bash
python main.py
```

---

## Assignment Tasks Breakdown

### Part 1: File Handling & Validation (`file_handler.py`)

**Implemented Functions:**

* `read_sales_data()`
* `parse_transactions()`
* `validate_and_filter()`

**Features:**

* Encoding-safe file reading
* Skips invalid or malformed rows
* Validation rules for IDs, quantity, price
* Returns clean and valid transaction list

---

### Part 2: Sales Analytics (`data_processor.py`)

**Implemented Analytics:**

* Total revenue calculation
* Region-wise sales distribution
* Top selling products
* Customer purchase analysis
* Daily sales trend
* Peak sales day detection
* Low performing products

---

### Part 3: API Integration (`api_handler.py`)

**API Used:**
DummyJSON Products API

**Implemented Functions:**

* `fetch_all_products()`
* `create_product_mapping()`
* `enrich_sales_data()`
* `save_enriched_data()`

**Key Highlights:**

* Extracts numeric ProductID (e.g., P101 → 101) but since no id was present in json acording to trasaction data, no data related to API is extracted.
* Matches sales data with API products
* Handles missing products gracefully
* Adds API_Category, API_Brand, API_Rating
* Saves enriched data to file

---

### Part 4: Report Generation (`generate_sales_report`)

**Report Includes:**

1. Header & metadata
2. Overall summary
3. Region-wise performance
4. Top 5 products
5. Top 5 customers
6. Daily sales trends
7. Product performance analysis
8. API enrichment summary

## Sample Console Output

<img width="855" height="933" alt="image" src="https://github.com/user-attachments/assets/b2ad485e-03ec-4a90-af63-b5e2c5e96338" />





---

## 📄 License

This project is created for academic and learning purposes only.
