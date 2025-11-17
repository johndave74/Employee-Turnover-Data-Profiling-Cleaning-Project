import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import warnings

def setup_environment():
    """Set up the environment and print library versions."""
    warnings.filterwarnings('ignore')
    print("pandas:", pd.__version__)
    print("numpy:", np.__version__)
    print("seaborn:", sns.__version__)

def load_data(data_path):
    """Load the dataset from CSV file."""
    df = pd.read_csv(data_path)
    return df

def profile_variables(df):
    """Profile each variable in the dataset."""
    profile = []
    for col in df.columns:
        s = df[col]
        # determine quantitative vs qualitative
        if pd.api.types.is_numeric_dtype(s):
            var_type = "Quantitative/Numerical"
            subtype = "Continuous" if s.nunique() > 20 else "Discrete"
        else:
            var_type = "Qualitative/Categorical"
            unique_vals = s.dropna().unique()
            # crude ordinal inference
            ordinal_keywords = {"general","medium","high","junior","senior","entry","mid","senior"}
            if len(unique_vals) <= 12 and any(isinstance(x, str) and x.strip().lower() in ordinal_keywords for x in unique_vals):
                subtype = "Ordinal (inferred)"
            else:
                subtype = "Nominal"
        sample_values = s.dropna().astype(str).unique()[:8].tolist()
        missing = int(s.isna().sum())
        profile.append({
            "variable": col,
            "data_type": var_type,
            "subtype": subtype,
            "n_unique": int(s.nunique(dropna=True)),
            "missing": missing,
            "sample_values": sample_values
        })
    
    profile_df = pd.DataFrame(profile)
    print(profile_df.to_string(index=False))
    return profile_df

def inspect_data(df):
    """Inspect the data and display basic information."""
    rows, columns = df.shape
    print(f"The dataset has {rows} rows and {columns} columns")
    print("Columns:", df.columns, "\n")
    print("Descriptive statistics:")
    descriptive_stats = df.describe(include='all').transpose()
    print(descriptive_stats)
    return descriptive_stats

def handle_duplicates(df):
    """Remove duplicate entries from the dataset."""
    dup_mask = df.duplicated()
    dup_count = dup_mask.sum()
    print("Exact duplicate rows:", dup_count)
    if dup_count:
        print("First few duplicate rows:")
        print(df[dup_mask].head())
    
    print("Original shape:", df.shape)
    df_clean = df.drop_duplicates().reset_index(drop=True)
    print("New shape after dropping duplicates:", df_clean.shape)
    return df_clean

def handle_missing_values(df_clean):
    """Handle missing values in the dataset."""
    missing_counts = df_clean.isnull().sum().sort_values(ascending=False)
    print("Missing values per column: ", missing_counts)
    
    # Numeric median imputation
    num_cols = df_clean.select_dtypes(include=[np.number]).columns
    for col in num_cols:
        median_val = df_clean[col].median()
        df_clean[col] = df_clean[col].fillna(median_val)
    
    # Categorical mode imputation
    cat_cols = df_clean.select_dtypes(include=['object']).columns
    for col in cat_cols:
        if df_clean[col].mode().size > 0:
            mode_val = df_clean[col].mode().iloc[0]
            df_clean[col] = df_clean[col].fillna(mode_val)
        else:
            df_clean[col] = df_clean[col].fillna("Unknown")
    
    final_missing_counts = df_clean.isnull().sum().sort_values(ascending=False)
    print("Missing values after imputation: ", final_missing_counts)
    return df_clean, cat_cols

def handle_inconsistent_entries(df_clean, cat_cols):
    """Handle inconsistent entries in categorical columns."""
    for col in cat_cols:
        unique_vals = df_clean[col].dropna().astype(str).unique()
        print(f"\nColumn: {col} - Unique Values Count: {len(unique_vals)}")
        print(col, "->", unique_vals[:])
    
    # Create Mapping dictionary for inconsistent entries
    mapping = {
        'Mail Check': 'Mailed Check',
        'Mailed Check': 'Mailed Check',
        'Mail_Check': 'Mailed Check',
        'MailedCheck': 'Mailed Check',
        'Direct_Deposit': 'Direct Deposit',
        'DirectDeposit': 'Direct Deposit',
        'Direct Deposit': 'Direct Deposit',
    }
    
    if 'PaycheckMethod' in df_clean.columns:
        df_clean['PaycheckMethod'] = df_clean['PaycheckMethod'].replace(mapping)
    
    # Generic normalization
    df_clean[cat_cols] = df_clean[cat_cols].apply(lambda col: col.str.title())
    return df_clean

