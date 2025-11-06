# FDS_app.py
import streamlit as st
import plotly.express as px
import pandas as pd
from datetime import datetime
from FDS_backend import load_data, compute_kpis, top_n_countries, region_summary, filter_data

# --- NEW IMPORTS FOR LINEAR REGRESSION ---
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score, mean_squared_error
# ----------------------------------------

# -----------------------------------------------------------
# Page Setup
# -----------------------------------------------------------
st.set_page_config(page_title="🌍 Global COVID-19 Dashboard", layout="wide")

# -----------------------------------------------------------
# Background Styling (CSS)
# -----------------------------------------------------------
st.markdown("""
    <style>
    [data-testid="stAppViewContainer"] {
        background: linear-gradient(135deg, #0f2027, #203a43, #2c5364);
        color: #FFFFFF;
        animation: fadeIn 1.2s ease-in-out;
    }
    [data-testid="stSidebar"] {
        background: #111827;
    }
    h1, h2, h3, h4, h5 {
        color: #FFFFFF !important;
        text-shadow: 0px 0px 6px rgba(255,255,255,0.2);
    }
    .stMetric {
        background-color: rgba(255, 255, 255, 0.05);
        border-radius: 10px;
        padding: 10px;
        box-shadow: 0 4px 10px rgba(0,0,0,0.2);
    }
    @keyframes fadeIn {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    /* Typewriter animation for cinematic header */
    .typewriter {
        overflow: hidden;
        border-right: .15em solid #ffffff;
        white-space: nowrap;
        margin: 0 auto;
        letter-spacing: .1em;
        animation: typing 3.5s steps(30, end), blink-caret 0.75s step-end infinite;
        font-size: 42px;
        font-weight: bold;
        text-align: center;
        color: #FFFFFF;
        text-shadow: 0 0 10px rgba(255,255,255,0.3);
    }
    /* Subtitle fade-in animation */
    .subtitle {
        text-align: center;
        font-size: 20px;
        font-weight: 400;
        color: #E0E0E0;
        opacity: 0;
        animation: fadeInSubtitle 2s ease-in forwards;
        animation-delay: 3.5s;
        margin-top: 10px;
        text-shadow: 0 0 8px rgba(255,255,255,0.15);
    }
    @keyframes typing {
        from { width: 0 }
        to { width: 100% }
    }
    @keyframes blink-caret {
        from, to { border-color: transparent }
        50% { border-color: #FFFFFF; }
    }
    @keyframes fadeInSubtitle {
        from {opacity: 0;}
        to {opacity: 1;}
    }
    </style>
""", unsafe_allow_html=True)

# -----------------------------------------------------------
# Load Data
# -----------------------------------------------------------
try:
    df = load_data()
except FileNotFoundError:
    st.error("❌ CSV file not found! Ensure 'country_wise_latest_covid.csv' is in this folder.")
    st.stop()
except Exception as e:
    st.error(f"⚠️ Error loading data: {e}")
    st.stop()

# -----------------------------------------------------------
# Sidebar Filters
# -----------------------------------------------------------
st.sidebar.header("🔍 Filters")
countries = st.sidebar.multiselect("Select Country", options=df["country"].unique())
regions = st.sidebar.multiselect("Select Region", options=df["region"].unique() if "region" in df.columns else [])
min_cases = st.sidebar.number_input("Min Confirmed Cases", min_value=0, value=0)
max_cases = st.sidebar.number_input("Max Confirmed Cases (optional)", min_value=0, value=0)
search = st.sidebar.text_input("Search Country")

filtered_df = filter_data(
    df,
    country_list=countries if countries else None,
    region_list=regions if regions else None,
    min_cases=min_cases,
    max_cases=max_cases if max_cases > 0 else None,
    search_term=search if search else None,
)

if filtered_df.empty:
    st.warning("⚠️ No data found for the selected filters.")
    st.stop()

# Compute Rates
filtered_df["recovery_rate"] = (filtered_df["recovered"] / filtered_df["confirmed"] * 100).round(2)
filtered_df["death_rate"] = (filtered_df["deaths"] / filtered_df["confirmed"] * 100).round(2)

