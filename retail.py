import pandas as pd

df = pd.read_csv("./data/online_retail_II.csv")


# print('\n-----Head-----')
# print(df.head())
# print('\n-----Info-----')
# print(df.info())
# print('\n-----Desc-----')
# print(df.describe())
# print('\n-----Shape-----')
# print(df.shape)
# print('\n-----Columns-----')
# print(df.columns)
# print('\n-----Dtypes-----')
# print(df.dtypes)

# print('\n-----isnull-----')
# print(df.isnull().sum())
# print('\n-----duplicated-----')
# print(df.duplicated().sum())
# print('\n-----Quantity <0-----')
# print(df[df['Quantity'] < 0])
# print('\n-----Price <0-----')
# print(df[df['Price'] <= 0])


def strutureAndQuality(df):
    """
    EDA: Explore data
    """
    ## 1. Data Structure
    print('===EDA'+'='*50)
    print('\n[1] Basic Info')
    print(f'Rows count: {df.shape[0]:,}  Columns count: {df.shape[1]}')

    ## 2. Data Quality
    print('\n[2] Missing Values')
    missing_count = df.isnull().sum()
    missing_percent = (missing_count / len(df) * 100).round(2)
    missing_df = pd.DataFrame({'Missing Count': missing_count, 'Percentage(%)': missing_percent})
    # missing_df = missing_df[missing_df['Missing Count']>0].sort_values(by='Missing Count', ascending=False)
    missing_df = missing_df.sort_values(by='Missing Count', ascending=False)
    if not missing_df.empty:
        print(missing_df)
    else:
        print('No missing value.')

    ## 3. Duplicates
    print('\n[3] Duplicates check')
    dup_count = df.duplicated().sum()
    dup_percent = (dup_count / len(df) * 100)
    print(f'Duplicate count: {dup_count:,} ({dup_percent:.2f}%)')

    ## 4. Anomalies
    print('\n[4] Business Anomalies')

    # Quantity
    print(f' ▶ Negative Quantity count (return or cancel): {len(df[df['Quantity'] < 0])}')
    print(f' ▶ 0 Quantity count: {len(df[df['Quantity'] == 0])}')

    # Price
    print(f' ▶ Negative Price count (return or cancel): {len(df[df['Price'] < 0])}')
    print(f' ▶ 0 Price count: {len(df[df['Price'] == 0])}')

    # Invoice
    invoice_cancel = len(df[df['Invoice'].astype(str).str.startswith('C', na=False)])
    print(f' ▶ Invoice starts with C count(canceled order):{invoice_cancel:,}')

    ## 5. Consistency 類別一致性檢查
    print('\n[5] Consistency')
    country_list = df['Country'].drop_duplicates().sort_values().to_list()
    # country_list = sorted(df['Country'].unique())
    # print(f'Country list: {country_list}')

    country_count = len(country_list)
    # country_count = df['Country'].nunique()
    print(f'Country count: {country_count}')    

    print('\n\n===Result'+'='*50)
    print('1. Change missing Customer ID as "Guest"')
    print('2. Remove duplicates.')
    print('3. Take negative or zero Quantity and Price away, or maybe do a seperate analysis.')

    # 6. Data Distribution
    print('\n[6] Distribution')
    top_product = df.groupby(['Description', 'StockCode'])['Quantity'].sum().reset_index().sort_values(by='Quantity', ascending=False).head(10)
    print('Top sale product(multiply Qty):')
    print(top_product)
    
    top_freq = df['StockCode'].value_counts().head(10)
    print(f'\nTop frequent product(by Stock code):\n {top_freq}')
# ===========================================
# Find: Description and StockCode don't match
# 3465     PACK OF 72 RETROSPOT CAKE CASES     21212     49344
# 3464    PACK OF 72 RETRO SPOT CAKE CASES     21212     46106
# *** INSIGHT: Inconsistent product descriptions were identified for the same StockCode, which could lead to inaccurate product-level analysis if not standardised.
# ===========================================




def standardise_desc(df):
    """
    Product Description Check, Master data quality issue.

    Issue: Same StockCode is linked to multiple descriptions, e.g. "RETROSPOT" vs "RETRO SPOT"
    Solution: Standardise description using most frequent value per StockCode   

    Args:
        df: The raw retail dataframe.

    Returns:
        df_clean (pd.DataFrame)
    """

    df_clean = df.copy()

    # Uppercase, remove space
    df_clean['Description'] = (df_clean['Description']
                               .astype(str)
                               .str.strip()
                               .str.upper()
                               .str.replace(r'\s+', ' ', regex=True))

    # Calculate StockCode+Description occur. Sort by counts, only remain the most frequent
    desc_counts = df_clean.groupby(['StockCode', 'Description']).size().reset_index(name='Count')
    desc_counts = desc_counts.sort_values(['StockCode', 'Count'], ascending=[True, False])
    desc_counts = desc_counts.drop_duplicates(subset=['StockCode'], keep='first')
    
    # Build a map, mapping back to the df
    desc_mapping = dict(zip(desc_counts['StockCode'], desc_counts['Description']))
    df_clean['Description'] = df_clean['StockCode'].map(desc_mapping)

    print(f'\n Descriptions counts(Master Descriptions): {len(desc_counts)}')
    print('Top 15 most frequent descriptions:')
    print(desc_counts.sort_values(by='Count', ascending=False).head(15))

    return df_clean



df_clean = standardise_desc(df)
# strutureAndQuality(df)