def clean_currency_formatting(df_clean):
    """Clean currency formatting in numeric columns."""
    hourly_cols = [c for c in df_clean.columns if c.strip() == 'HourlyRate']
    
    if not hourly_cols:
        print("No HourlyRate column found.")
    else:
        for col in hourly_cols:
            backup_col = f"{col}_orig"
            if backup_col not in df_clean.columns:
                df_clean[backup_col] = df_clean[col].astype(str)
            
            cleaned = df_clean[col].astype(str).str.replace(r'[\$,]', '', regex=True).str.strip()
            df_clean[col] = pd.to_numeric(cleaned.replace('', np.nan), errors='coerce')
            
            n_coerced = df_clean[col].isna().sum()
            print(f"Column '{col}': {n_coerced} non-numeric/missing after stripping currency (of {len(df_clean)})")
            
            if n_coerced:
                med = df_clean[col].median()
                df_clean[col] = df_clean[col].fillna(med)
                print(f"Imputed {n_coerced} values in '{col}' with median = {med:.2f}")
            
            print(f"'{col}' dtype after cleaning:", df_clean[col].dtype)
    return df_clean

def handle_outliers(df_clean):
    """Detect and handle outliers using IQR method."""
    numeric_cols = df_clean.select_dtypes(include=[np.number]).columns.tolist()
    summary = []
    
    for col in numeric_cols:
        s = df_clean[col].dropna()
        q1 = s.quantile(0.25)
        q3 = s.quantile(0.75)
        iqr = q3 - q1
        lower = q1 - 1.5 * iqr
        upper = q3 + 1.5 * iqr
        
        out_mask = (df_clean[col] < lower) | (df_clean[col] > upper)
        n_out = int(out_mask.sum())
        pct_out = n_out / len(df_clean) * 100
        
        summary.append({
            "variable": col,
            "n_outliers": n_out,
            "pct_outliers": pct_out,
            "lower_bound": lower,
            "upper_bound": upper,
            "iqr": iqr
        })
        
        if n_out:
            print(f"{col}: {n_out} outliers ({pct_out:.2f}%) — LB={lower:.2f}, UB={upper:.2f}")
        else:
            print(f"{col}: 0 outliers")
    
    outlier_summary = pd.DataFrame(summary).set_index("variable")
    print("\nOutlier Summary:")
    print(outlier_summary)
    
    # Handle outliers by capping them at the IQR bounds
    for col in numeric_cols:
        lower = outlier_summary.loc[col, "lower_bound"]
        upper = outlier_summary.loc[col, "upper_bound"]
        df_clean[col] = np.where(df_clean[col] < lower, lower,
                                np.where(df_clean[col] > upper, upper, df_clean[col]))
    return df_clean

def validate_annual_salary(df_clean):
    """Validate and recalculate annual salary if needed."""
    if all(col in df_clean.columns for col in ['Hourly Rate', 'Hours Weekly', 'Annual Salary']):
        computed = df_clean['Hourly Rate'] * df_clean['Hours Weekly'] * 52
        diff = (df_clean['Annual Salary'] - computed).abs()
        mask = diff > (0.01 * computed)
        df_clean.loc[mask, 'Annual Salary'] = computed[mask]
        print("Recomputed Annual Salary for", mask.sum(), "records.")
    return df_clean

def final_checks_and_save(df_clean, output_path):
    """Perform final checks and save the cleaned dataset."""
    print("Final shape:", df_clean.shape, "\n")
    print("Missing counts (final):")
    print(df_clean.isnull().sum())
    print("\nDtypes:")
    print(df_clean.dtypes)
    print("\nSample cleaned rows:")
    print(df_clean.head(5))
    
    # Save cleaned file
    df_clean.to_csv(output_path, index=False)
    print(f"\nSaved cleaned dataset to {output_path}")

def main():
    # Setup
    setup_environment()
    
    # Define paths
    input_path = "Employee Turnover Dataset.csv"
    output_path = "Employee_Turnover_Cleaned.csv"
    
    # Load data
    df = load_data(input_path)
    
    # Profile variables
    profile_variables(df)
    
    # Inspect data
    inspect_data(df)
    
    # Clean data
    df_clean = handle_duplicates(df)
    df_clean, cat_cols = handle_missing_values(df_clean)
    df_clean = handle_inconsistent_entries(df_clean, cat_cols)
    df_clean = clean_currency_formatting(df_clean)
    df_clean = handle_outliers(df_clean)
    df_clean = validate_annual_salary(df_clean)
    
    # Final checks and save
    final_checks_and_save(df_clean, output_path)

if __name__ == "__main__":
    main()