# -----------------------------------------------------------
# Cinematic Header + Subtitle
# -----------------------------------------------------------
st.markdown("<div class='typewriter'>🌍 Global COVID-19 Dashboard</div>", unsafe_allow_html=True)
st.markdown("<div class='subtitle'>A Real-Time Data Visualization of the Global Pandemic</div>", unsafe_allow_html=True)
st.markdown("<br>", unsafe_allow_html=True)

# -----------------------------------------------------------
# KPI Section
# -----------------------------------------------------------
kpi_data = compute_kpis(filtered_df)
cols = st.columns(3)
for i, (key, val) in enumerate(kpi_data.items()):
    with cols[i % 3]:
        st.metric(label=key, value=f"{val:,}")

st.divider()

# -----------------------------------------------------------
# 🗺️ Global Map Visualization
# -----------------------------------------------------------
st.subheader("🗺️ Worldwide COVID-19 Spread Map")

try:
    fig_map = px.choropleth(
        filtered_df,
        locations="country",
        locationmode="country names",
        color="confirmed",
        hover_name="country",
        hover_data={
            "confirmed": True,
            "deaths": True,
            "recovered": True,
            "recovery_rate": True,
            "death_rate": True,
        },
        color_continuous_scale="Reds",
        title="Total Confirmed COVID-19 Cases by Country",
    )
    fig_map.update_layout(
        geo=dict(showframe=False, showcoastlines=True, projection_type="natural earth"),
        template="plotly_dark",
        margin=dict(l=0, r=0, t=30, b=0),
        transition_duration=800,
    )
    st.plotly_chart(fig_map, use_container_width=True)
except Exception as e:
    st.warning(f"🌐 Could not generate world map: {e}")

st.divider()

# -----------------------------------------------------------
# Comparative Visualizations
# -----------------------------------------------------------
col1, col2, col3 = st.columns(3)

# Top Confirmed
with col1:
    st.subheader("🏆 Top 10 Countries by Confirmed Cases")
    top_cases = top_n_countries(filtered_df, "confirmed", 10)
    if not top_cases.empty:
        top_cases = top_cases.loc[:, ~top_cases.columns.duplicated()]
        fig_confirmed = px.bar(
            top_cases, x="country", y="confirmed", text="confirmed",
            color="confirmed", color_continuous_scale="reds", template="plotly_dark"
        )
        fig_confirmed.update_traces(textposition="outside")
        st.plotly_chart(fig_confirmed, use_container_width=True)

# Top Deaths
with col2:
    st.subheader("⚰️ Top 10 Countries by Deaths")
    top_deaths = top_n_countries(filtered_df, "deaths", 10)
    top_deaths = top_deaths.loc[:, ~top_deaths.columns.duplicated()]
    if not top_deaths.empty:
        fig_death = px.bar(
            top_deaths, x="country", y="deaths", text="deaths",
            color="deaths", color_continuous_scale="Greys", template="plotly_dark"
        )
        fig_death.update_traces(textposition="outside")
        st.plotly_chart(fig_death, use_container_width=True)

# Top Recovered
with col3:
    st.subheader("💪 Top 10 Countries by Recoveries")
    if "recovered" in filtered_df.columns:
        top_recovered = top_n_countries(filtered_df, "recovered", 10)
        top_recovered = top_recovered.loc[:, ~top_recovered.columns.duplicated()]
        if not top_recovered.empty:
            fig_recover = px.bar(
                top_recovered, x="country", y="recovered", text="recovered",
                color="recovered", color_continuous_scale="greens", template="plotly_dark"
            )
            fig_recover.update_traces(textposition="outside")
            st.plotly_chart(fig_recover, use_container_width=True)

st.divider()

# -----------------------------------------------------------
# 📊 Linear Regression Analysis (New Section)
# -----------------------------------------------------------
st.subheader("📈 Linear Regression: Confirmed Cases vs. Deaths")

# Filter data for regression: must have non-zero deaths and confirmed cases
regression_df = filtered_df[
    (filtered_df["deaths"] > 0) & (filtered_df["confirmed"] > 0)
].copy()

