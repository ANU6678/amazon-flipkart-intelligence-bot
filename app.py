import streamlit as st
import pandas as pd
import numpy as np
import re
import plotly.express as px

st.set_page_config(page_title="Amazon & Flipkart Executive Intelligence Bot", page_icon="💼", layout="wide")

st.markdown("""
<style>
    .metric-card {
        background: #1e222d; border-radius: 10px; padding: 14px 18px; border: 1px solid #2d3748;
        box-shadow: 0 4px 6px -1px rgba(0,0,0,0.25);
        transition: transform 0.2s ease, box-shadow 0.2s ease, border-color 0.2s ease;
    }
    .metric-card:hover { transform: translateY(-3px); box-shadow: 0 8px 20px -2px rgba(56, 189, 248, 0.35); border-color: #38bdf8; }
    .metric-title { font-size: 0.8rem; color: #94a3b8; margin-bottom: 2px; font-weight: 500; text-transform: uppercase; }
    .metric-value { font-size: 1.5rem; font-weight: 700; color: #38bdf8; line-height: 1.2; }
    .metric-subtext { font-size: 0.75rem; color: #64748b; margin-top: 4px; }
    .summary-box { background: #0f172a; border-left: 4px solid #38bdf8; padding: 12px 18px; border-radius: 6px; margin: 16px 0; color: #f1f5f9; font-size: 0.95rem; }
    div.stButton > button { transition: transform 0.15s ease, box-shadow 0.15s ease, border-color 0.15s ease; border-radius: 8px; font-weight: 500; }
    div.stButton > button:hover { transform: translateY(-2px); box-shadow: 0 4px 12px rgba(56, 189, 248, 0.3); border-color: #38bdf8; }
    .custom-table-container { overflow-x: auto; border-radius: 8px; border: 1px solid #334155; margin-top: 10px; }
    .custom-table { width: 100%; border-collapse: collapse; font-size: 0.85rem; background-color: #0f172a; color: #e2e8f0; }
    .custom-table th { background-color: #1e293b; padding: 10px 12px; text-align: left; font-weight: 600; color: #94a3b8; border-bottom: 2px solid #334155; }
    .custom-table td { padding: 10px 12px; border-bottom: 1px solid #1e293b; vertical-align: middle; }
    .custom-table tr:hover { background-color: #1e293b55; }
</style>
""", unsafe_allow_html=True)

BRAND_COLORS = {
    "American Tourister": "#003366",
    "Safari": "#D32F2F",
    "VIP": "#1976D2",
    "Mokobara": "#7B1FA2",
    "Aristocrat": "#00796B",
    "Skybags": "#F57C00",
    "HRX": "#616161",
    "Wildcraft": "#388E3C"
}

def render_brand_badge(brand_name):
    b_str = str(brand_name).strip() if pd.notna(brand_name) else "Other"
    color = BRAND_COLORS.get(b_str, "#9E9E9E")
    label = b_str if b_str in BRAND_COLORS else f"{b_str} (Other)"
    return f'<span style="background-color: {color}; color: #ffffff; padding: 3px 8px; border-radius: 12px; font-size: 11px; font-weight: 600; display: inline-block;">{label}</span>'

def render_ad_badge(ad_type):
    ad_str = str(ad_type).lower() if pd.notna(ad_type) else "organic"
    if "sponsor" in ad_str:
        return '<span style="background-color: #F57C00; color: #ffffff; padding: 2px 7px; border-radius: 10px; font-size: 10px; font-weight: 700;">Sponsored</span>'
    return '<span style="background-color: #475569; color: #cbd5e1; padding: 2px 7px; border-radius: 10px; font-size: 10px;">Organic</span>'

