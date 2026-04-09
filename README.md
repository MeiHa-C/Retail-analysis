# Retail-analysis

## Business Problem
Understand customer behaviour and improve retention.

## Dataset
Online Retail Dataset

## Tools
Python


## Data Quality Handling
### Inconsistent Product Descriptions
It was observed that the same product (StockCode) is associated with multiple descriptions due to manual entry or formatting inconsistencies (e.g. spacing, formatting).
To ensure accurate product-level analysis, descriptions were standardised by assigning the most frequent label for each StockCode.


## Analysis Focus
1. When does transaction activity peak? (hourly / weekday patterns)
2. Customer contribution (revenue)
3. Top sales
4. Do customers repeat purchases?


## Key Insights
### 1. Transaction Patterns
Transaction volume peaks in midday between 12–15:00, after 17:00, activity declines. Suggesting reducing engagement in the early morning and evening.
Weekday results are better than weekend, and Friday indicates worse performance than other weekdays.

### 2. Customer Value Analysis
The top 20% of customers contribute nearly two-thirds of total revenue, indicating a strong revenue concentration among high-value customers.


## Business Impact
### 1. Transaction Patterns
The demand patterns have implications across multiple functions:
- Operations: workforce scheduling
- Marketing: campaign timing
- IT: system capacity scaling

### 2. Customer Value Analysis
This suggests that retaining high-value customers should be a priority, as they drive a disproportionate share of revenue. Strategies such as personalised offers or loyalty programmes could help maintain engagement, and customer retention strategies should prioritise this segment.


## Visualisation
1. Transaction Patterns
![alt text](<Images/Customer Transaction Patterns by Hour and Weekday.png>)

2. Customer Value Analysis
Different chart types were evaluated (stacked vs grouped bar charts). A grouped bar chart with customer groups on the x-axis was selected, as it provides a clearer comparison between transaction volume and revenue contribution.
- Stacked Bar Chart
![alt text](<Images/Customer group_stacked chart.png>)

- Grouped Bar Chart
![alt text](<Images/Customer group_grouped chart_Metrics.png>)
✅ Selected ✅ (Customer groups on the x-axis)
![alt text](<Images/Customer group_grouped chart_Customer.png>)

