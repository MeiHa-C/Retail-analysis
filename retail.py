import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

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
    print(df.head())
    print(f'Rows count: {df.shape[0]:,}  Columns count: {df.shape[1]}')

    df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])
    print(f'\nThe first transaction: {df['InvoiceDate'].min()}')
    print(f'The first transaction: {df['InvoiceDate'].max()}')

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

    Issue 1: Same StockCode is linked to multiple descriptions, e.g. "RETROSPOT" vs "RETRO SPOT"
    Solution: Standardise description using most frequent value per StockCode   

    Issue 2: Fill missing Customer ID out as 'Guest'

    Args:
        df: The raw retail dataframe.

    Returns:
        df_clean (pd.DataFrame)
    """

    df_clean = df.copy()


    ## Multiple Descriptions
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


    ## Missing Customer ID
    missing_count = df_clean['Customer ID'].isnull().sum()
    missing_percent = df_clean['Customer ID'].isnull().mean()*100 # Null=True=1; NotNull=False=0, then average it
    print(f'Missing ID count: {missing_count} ({missing_percent:.2f} %)')
    
    # Fill up the empty customer ID as 'Guest'
    df_clean['Customer ID'] = df_clean['Customer ID'].fillna('Guest')
    

    return df_clean




def create_features(df_clean):
    """
    Create some new features for analysis
    """
    df_clean['Revenue'] = df_clean['Quantity'] * df_clean['Price']


    # Convert datetime and date feature
    df_clean['InvoiceDate'] = pd.to_datetime(df_clean['InvoiceDate'])
    df_clean['Month'] = df_clean['InvoiceDate'].dt.month
    df_clean['Hour'] = df_clean['InvoiceDate'].dt.hour

    # Weekday order for plot
    df_clean['DayName'] = df_clean['InvoiceDate'].dt.day_name()
    weekday_order = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
    df_clean['DayName'] = pd.Categorical(df_clean['DayName'], categories=weekday_order)

    print(f'\nNew features:\n {df_clean.head()}')

    return df_clean


def transaction_analysis(df_clean):
    
    # 1. Monthly order amount
    plt.figure(figsize=(12,6))
    sales_monthly = df_clean.groupby('Month').size()
    # sns.barplot(x=sales_monthly.index, y=sales_monthly.values)
    plt.bar(sales_monthly.index, sales_monthly.values, color='tab:olive', width = 0.5, zorder=2)
    plt.xticks(sales_monthly.index)
    plt.grid(axis='y', linestyle='--', zorder=0)
    # plt.bar_label()
    plt.title('Trading volume by Month')
    plt.xlabel('Month')
    plt.ylabel('Number of transactions')
    plt.show()

    # 2. Weekly order amount
    plt.figure(figsize=(12,6))
    sales_weekly = df_clean.groupby('DayName').size()
    plt.bar(sales_weekly.index, sales_weekly.values, color='tab:green', width = 0.5, zorder=2)
    plt.xticks(sales_weekly.index)
    plt.grid(axis='y', linestyle='--', zorder=0)
    plt.title('Trading volume by Day')
    plt.xlabel('Day')
    plt.ylabel('Number of transactions')
    plt.show()

    # 3. Hourly order amount
    plt.figure(figsize=(12,6))
    sales_hour = df_clean.groupby('Hour').size()
    plt.bar(sales_hour.index, sales_hour.values, color='tab:cyan', width = 0.5, zorder=2)
    plt.xticks(sales_hour.index)
    plt.grid(axis='y', linestyle='--', zorder=0)
    plt.title('Trading volume by per Hour')
    plt.xlabel('Hours')
    plt.ylabel('Number of transactions')
    plt.show()

    # 4. Order amount by hour across weekdays
    plt.figure(figsize=(12,6))

    # Index: Hour, Columns = Weekday
    sales_hour_weekday = df_clean.groupby(['Hour', 'DayName']).size().unstack()

    # Dilute the color of weekend
    color_map = {
        'Saturday': 'khaki',
        'Sunday': 'lightgreen'
    }
    for day in sales_hour_weekday.columns:
        if day in ['Saturday', 'Sunday']:
            plt.plot(sales_hour_weekday.index, sales_hour_weekday[day], marker='o', label=day, color=color_map[day], linestyle='--', linewidth=1)
        else:
            plt.plot(sales_hour_weekday.index, sales_hour_weekday[day], marker='o', label=day, linewidth=2)

    plt.xticks(sales_hour_weekday.index)
    plt.grid(linestyle=':', zorder=0)
    plt.title('Customer Transaction Patterns by Hour and Weekday')
    plt.xlabel('Hours')
    plt.ylabel('Transaction Volume')
    plt.legend(title='Weekday')

    # Check the abnormal data
    sat_count = len(df_clean[df_clean['DayName'] == 'Saturday'])
    sat_percent = sat_count/len(df_clean)*100
    print(f'Saturday transaction count: {sat_count} ({sat_percent:.2f}%)')
    # Annotation
    anno_text = f'**Note: Saturday accounts for only {sat_percent:.2f}% of all transactions. \n May indicate store closure or system data loss.'
    plt.text(x=0.3, y=0.02, s=anno_text, transform=plt.gcf().transFigure)

    plt.tight_layout() 
    plt.subplots_adjust(bottom=0.18)
    plt.show()


strutureAndQuality(df)
df_clean = standardise_desc(df)
df_clean = create_features(df_clean)
transaction_analysis(df_clean)