@st.cache_data
def load_all_datasets():
    """Loads all 3 Excel files using relative paths with clean error handling."""
    try:
        amz = pd.read_excel('amazon_bag_keywords_first_page_20260701_204309.xlsx', sheet_name='Raw_Data')
        flp = pd.read_excel('flipkart_trolley_keywords_first_page_20260701_190125.xlsx', sheet_name='Raw_Data')
        cmp = pd.read_excel('All_Campaigns_May_Jun_Jul_Analysis_20260814_111955.xlsx', sheet_name='ASIN Analysis - AdvProd Master')
    except Exception as e:
        st.error(f"Error loading Excel data files: {e}")
        return None, None, None

    amz['num_price'] = pd.to_numeric(amz['price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce')
    flp['num_price'] = pd.to_numeric(flp['price'].astype(str).str.replace(r'[^\d.]', '', regex=True), errors='coerce')
    return amz, flp, cmp

amazon_df, flipkart_df, campaigns_df = load_all_datasets()
if amazon_df is None or flipkart_df is None or campaigns_df is None:
    st.stop()

all_detected_brands = set(amazon_df['brand_inferred'].dropna()) | set(flipkart_df['brand_inferred'].dropna())
last_scraped_amz = amazon_df['scraped_at'].dropna().max()
last_scraped_flp = flipkart_df['scraped_at'].dropna().max()
primary_keyword = amazon_df['keyword'].value_counts().index[0]
amazon_keywords = amazon_df['keyword'].dropna().unique().tolist()

with st.sidebar:
    st.title("💼 Executive BI Bot")
    st.markdown("**American Tourister Intelligence**")
    st.markdown("---")
    st.write(f"🏷️ **Tracked Competitors:** {len(BRAND_COLORS)}")
    st.write(f"🔍 **Detected Brands:** {len(all_detected_brands):,}")
    st.write(f"📅 **Latest Scrape:** {str(last_scraped_amz)[:10]}")
    st.write(f"📦 **Amazon Records:** {len(amazon_df):,}")
    st.write(f"🛒 **Flipkart Records:** {len(flipkart_df):,}")
    st.write(f"📊 **Campaign Records:** {len(campaigns_df):,}")
    st.markdown("---")
    st.caption("Tracked: " + ", ".join(BRAND_COLORS.keys()))

st.title("Amazon & Flipkart Executive Intelligence Bot")
st.caption("Competitor & Marketplace Performance Intelligence for American Tourister Leadership")

k1, k2, k3, k4, k5 = st.columns(5)
with k1:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Tracked Brands</div><div class="metric-value">{len(BRAND_COLORS)}</div><div class="metric-subtext">8 Key Competitors</div></div>', unsafe_allow_html=True)
with k2:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Amazon Records</div><div class="metric-value">{len(amazon_df):,}</div><div class="metric-subtext">Last sync: {str(last_scraped_amz)[:10]}</div></div>', unsafe_allow_html=True)
with k3:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Flipkart Records</div><div class="metric-value">{len(flipkart_df):,}</div><div class="metric-subtext">Last sync: {str(last_scraped_flp)[:10]}</div></div>', unsafe_allow_html=True)
with k4:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Campaign Lines</div><div class="metric-value">{campaigns_df["Line"].nunique():,}</div><div class="metric-subtext">Across {campaigns_df["Brand"].nunique()} brands</div></div>', unsafe_allow_html=True)
with k5:
    st.markdown(f'<div class="metric-card"><div class="metric-title">Advertised ASINs</div><div class="metric-value">{campaigns_df["Advertised ASIN"].nunique():,}</div><div class="metric-subtext">May – Jul 2026</div></div>', unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)

amz_p1 = amazon_df[amazon_df['page'] == 1]
brand_counts = amz_p1['brand_inferred'].value_counts().reset_index()
brand_counts.columns = ['Brand', 'Page 1 Appearances']
top_brand_data = brand_counts[brand_counts['Brand'].isin(list(BRAND_COLORS.keys()))].head(8)

fig_overview = px.bar(
    top_brand_data,
    x='Brand',
    y='Page 1 Appearances',
    color='Brand',
    color_discrete_map=BRAND_COLORS,
    title="Amazon Page 1 Share of Voice: American Tourister vs Competitors",
    template="plotly_dark"
)
fig_overview.update_layout(
    margin=dict(l=20, r=20, t=40, b=20),
    height=280,
    showlegend=False,
    xaxis_title="",
    yaxis=dict(title="Page 1 Listings", rangemode="tozero")
)
st.plotly_chart(fig_overview, use_container_width=True)

st.subheader("⚡ Quick Intelligence Presets")
b1, b2, b3, b4 = st.columns(4)

active_query = None
if b1.button("🥇 Top 5 Ranked Bags on Amazon", use_container_width=True): active_query = "preset_top5_amazon"
if b2.button("🏷️ Safari Price Undercuts (< ₹1,500)", use_container_width=True): active_query = "preset_safari_undercut"
if b3.button("📈 Top Campaign Lines by RoAS", use_container_width=True): active_query = "preset_campaign_roas"
if b4.button("⚔️ Competitor Share of Voice Breakdown", use_container_width=True): active_query = "preset_brand_distribution"

user_text = st.text_input(
    "🔍 Ask a business question:",
    placeholder="e.g., 'top 5 school bags', 'Safari bags under 1500', 'Mokobara trolley', 'campaign roas'",
    key="search_box"
)
if user_text: active_query = user_text

def deduplicate_table(df):
    """Groups rows by title, keeps best rank, and counts locations found."""
    if df is None or df.empty:
        return df
    loc_col = 'pincode' if 'pincode' in df.columns else df.columns[0]
    grouped = df.groupby('title', as_index=False).agg({
        'rank': 'min',
        'brand_inferred': 'first',
        'price': 'first',
        'rating': 'first',
        'ad_type': 'first',
        'keyword': 'first',
        loc_col: 'count'
    }).rename(columns={loc_col: 'Locations Found'})
    return grouped.sort_values('rank', ascending=True)

def detect_target_keyword(query_text, available_kws, default_kw):
    q = query_text.lower().strip()
    candidate_kws = [k for k in available_kws if k != 'bag'] if q != 'bag' else available_kws
    tokens = ['school', 'trolley', 'laptop', 'backpack', 'college']
    matched = next((k for k in sorted(candidate_kws, key=len, reverse=True) if k.lower() in q or any(t in q and t in k.lower() for t in tokens)), None)
    return (matched, True) if matched else (default_kw, False)

def process_query(query):
    if not query: return None, None, None
    q_lower = query.lower().strip()

    if query == "preset_top5_amazon":
        res = amazon_df[amazon_df['keyword'] == primary_keyword]
        disp = deduplicate_table(res).head(5)
        return f"Showing top 5 unique products for '{primary_keyword}' — the most tracked keyword.", disp, None

    if query == "preset_safari_undercut":
        res = flipkart_df[(flipkart_df['brand_inferred'].str.lower() == 'safari') & (flipkart_df['num_price'] < 1500)]
        disp = deduplicate_table(res)
        return f"Found {len(disp)} unique Safari trolley models priced under ₹1,500 across Flipkart search locations.", disp, None

    if query == "preset_campaign_roas" or "roas" in q_lower or "campaign" in q_lower:
        spend_col = [c for c in campaigns_df.columns if 'Spend' in c][0]
        sales_col = [c for c in campaigns_df.columns if 'Sales' in c][0]
        orders_col = [c for c in campaigns_df.columns if 'Orders' in c][0]
        
        grp = campaigns_df.groupby('Line').agg({spend_col: 'sum', sales_col: 'sum', orders_col: 'sum'}).reset_index()
        grp.rename(columns={spend_col: 'Total Spend (₹)', sales_col: 'Total Sales (₹)', orders_col: 'Total Orders'}, inplace=True)
        grp['RoAS'] = (grp['Total Sales (₹)'] / grp['Total Spend (₹)'].replace(0, np.nan)).round(2)
        top_lines = grp.dropna(subset=['RoAS']).sort_values('RoAS', ascending=False).head(10)
        
        fig = px.bar(top_lines, x='Line', y='RoAS', color='Total Sales (₹)', title="Top 10 Campaign Lines by RoAS", template="plotly_dark")
        fig.update_layout(yaxis=dict(rangemode="tozero", title="RoAS"))
        return "Aggregated campaign performance across product lines sorted by RoAS.", top_lines, fig

    if query == "preset_brand_distribution" or "competitor" in q_lower or "vs" in q_lower:
        return "Share of Voice comparison on Amazon Page 1 for major tracked brands.", top_brand_data, fig_overview

    top_match = re.search(r'top\s+(\d+)', q_lower)
    limit = int(top_match.group(1)) if top_match else 10
    price_match = re.search(r'(?:under|below|<)\s*(?:rs\.?|inr|₹)?\s*(\d+)', q_lower)
    price_val = float(price_match.group(1)) if price_match else None
    matched_brand = next((b for b in BRAND_COLORS.keys() if b.lower() in q_lower), None)
    target_kw, is_specific_kw = detect_target_keyword(query, amazon_keywords, primary_keyword)

    filtered = amazon_df[amazon_df['keyword'] == target_kw].copy()
    insight_desc = [f"keyword '{target_kw}'"] if is_specific_kw else [f"'{target_kw}' (most tracked keyword)"]
    if matched_brand:
        filtered = filtered[filtered['brand_inferred'].str.lower() == matched_brand.lower()]
        insight_desc.append(f"brand '{matched_brand}'")
    if price_val:
        filtered = filtered[filtered['num_price'] <= price_val]
        insight_desc.append(f"price under ₹{int(price_val):,}")

    if not filtered.empty or matched_brand or price_val or top_match or is_specific_kw:
        deduped = deduplicate_table(filtered).head(limit)
        return f"Showing top {len(deduped)} unique products for " + ", ".join(insight_desc) + ".", deduped, None

    return "I couldn't understand that — try a preset button or ask about a brand, price range ('under 1500'), or 'campaign roas'.", None, None

if active_query:
    summary_text, results_df, chart_fig = process_query(active_query)

    if summary_text:
        st.markdown(f'<div class="summary-box">💡 <b>Executive Insight:</b> {summary_text}</div>', unsafe_allow_html=True)
    if chart_fig and active_query != "preset_brand_distribution":
        st.plotly_chart(chart_fig, use_container_width=True)

    if results_df is not None and not results_df.empty:
        st.markdown("### 📋 Verified Filtered Records")
        if 'brand_inferred' in results_df.columns and 'ad_type' in results_df.columns:
            rows_html = [
                f"<tr><td><b>#{r.get('rank', '-')}</b></td>"
                f"<td>{render_brand_badge(r.get('brand_inferred', ''))}</td>"
                f"<td>{str(r.get('title', '-'))[:75]}...</td>"
                f"<td><b>{r.get('price', '-')}</b></td>"
                f"<td>{r.get('rating', '-')}</td>"
                f"<td>{render_ad_badge(r.get('ad_type', ''))}</td>"
                f"<td><span style='color:#38bdf8; font-weight:600;'>{r.get('Locations Found', 1)}</span></td>"
                f"<td><span style='color:#64748b; font-size:11px;'>{r.get('keyword', '-')}</span></td></tr>"
                for _, r in results_df.iterrows()
            ]
            table_html = f"""
            <div class="custom-table-container">
                <table class="custom-table">
                    <thead><tr><th>Best Rank</th><th>Brand</th><th>Product Title</th><th>Price</th><th>Rating</th><th>Listing Type</th><th>Locations Found</th><th>Search Keyword</th></tr></thead>
                    <tbody>{"".join(rows_html)}</tbody>
                </table>
            </div>
            """
            st.markdown(table_html, unsafe_allow_html=True)
        else:
            st.dataframe(results_df, use_container_width=True, hide_index=True)
