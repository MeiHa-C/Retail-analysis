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




## Business Impact
### 1. Transaction Patterns
The demand patterns have implications across multiple functions:
- Operations: workforce scheduling
- Marketing: campaign timing
- IT: system capacity scaling


## Visualisation
![alt text](<Images/Customer Transaction Patterns by Hour and Weekday.png>)
![alt text](<Images/Customer group_stacked chart.png>)

