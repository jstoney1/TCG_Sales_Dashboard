# 📊 TCG Sales Dashboard

This ongoing project analyzes and visualizes my personal trading card game (TCG) sales data to identify trends and optimize strategies for my hobby business. It’s also a portfolio piece showcasing my data skills for entry-level job applications—turning my TCG passion into Python-powered insights!

## 🚀 Overview
- **What It Does:** Tracks sales, costs, and profits from my TCGplayer store, with visuals in progress.
- **Tools:** Python, Pandas, Requests
- **Skills:** Data merging, profit analysis, API integration
- **Period:** October 2022 - February 2025 (partial data)
- **Data Sources:**
  - [Sales Report](https://raw.githubusercontent.com/jstoney1/TCG_Sales_Dashboard/refs/heads/main/data/ProfessorSteg%20Sales%20Report%20-%20ProfessorSteg%20Sales%20Report.csv) (367 transactions)
  - [Order Data](https://raw.githubusercontent.com/jstoney1/TCG_Sales_Dashboard/refs/heads/main/data/TCGPlayer%20Card%20Business%20Spreadsheet%20-%20Order%20Data.csv) (1,466 orders)
  - [Single Card Data](https://raw.githubusercontent.com/jstoney1/TCG_Sales_Dashboard/refs/heads/main/data/TCGPlayer%20Card%20Business%20Spreadsheet%20-%20Single%20Card%20Data.csv) (1,108 cards)
  - [Sales by Set](https://raw.githubusercontent.com/jstoney1/TCG_Sales_Dashboard/refs/heads/main/data/TCGPlayer%20Card%20Business%20Spreadsheet%20-%20Sales%20Data%20by%20Set.csv) (255 sets)
  - [Sales by Card](https://raw.githubusercontent.com/jstoney1/TCG_Sales_Dashboard/refs/heads/main/data/TCGPlayer%20Card%20Business%20Spreadsheet%20-%20Sales%20Data%20by%20Card.csv) (1,108 cards)
  - [Business Expenses](https://raw.githubusercontent.com/jstoney1/TCG_Sales_Dashboard/refs/heads/main/data/TCGPlayer%20Card%20Business%20Spreadsheet%20-%20Business%20Expenses.csv) (14 expenses)

## 📈 Key Findings
Here’s where my data’s at (run `analyze_sales.py` for latest):
- **Total Units Sold:** 1064
- **Gross Sales:** $1804.84
- **Net Revenue:** $1343.98
- **Total Fees:** $385.56
- **Total Cost:** $424.99
- **Total Profit (before expenses):** $918.99
- **Total Expenses:** $513.75
- **Net Profit:** $405.24
- **Overall Profit Margin:** 23.43%

### 🏆 Top 5 Sales with Profit
| Product Name             | Net Revenue | Cost Basis | Profit  | Profit Margin | Date       | Game    |
|--------------------------|-------------|------------|---------|---------------|------------|---------|
| Blue-Eyes White Dragon   | $51.05      | $0.25      | $50.55  | 85.72%        | 11/01/22   | YuGiOh  |
| Ragavan, Nimble Pilferer | $44.87      | $30.00     | $14.87  | 28.18%        | 05/03/23   | Magic   |
| ______'s Chansey         | $37.35      | $0.25      | $37.10  | 84.34%        | 10/27/24   | Pokémon |
| Victreebel (14)          | $37.34      | $0.25      | $37.09  | 84.33%        | 02/14/23   | Pokémon |
| Sliver Overlord          | $29.29      | $0.25      | $29.04  | 85.46%        | 10/27/22   | Magic   |

## 🛠 Installation
1. Clone the repo:  
   ```bash
   git clone https://github.com/jstoney1/TCG_Sales_Dashboard.git
2. Install Dependencies
   pip install pandas requests
3. Run the Analysis
   python src/analyze_sales.py
Note: Outputs stats and saves Magic card images to images/. Streamlit dashboard coming soon!

🎮 Planned Features
  📈 Sales trends over time (e.g., monthly breakdowns)
  🏆 Best-selling products analysis (beyond top 5)
  🎮 Revenue breakdown by game (Magic, Yu-Gi-Oh!, Pokémon)
  📊 Interactive charts via Streamlit or web app
  📊 Example Visualizations
Coming Soon: Profit by product line, top sets bar chart.

📝 Notes
Data Gaps: Some orders missing; cost basis of bulk acquired cards set to $0.25 with Single Card Data.
Progress: Building toward a fully visual dashboard with card pics!

🚀 Next Steps
Add Yu-Gi-Oh! and Pokémon card images (beyond Magic).
Build an interactive web dashboard with Streamlit.
Enhance with time-series charts and customer insights.

📩 Contact
Questions or ideas? Reach out on GitHub!
Last updated: February 2025
