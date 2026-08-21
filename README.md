# Amazon & Flipkart Executive Intelligence Bot

An executive business intelligence dashboard and conversational chatbot built with Python and Streamlit for American Tourister leadership. It aggregates and cross-analyzes scraped search results across Amazon and Flipkart against 8 core competitor brands (American Tourister, Safari, VIP, Mokobara, Aristocrat, Skybags, HRX, and Wildcraft) alongside internal advertising campaign performance data to provide real-time Share of Voice metrics, pricing undercut alerts, and Return on Ad Spend (RoAS) analytics.

## Setup & Running

1. **Install dependencies**:
   ```bash
   pip install -r requirements.txt
   ```

2. **Launch the application**:
   ```bash
   streamlit run app.py
   ```

> **Note on Data Files**: The raw Excel datasets (`*.xlsx`) contain confidential competitor intelligence and are excluded from version control via `.gitignore`. To run the dashboard, ensure the required `.xlsx` files (`amazon_bag_keywords_*.xlsx`, `flipkart_trolley_keywords_*.xlsx`, and `All_Campaigns_*.xlsx`) are placed directly in the project root folder.
