import streamlit as st
import pandas as pd
import os
import time
from google import genai
from google.genai import types

# ---------------------------------------------------------
# PAGE SETUP
# ---------------------------------------------------------

st.set_page_config(
    page_title="AI Data Analyst Assistant",
    page_icon="📊",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ---------------------------------------------------------
# CUSTOM UI
# ---------------------------------------------------------

st.markdown(
    """
    <style>

    .main-title {
        font-size: 2.2rem;
        font-weight: 700;
        margin-bottom: 0.2rem;
    }

    .subtitle {
        color: #666;
        font-size: 1rem;
        margin-bottom: 1.5rem;
    }

    .section-title {
        font-size: 1.35rem;
        font-weight: 650;
        margin-top: 1rem;
        margin-bottom: 0.8rem;
    }

    </style>
    """,
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# GEMINI SETUP
# ---------------------------------------------------------

api_key = os.getenv("GEMINI_API_KEY")

if not api_key:
    st.error("Gemini API key not found.")
    st.stop()

client = genai.Client(api_key=api_key)

PRIMARY_MODEL = "gemini-3.5-flash-lite"
FALLBACK_MODEL = "gemini-3.5-flash"

# ---------------------------------------------------------
# HEADER
# ---------------------------------------------------------

st.markdown(
    '<div class="main-title">📊 AI Data Analyst Assistant</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="subtitle">'
    'Explore your dataset, analyze business performance, '
    'and ask questions using natural language.'
    '</div>',
    unsafe_allow_html=True
)

# ---------------------------------------------------------
# SIDEBAR
# ---------------------------------------------------------

with st.sidebar:

    st.header("📁 Dataset")

    uploaded_file = st.file_uploader(
        "Upload a CSV file",
        type=["csv"]
    )

    st.divider()

    st.markdown("### How it works")

    st.markdown(
        """
        **1. Upload** your CSV dataset

        **2. Explore** key metrics and charts

        **3. Ask** questions in plain English

        **4. Analyze** results using Pandas and Gemini
        """
    )

    st.divider()

    st.caption(
        "Built with Python, Pandas, Streamlit and Gemini API"
    )

# ---------------------------------------------------------
# NO FILE
# ---------------------------------------------------------

if uploaded_file is None:

    st.info(
        "👈 Upload a CSV file from the sidebar to get started."
    )

    st.markdown("### What you can analyze")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("#### 📈 Performance")
        st.write(
            "Analyze sales, profit, margins and overall business performance."
        )

    with col2:
        st.markdown("#### 🔎 Comparisons")
        st.write(
            "Compare products, regions and monthly performance."
        )

    with col3:
        st.markdown("#### 🤖 AI Analysis")
        st.write(
            "Ask natural-language questions and get business insights."
        )

    st.stop()

# ---------------------------------------------------------
# LOAD DATA
# ---------------------------------------------------------

try:

    df = pd.read_csv(uploaded_file)

except Exception as e:

    st.error(
        f"Could not read the CSV file: {e}"
    )

    st.stop()

if "Date" in df.columns:

    df["Date"] = pd.to_datetime(
        df["Date"],
        errors="coerce"
    )

st.success(
    f"Successfully loaded **{len(df):,} rows** and "
    f"**{len(df.columns):,} columns**."
)

# ---------------------------------------------------------
# DATASET INFORMATION
# ---------------------------------------------------------

missing_values = int(
    df.isna().sum().sum()
)

numeric_columns = df.select_dtypes(
    include="number"
).columns

# ---------------------------------------------------------
# KPI CARDS
# ---------------------------------------------------------

if "Sales" in df.columns and "Profit" in df.columns:

    total_sales = df["Sales"].sum()
    total_profit = df["Profit"].sum()

    overall_margin = (
        total_profit / total_sales * 100
        if total_sales != 0
        else 0
    )

    st.markdown(
        '<div class="section-title">Business Overview</div>',
        unsafe_allow_html=True
    )

    col1, col2, col3, col4 = st.columns(4)

    with col1:
        st.metric(
            "Total Sales",
            f"{total_sales:,.0f}"
        )

    with col2:
        st.metric(
            "Total Profit",
            f"{total_profit:,.0f}"
        )

    with col3:
        st.metric(
            "Profit Margin",
            f"{overall_margin:.2f}%"
        )

    with col4:
        st.metric(
            "Transactions",
            f"{len(df):,}"
        )

else:

    col1, col2, col3 = st.columns(3)

    with col1:
        st.metric(
            "Rows",
            f"{len(df):,}"
        )

    with col2:
        st.metric(
            "Columns",
            f"{len(df.columns):,}"
        )

    with col3:
        st.metric(
            "Missing Values",
            f"{missing_values:,}"
        )

# ---------------------------------------------------------
# ANALYSIS DATA
# ---------------------------------------------------------

region_analysis = None
product_analysis = None
monthly_sales = None
monthly_profit = None

# Region
if (
    "Region" in df.columns
    and "Sales" in df.columns
    and "Profit" in df.columns
):

    region_analysis = df.groupby("Region").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )

    if "Units" in df.columns:

        region_analysis["Units"] = (
            df.groupby("Region")["Units"].sum()
        )

    region_analysis["Profit Margin"] = (
        region_analysis["Profit"]
        / region_analysis["Sales"]
        * 100
    )

# Product
if (
    "Product" in df.columns
    and "Sales" in df.columns
    and "Profit" in df.columns
):

    product_analysis = df.groupby("Product").agg(
        Sales=("Sales", "sum"),
        Profit=("Profit", "sum")
    )

    if "Units" in df.columns:

        product_analysis["Units"] = (
            df.groupby("Product")["Units"].sum()
        )

    product_analysis["Profit Margin"] = (
        product_analysis["Profit"]
        / product_analysis["Sales"]
        * 100
    )

# Monthly
if "Date" in df.columns:

    if "Sales" in df.columns:

        monthly_sales = (
            df.groupby(
                df["Date"].dt.to_period("M")
            )["Sales"]
            .sum()
        )

        monthly_sales.index = (
            monthly_sales.index.astype(str)
        )

    if "Profit" in df.columns:

        monthly_profit = (
            df.groupby(
                df["Date"].dt.to_period("M")
            )["Profit"]
            .sum()
        )

        monthly_profit.index = (
            monthly_profit.index.astype(str)
        )

# ---------------------------------------------------------
# TABS
# ---------------------------------------------------------

overview_tab, product_tab, region_tab, trends_tab = st.tabs(
    [
        "📋 Overview",
        "📦 Products",
        "🌎 Regions",
        "📈 Trends"
    ]
)

# ---------------------------------------------------------
# OVERVIEW TAB
# ---------------------------------------------------------

with overview_tab:

    st.markdown(
        '<div class="section-title">Dataset Preview</div>',
        unsafe_allow_html=True
    )

    st.dataframe(
        df.head(10),
        use_container_width=True
    )

    st.markdown(
        '<div class="section-title">Dataset Information</div>',
        unsafe_allow_html=True
    )

    info_col1, info_col2, info_col3 = st.columns(3)

    with info_col1:

        st.metric(
            "Rows",
            f"{len(df):,}"
        )

    with info_col2:

        st.metric(
            "Columns",
            f"{len(df.columns):,}"
        )

    with info_col3:

        st.metric(
            "Missing Values",
            f"{missing_values:,}"
        )

    if len(numeric_columns) > 0:

        st.markdown(
            '<div class="section-title">Basic Statistics</div>',
            unsafe_allow_html=True
        )

        stats_df = (
            df[numeric_columns]
            .describe()
            .transpose()
        )

        st.dataframe(
            stats_df,
            use_container_width=True
        )

# ---------------------------------------------------------
# PRODUCT TAB
# ---------------------------------------------------------

with product_tab:

    if product_analysis is not None:

        st.markdown(
            '<div class="section-title">Product Performance</div>',
            unsafe_allow_html=True
        )

        chart_col, table_col = st.columns(
            [1.1, 1]
        )

        with chart_col:

            st.bar_chart(
                product_analysis["Sales"]
                .sort_values(ascending=False)
            )

        with table_col:

            display_product = (
                product_analysis
                .sort_values(
                    "Sales",
                    ascending=False
                )
                .round(2)
            )

            st.dataframe(
                display_product,
                use_container_width=True
            )

    else:

        st.info(
            "This dataset does not contain the required "
            "Product, Sales and Profit columns."
        )

# ---------------------------------------------------------
# REGION TAB
# ---------------------------------------------------------

with region_tab:

    if region_analysis is not None:

        st.markdown(
            '<div class="section-title">Regional Performance</div>',
            unsafe_allow_html=True
        )

        chart_col, table_col = st.columns(
            [1.1, 1]
        )

        with chart_col:

            st.bar_chart(
                region_analysis["Sales"]
                .sort_values(ascending=False)
            )

        with table_col:

            display_region = (
                region_analysis
                .sort_values(
                    "Sales",
                    ascending=False
                )
                .round(2)
            )

            st.dataframe(
                display_region,
                use_container_width=True
            )

    else:

        st.info(
            "This dataset does not contain the required "
            "Region, Sales and Profit columns."
        )

# ---------------------------------------------------------
# TRENDS TAB
# ---------------------------------------------------------

with trends_tab:

    if monthly_sales is not None:

        st.markdown(
            '<div class="section-title">Monthly Sales</div>',
            unsafe_allow_html=True
        )

        st.line_chart(
            monthly_sales
        )

    if monthly_profit is not None:

        st.markdown(
            '<div class="section-title">Monthly Profit</div>',
            unsafe_allow_html=True
        )

        st.line_chart(
            monthly_profit
        )

    if (
        monthly_sales is None
        and monthly_profit is None
    ):

        st.info(
            "A valid Date column is required to display trends."
        )

# ---------------------------------------------------------
# ANALYTICAL CONTEXT
# ---------------------------------------------------------

analytical_context = ""

if "Sales" in df.columns and "Profit" in df.columns:

    analytical_context += f"""
Overall:
Sales = {df["Sales"].sum():,.0f}
Profit = {df["Profit"].sum():,.0f}
Profit Margin =
{(df["Profit"].sum() / df["Sales"].sum() * 100):.2f}%
"""

if product_analysis is not None:

    analytical_context += f"""

Product Performance:
{product_analysis.round(2).to_string()}
"""

if region_analysis is not None:

    analytical_context += f"""

Region Performance:
{region_analysis.round(2).to_string()}
"""

if monthly_sales is not None:

    analytical_context += f"""

Monthly Sales:
{monthly_sales.round(2).to_string()}
"""

if monthly_profit is not None:

    analytical_context += f"""

Monthly Profit:
{monthly_profit.round(2).to_string()}
"""

# ---------------------------------------------------------
# DIRECT PANDAS ANSWERS
# ---------------------------------------------------------

def direct_answer(question):

    q = question.lower().strip()

    if (
        product_analysis is not None
        and "product" in q
        and "highest" in q
        and "margin" in q
    ):

        product = product_analysis[
            "Profit Margin"
        ].idxmax()

        margin = product_analysis[
            "Profit Margin"
        ].max()

        return (
            f"**{product}** has the highest profit margin "
            f"at **{margin:.2f}%**."
        )

    if (
        product_analysis is not None
        and "product" in q
        and "lowest" in q
        and "margin" in q
    ):

        product = product_analysis[
            "Profit Margin"
        ].idxmin()

        margin = product_analysis[
            "Profit Margin"
        ].min()

        return (
            f"**{product}** has the lowest profit margin "
            f"at **{margin:.2f}%**."
        )

    if (
        product_analysis is not None
        and "product" in q
        and "highest" in q
        and "profit" in q
        and "margin" not in q
    ):

        product = product_analysis[
            "Profit"
        ].idxmax()

        profit = product_analysis[
            "Profit"
        ].max()

        return (
            f"**{product}** generated the highest total "
            f"profit of **{profit:,.0f}**."
        )

    if (
        product_analysis is not None
        and "product" in q
        and "highest" in q
        and "sales" in q
    ):

        product = product_analysis[
            "Sales"
        ].idxmax()

        sales = product_analysis[
            "Sales"
        ].max()

        return (
            f"**{product}** generated the highest total "
            f"sales of **{sales:,.0f}**."
        )

    if (
        region_analysis is not None
        and "region" in q
        and "highest" in q
        and "profit" in q
    ):

        region = region_analysis[
            "Profit"
        ].idxmax()

        profit = region_analysis[
            "Profit"
        ].max()

        return (
            f"**{region}** generated the highest total "
            f"profit of **{profit:,.0f}**."
        )

    if (
        region_analysis is not None
        and "region" in q
        and "highest" in q
        and "sales" in q
    ):

        region = region_analysis[
            "Sales"
        ].idxmax()

        sales = region_analysis[
            "Sales"
        ].max()

        return (
            f"**{region}** generated the highest total "
            f"sales of **{sales:,.0f}**."
        )

    if (
        monthly_sales is not None
        and "month" in q
        and "sales" in q
    ):

        month = monthly_sales.idxmax()
        sales = monthly_sales.max()

        return (
            f"**{month}** had the highest sales "
            f"at **{sales:,.0f}**."
        )

    if (
        monthly_profit is not None
        and "month" in q
        and "profit" in q
    ):

        month = monthly_profit.idxmax()
        profit = monthly_profit.max()

        return (
            f"**{month}** had the highest profit "
            f"at **{profit:,.0f}**."
        )

    return None

# ---------------------------------------------------------
# ASK YOUR DATA
# ---------------------------------------------------------

st.divider()

st.markdown(
    '<div class="section-title">💬 Ask Your Data</div>',
    unsafe_allow_html=True
)

st.write(
    "Ask a business question about the uploaded dataset."
)

question = st.text_input(
    "Your question",
    placeholder=(
        "Example: Which product has the highest profit margin?"
    ),
    label_visibility="collapsed"
)

if st.button(
    "🔍 Analyze",
    use_container_width=False
):

    if not question.strip():

        st.warning(
            "Please enter a question."
        )

        st.stop()

    # -----------------------------------------------------
    # DIRECT PANDAS ANSWER
    # -----------------------------------------------------

    direct_result = direct_answer(question)

    if direct_result:

        st.markdown(
            "### 📊 Analysis"
        )

        st.success(
            direct_result
        )

        st.caption(
            "Calculated directly using Pandas. "
            "No Gemini API request was required."
        )

        st.stop()

    # -----------------------------------------------------
    # GEMINI
    # -----------------------------------------------------

    prompt = f"""
You are an AI Data Analyst Assistant.

Python and Pandas already calculated the data below.

Your job is to interpret the results, not perform the arithmetic.

DATA:
{analytical_context}

USER QUESTION:
{question}

RULES:

- Answer directly.
- Use only the provided data.
- Never invent numbers.
- Keep the answer concise.
- Give 2-3 useful insights maximum.
- For recommendations, consider sales, profit, margin,
  units and trends.
- Highest sales does not automatically mean the company
  should invest more.
- Do not invent customer behavior, market demand,
  costs or competition.
- If the data is insufficient for a recommendation,
  say so.

FORMAT:

Answer:
1-3 sentences.

Key Insights:
- Insight 1
- Insight 2
- Insight 3

Recommendation:
Only if supported by the data.
"""

    st.markdown(
        "### 🤖 AI Analysis"
    )

    answer_placeholder = st.empty()

    models_to_try = [
        PRIMARY_MODEL,
        FALLBACK_MODEL
    ]

    success = False

    for model_name in models_to_try:

        for attempt in range(2):

            try:

                stream = (
                    client.models.generate_content_stream(
                        model=model_name,
                        contents=prompt,
                        config=types.GenerateContentConfig(
                            temperature=0.2,
                            max_output_tokens=250
                        )
                    )
                )

                full_response = ""

                for chunk in stream:

                    if chunk.text:

                        full_response += chunk.text

                        answer_placeholder.markdown(
                            full_response
                        )

                if full_response.strip():

                    success = True
                    break

            except Exception as e:

                error_text = str(e)

                if "429" in error_text:

                    st.error(
                        "Gemini API quota has been reached. "
                        "Please wait for the quota to reset "
                        "before sending more AI questions."
                    )

                    st.stop()

                if "503" in error_text:

                    if attempt == 0:

                        with st.spinner(
                            "Gemini is temporarily busy. "
                            "Retrying..."
                        ):

                            time.sleep(2)

                        continue

                    break

                st.error(
                    f"Gemini error: {error_text}"
                )

                st.stop()

        if success:
            break

    if not success:

        st.error(
            "Gemini is temporarily unavailable. "
            "Your dataset and Pandas analysis are working "
            "correctly. Please try again shortly."
        )

# ---------------------------------------------------------
# FOOTER
# ---------------------------------------------------------

st.divider()

st.caption(
    "AI Data Analyst Assistant • "
    "Python • Pandas • Streamlit • Gemini API"
)