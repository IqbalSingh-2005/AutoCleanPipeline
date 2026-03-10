<p align="center">
  <img src="https://img.shields.io/github/license/IqbalSingh-2005/AutoCleanPipeline?style=for-the-badge&logo=opensourceinitiative&logoColor=white&color=0080ff" alt="license">
  <img src="https://img.shields.io/github/last-commit/IqbalSingh-2005/AutoCleanPipeline?style=for-the-badge&logo=git&logoColor=white&color=0080ff" alt="last-commit">
  <img src="https://img.shields.io/github/languages/top/IqbalSingh-2005/AutoCleanPipeline?style=for-the-badge&color=0080ff" alt="top-language">
  <img src="https://img.shields.io/github/languages/count/IqbalSingh-2005/AutoCleanPipeline?style=for-the-badge&color=0080ff" alt="language-count">
</p>

<h1 align="center">🧹 AutoCleanPipeline</h1>

<p align="center">
  <strong>An automated data-cleaning pipeline with a modern Django web dashboard.</strong><br>
  Upload messy CSV / Excel / JSON files and get back clean, analysis-ready data — no code required.
</p>

---

## 📑 Table of Contents

- [📍 Overview](#-overview)
- [✨ Features](#-features)
- [🛠️ Tech Stack](#️-tech-stack)
- [📁 Project Structure](#-project-structure)
- [🚀 Getting Started](#-getting-started)
  - [☑️ Prerequisites](#️-prerequisites)
  - [⚙️ Installation](#️-installation)
  - [🖥️ Run Locally (Web Dashboard)](#️-run-locally-web-dashboard)
  - [🤖 Run as a Python Script (CLI)](#-run-as-a-python-script-cli)
- [🌐 API Endpoints](#-api-endpoints)
- [☁️ Deployment (Render.com)](#️-deployment-rendercom)
- [🧪 Testing](#-testing)
- [🔰 Contributing](#-contributing)
- [🎗 License](#-license)

---

## 📍 Overview

**AutoCleanPipeline** is a full-stack data-cleaning tool that automates the most tedious preprocessing steps every data analyst faces:

| Problem | What AutoCleanPipeline does |
|---|---|
| Inconsistent column names | Lowercases, strips whitespace, replaces spaces with `_` |
| Mixed data types | Detects numeric strings and converts them automatically |
| Missing values | Fills numeric nulls with the column median |
| Outliers | Flags outliers using the IQR method |
| Manual charting | Interactive charts (line, bar, scatter, area, histogram, box) |
| Exporting results | One-click Excel (`.xlsx`) and PDF chart download |

The project ships two interfaces:

1. **Web Dashboard** — a Django + Tailwind CSS UI for uploading files, viewing summaries, generating interactive charts, and downloading results.
2. **Python API / CLI** — the `AutoCleanPipeline` class can be imported directly into any Python script or notebook.

---

## ✨ Features

- 📂 **Multi-format file support** — CSV, Excel (`.xlsx` / `.xls`), JSON, Parquet, Feather, ORC, Pickle, FWF, HTML, HDF
- 🔤 **Column standardisation** — snake_case names, duplicate column removal
- 🔢 **Smart type conversion** — numeric strings auto-cast to `float64`
- 🩹 **Missing-value imputation** — median fill for all numeric columns
- 📐 **IQR outlier detection** — flags outliers without dropping rows
- 📊 **Interactive charts** — six chart types with configurable X / Y axes
- 📗 **Excel export** — download cleaned data as a timestamped `.xlsx` file
- 📄 **PDF chart export** — high-resolution PDF of the current chart
- 🗂️ **Data summary cards** — row / column counts, memory usage, null counts, duplicate counts
- 🔧 **Modular Python API** — use any individual cleaning step in your own code

---

## 🛠️ Tech Stack

| Layer | Technology |
|---|---|
| Backend framework | Django 6 |
| Data processing | pandas 3, NumPy 2 |
| Visualisation | Matplotlib 3 |
| File formats | openpyxl, pyarrow |
| Static files | WhiteNoise |
| Production server | Gunicorn |
| Styling | Tailwind CSS (via CDN) |

---

## 📁 Project Structure

```
AutoCleanPipeline/
├── AutoCleanPipeline/          # Core Python package
│   ├── main.py                 # AutoCleanPipeline class — Python API entry point
│   ├── requirements.txt        # Python dependencies
│   ├── build.sh                # Render.com build script
│   ├── src/
│   │   ├── cleaner.py          # column_cleaner — standardise, type-convert, fill nulls, IQR outliers
│   │   ├── loader.py           # FileLoader     — multi-format file reader + file-picker dialog
│   │   ├── visualizer.py       # generate_chart — base64 chart renderer (6 chart types)
│   │   └── validator.py        # stats          — data-summary generator
│   ├── AutoCleanSet/           # Django project
│   │   ├── AutoClean/          # Django settings, URLs, WSGI
│   │   └── AutoCleanUI/        # Main Django app
│   │       ├── models.py       # UploadedFile model
│   │       ├── views.py        # Dashboard, upload, chart, and download views
│   │       ├── urls.py         # URL routing
│   │       └── templates/      # HTML templates (Tailwind CSS)
│   └── test/
│       └── Salary.csv          # Sample dataset for testing
├── AutoCleanPipeline.slnx      # Visual Studio solution file
└── LICENSE.txt
```

---

## 🚀 Getting Started

### ☑️ Prerequisites

- Python **3.10+**
- `pip` (bundled with Python)
- *(Optional)* a virtual environment tool such as `venv` or `conda`

### ⚙️ Installation

```bash
# 1. Clone the repository
git clone https://github.com/IqbalSingh-2005/AutoCleanPipeline.git
cd AutoCleanPipeline/AutoCleanPipeline

# 2. Create and activate a virtual environment (recommended)
python -m venv env

# Windows
env\Scripts\activate

# macOS / Linux
source env/bin/activate

# 3. Install dependencies
pip install -r requirements.txt
```

### 🖥️ Run Locally (Web Dashboard)

```bash
# From the AutoCleanPipeline/ directory
cd AutoCleanSet

# Apply database migrations (first run only)
python manage.py migrate

# Start the development server
python manage.py runserver
```

Open **http://127.0.0.1:8000** in your browser.

**Dashboard walkthrough:**

1. Click **Upload Files** in the navbar and select a CSV, Excel, or JSON file.
2. The dashboard shows data-summary cards (rows, columns, memory usage, null counts, duplicates).
3. Choose an X-axis column, Y-axis column, and chart type, then click **Generate Chart**.
4. Click the green **Download Excel** button to export the cleaned dataset as `.xlsx`.
5. Click the red **Download PDF** button to export the current chart as a high-resolution PDF.

### 🤖 Run as a Python Script (CLI)

```python
from main import AutoCleanPipeline

pipeline = AutoCleanPipeline()

# Option A — full pipeline (opens a file-picker dialog)
df = pipeline.run_full_pipeline()

# Option B — step by step with an explicit file path
pipeline.load_data("test/Salary.csv")
summary = pipeline.get_summary()              # dict: rows, cols, nulls, dtypes …
df      = pipeline.clean_all()                # standardise + type-convert + fill nulls
df      = pipeline.detect_outliers("salary")  # adds a 'salary_outlier' boolean column
pipeline.generate_stats()                     # prints describe() for every numeric column
pipeline.visualize()                          # renders line / scatter / bar charts

print(df.head())
```

**Use individual cleaning steps:**

```python
pipeline.load_data("my_data.csv")

pipeline.standardize_columns()   # snake_case names, remove duplicate columns
pipeline.convert_data_types()    # cast numeric-looking strings to float64
pipeline.handle_missing_data()   # median-fill numeric nulls
pipeline.detect_outliers("age")  # adds 'age_outlier' boolean column
```

---

## 🌐 API Endpoints

| Method | URL | Description |
|---|---|---|
| `GET` | `/` | Main dashboard — upload & visualise |
| `POST` | `/upload/` | Upload a data file |
| `POST` | `/generate-chart/` | Generate a chart (returns JSON with base64 image) |
| `GET` | `/download-excel/` | Download cleaned data as `.xlsx` |
| `POST` | `/download-chart-pdf/` | Download the current chart as `.pdf` |

**Generate chart — example request body:**

```json
{
  "x_column": "age",
  "y_column": "salary",
  "chart_type": "scatter"
}
```

Supported `chart_type` values: `line`, `scatter`, `bar`, `area`, `histogram`, `box`.

---

## ☁️ Deployment (Render.com)

A complete deployment walkthrough is available in [`RENDER_DEPLOYMENT.md`](AutoCleanPipeline/RENDER_DEPLOYMENT.md).

Quick reference:

| Setting | Value |
|---|---|
| **Runtime** | Python 3 |
| **Root Directory** | `AutoCleanPipeline` |
| **Build Command** | `pip install -r requirements.txt && cd AutoCleanSet && python manage.py collectstatic --no-input && python manage.py migrate` |
| **Start Command** | `cd AutoCleanSet && gunicorn AutoClean.wsgi:application` |

Required environment variables:

| Key | Example value |
|---|---|
| `DEBUG` | `False` |
| `SECRET_KEY` | *(generate with Django's `get_random_secret_key()`)* |
| `ALLOWED_HOSTS` | `*.onrender.com` |

---

## 🧪 Testing

A sample dataset is included at `test/Salary.csv`.  
To verify the pipeline end-to-end:

```bash
cd AutoCleanPipeline
python -c "
from main import AutoCleanPipeline
p = AutoCleanPipeline()
p.load_data('test/Salary.csv')
print(p.get_summary())
df = p.clean_all(outlier_column='salary')
print(df.head())
"
```

---

## 🔰 Contributing

Contributions are welcome!

1. Fork the repository.
2. Create a feature branch: `git checkout -b feature/my-feature`
3. Commit your changes: `git commit -m "feat: add my feature"`
4. Push the branch: `git push origin feature/my-feature`
5. Open a Pull Request with a short description of what was changed and why.

---

## 🎗 License

This project is licensed under the terms found in [`LICENSE.txt`](LICENSE.txt).

---

<p align="center">Made with ❤️ by <a href="https://github.com/IqbalSingh-2005">IqbalSingh-2005</a></p>
