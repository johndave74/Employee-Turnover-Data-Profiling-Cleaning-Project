📘 **Employee Turnover Data Profiling & Cleaning Project**

### *D599 – Data Preparation & Exploration*

## 📌 **Project Overview**

This project focuses on profiling, cleaning, and preparing an **Employee Turnover Dataset** for downstream analytical tasks such as turnover prediction, workforce insights, and HR decision-making.

The dataset originates from a multinational technology firm and contains **10,199 employee records** across **16 variables**, including demographics, job role information, compensation data, and turnover status.

The project performs:

* Comprehensive data profiling
* Data quality assessment
* Cleaning, standardization, and transformation
* Outlier detection and treatment
* Dataset integrity verification (e.g., recalculating salary)

This README documents everything needed to understand, reproduce, and extend the project.

---

# 📂 **Repository Structure**

```
├── data/
│   └── employee_turnover_raw.csv
│   └── employee_turnover_cleaned.csv
│
├── notebooks/
│   └── D599 Task 1 Main.ipynb
│
├── reports/
│   └── D599 Task 1 Report.docx
│
├── scripts/
│   └── cleaning_script.py
│   └── utilities.py
│
├── README.md   ← (this file)
└── requirements.txt
```

---

# 📊 **Dataset Summary**

### **Number of Records:** 10,199

### **Number of Variables:** 16

### **Examples of variables:**

| Variable                        | Type                  | Example                    |
| ------------------------------- | --------------------- | -------------------------- |
| Employee Number                 | Continuous            | 1, 2, 3                    |
| Age                             | Continuous            | 22, 28, 33                 |
| Tenure                          | Discrete              | 1, 2, 6                    |
| Turnover                        | Nominal               | Yes, No                    |
| Hourly Rate                     | Continuous (currency) | $24.37                     |
| Hours Weekly                    | Discrete              | 40                         |
| Compensation Type               | Nominal               | Salary                     |
| Annual Salary                   | Continuous            | 50,689.6                   |
| DrivingCommuterDistance         | Continuous            | 12, 35, 89                 |
| Job Role Area                   | Nominal               | Research, Sales            |
| Gender                          | Nominal               | Male, Female               |
| Marital Status                  | Nominal               | Married                    |
| Num Companies Previously Worked | Discrete              | 1, 3 →                     |
| Annual Professional Dev Hours   | Continuous            | 7, 8, 19                   |
| Paycheck Method                 | Nominal               | Mail Check, Direct Deposit |
| Text Message Opt-In             | Nominal               | Yes, No                    |

---

# 🧪 **Data Profiling Summary**

### ✔ Structure profiling

* Checked record count and variable count (`df.shape`)
* Verified variable data types (`df.info()`)
* Generated descriptive statistics for numeric variables (`df.describe()`)

### ✔ Categorical analysis

* Used `value_counts()` to detect inconsistent categories
* Identified misspellings and capitalization issues

### ✔ Outlier checks

* Used:

  * IQR method
  * Boxplot visualization
  * Salary distribution checks

### ✔ Integrity checks

* Recalculated **Annual Salary = Hourly Rate × Hours Weekly × 52**
* Flagged records where calculated value differed from dataset > 1%

---

# 🛠 **Data Cleaning Steps**

The following steps were implemented using Python (pandas):

### 1️⃣ **Duplicate Removal**

`df.drop_duplicates()`
Ensures each employee record is unique.

### 2️⃣ **Handling Missing Values**

* Numeric fields → imputed with **mean or median**
* Categorical fields → imputed with **mode**

### 3️⃣ **Standardization of Categories**

Cleaned inconsistencies such as:

* “Mail Check”, “Mailed Check”, “Mail check”
* Gender formatting issues

Applied:

```python
df['Paycheck Method'] = df['Paycheck Method'].str.lower().str.strip()
```

### 4️⃣ **Data Type Corrections**

Converted:

* Annual Salary → float
* Hourly Rate → float
* Tenure → integer

### 5️⃣ **Outlier Treatment**

Applied IQR-based **capping/Winsorization** for:

* Annual Salary
* Commuter Distance

### 6️⃣ **Annual Salary Validation**

Recomputed salary to maintain integrity and replaced when deviation >1%.

---

# 🚀 **How to Run the Project**

### **1️⃣ Clone the repository**

```bash
git clone https://github.com/<yourusername>/<repo-name>.git
cd <repo-name>
```

### **2️⃣ Install dependencies**

```bash
pip install -r requirements.txt
```

### **3️⃣ Run the cleaning script**

```bash
python scripts/cleaning_script.py
```

### **4️⃣ View the cleaned dataset**

Output file will be saved to:

```
data/employee_turnover_cleaned.csv
```

---

# 📈 **Key Insights from Profiling**

* Several categorical fields needed standardization.
* Annual Salary had major inconsistencies requiring recalculation.
* Only a few duplicate records existed.
* Missing values were primarily in development hours and companies previously worked.
* Outliers were present in salary and commuting distance.

---

# ⚠️ **Limitations**

* Missing values may not be completely random.
* Imputation introduces statistical bias.
* Outlier capping may remove meaningful real-world variation.
* Dataset lacks timestamps; temporal turnover trends cannot be analyzed.

---

# 📚 **References**

McKinney, W. (2022). *Python for Data Analysis*. O'Reilly Media.
Pandas Documentation (2024).
Waskom, M. (2021). *Seaborn: Statistical Data Visualization*.
Statology. “How to Winsorize Data in Python.” (2023).
WGU D599 Course Resources (2024).

---

# 🤝 **Contribution Guidelines**

Pull requests are welcome for:

* Improved cleaning pipelines
* Visualizations
* Turnover prediction models
* Automated unit tests

Please fork the repo and submit changes via PR.

---

# 📜 **License**

This project is released under the MIT License.