if len(regression_df) >= 2:
    # Prepare data for scikit-learn
    # x (Deaths) must be reshaped for the model
    x = regression_df["deaths"].values.reshape(-1, 1)
    y = regression_df["confirmed"].values

    # 1. Model Training
    model = LinearRegression()
    model.fit(x, y)
    y_pred = model.predict(x)

    # 2. Metrics Calculation
    r2 = r2_score(y, y_pred)
    mse = mean_squared_error(y, y_pred)
    rmse = np.sqrt(mse)
    slope = model.coef_[0]
    intercept = model.intercept_
    
    # 3. Streamlit Display (Metrics)
    st.markdown(f"""
        <div style='background-color: #111827; padding: 10px; border-radius: 5px; font-size: 16px;'>
        Linear Equation: $\\text{{Confirmed}} = {slope:.4f} \\times \\text{{Deaths}} + {intercept:.2f}$<br>
        $R^2$ Score: <b>{r2:.4f}</b> | RMSE: <b>{rmse:.2f}</b>
        </div>
    """, unsafe_allow_html=True)


    # 4. Plotting using Matplotlib/Seaborn (Rendered via st.pyplot)
    fig, ax = plt.subplots(figsize=(10, 6))
    
    # Scatter plot of actual data
    sns.scatterplot(x=regression_df["deaths"], y=regression_df["confirmed"], color="royalblue", alpha=0.6, label="Actual Data", ax=ax)
    
    # Regression line
    ax.plot(regression_df["deaths"], y_pred, color="crimson", linewidth=2.5, label="Regression Line")

    ax.set_title("Linear Regression: Confirmed Cases vs Deaths", fontsize=16, weight='bold', color='white')
    ax.set_xlabel("Deaths", fontsize=12, color='white')
    ax.set_ylabel("Confirmed Cases", fontsize=12, color='white')
    ax.legend(facecolor='#333333', edgecolor='white', labelcolor='white')
    ax.grid(alpha=0.3)
    
    # Annotate the plot with results
    ax.text(
        x=regression_df["deaths"].max() * 0.5,
        y=regression_df["confirmed"].max() * 0.3,
        s=f"Equation: Confirmed = {slope:.2f} × Deaths + {intercept:.2f}\n$R^2$ = {r2:.4f}\nRMSE = {rmse:.2f}",
        fontsize=10,
        bbox=dict(facecolor='#333333', alpha=0.7, edgecolor='gray', boxstyle='round,pad=0.5', color='white')
    )
    
    # Set plot background to match Streamlit dark theme
    ax.set_facecolor("#203a43")
    fig.patch.set_facecolor("#203a43")
    ax.tick_params(colors='white')
    
    plt.tight_layout()
    st.pyplot(fig)
    plt.close(fig) # Prevent memory leaks
else:
    st.info("Insufficient data points (less than 2) with non-zero cases/deaths for regression analysis based on current filters.")

st.divider()

# -----------------------------------------------------------
# 🥧 Case Severity Breakdown (Global Share)
# -----------------------------------------------------------
st.subheader("🥧 Case Severity Breakdown (Global Share)")
try:
    total_confirmed = filtered_df["confirmed"].sum()
    total_deaths = filtered_df["deaths"].sum()
    total_recovered = filtered_df["recovered"].sum()

    severity_data = pd.DataFrame({
        "Category": ["Confirmed", "Deaths", "Recovered"],
        "Count": [total_confirmed, total_deaths, total_recovered],
    })

    fig_severity = px.pie(
        severity_data,
        values="Count",
        names="Category",
        color_discrete_sequence=px.colors.qualitative.Set2,
        hole=0.4,
        title="Global Distribution by Case Severity",
    )
    fig_severity.update_layout(transition_duration=800, template="plotly_dark")
    st.plotly_chart(fig_severity, use_container_width=True)
except Exception as e:
    st.warning(f"🥧 Could not generate case severity chart: {e}")

# -----------------------------------------------------------
# Footer
# -----------------------------------------------------------
st.markdown("---")
st.markdown(
    f"""
    <div style='text-align:center; font-size:14px; color:#D1D5DB; text-shadow:0px 0px 6px rgba(255,255,255,0.2);'>
        ✅ Dashboard Ready — Data Source: WHO Global Reports<br>
        📅 Last updated: <b>{datetime.now().strftime("%d %B %Y, %I:%M %p")}</b><br>
        👨‍💻 Developed by <b>Atharva Khobrekar</b> | Streamlit + Plotly
    </div>
    """,
    unsafe_allow_html=True,
)
