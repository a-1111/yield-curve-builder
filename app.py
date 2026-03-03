import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from yield_curve import get_gilt_data, interpolate_curve, calc_spread, calc_forward_rate

st.set_page_config(page_title="Yield Curve Builder", layout="wide")
st.title("UK Gilt Yield Curve Builder & Analyser")
st.caption("Cubic spline interpolation with spread and forward rate analysis")

# --- Let user override yields in sidebar ---
st.sidebar.header("Gilt Yields (%)")
default_mats, default_ylds = get_gilt_data()

user_yields = []
for i, mat in enumerate(default_mats):
    label = f"{mat}Y" if mat >= 1 else f"{int(mat*12)}M"
    val = st.sidebar.number_input(label, value=default_ylds[i], step=0.05, format="%.2f")
    user_yields.append(val)

# --- Interpolate ---
smooth_mats, smooth_yields, cs = interpolate_curve(default_mats, user_yields)

# --- Curve plot ---
st.subheader("Yield Curve")
fig, ax = plt.subplots(figsize=(10, 5))
ax.plot(smooth_mats, smooth_yields, linewidth=2, label="Interpolated Curve")
ax.scatter(default_mats, user_yields, color="red", zorder=5, label="Gilt Data Points")
ax.set_xlabel("Maturity (Years)")
ax.set_ylabel("Yield (%)")
ax.legend()
ax.grid(True, alpha=0.3)
st.pyplot(fig)

# --- Spreads ---
st.subheader("Key Spreads")
col1, col2, col3 = st.columns(3)

spread_2s10s, y2, y10 = calc_spread(cs, 2, 10)
spread_2s5s, _, y5 = calc_spread(cs, 2, 5)
spread_5s30s, _, y30 = calc_spread(cs, 5, 30)

with col1:
    st.metric("2s10s Spread", f"{spread_2s10s:.1f} bps")
    st.caption(f"2Y: {y2:.2f}% | 10Y: {y10:.2f}%")

with col2:
    st.metric("2s5s Spread", f"{spread_2s5s:.1f} bps")
    st.caption(f"2Y: {y2:.2f}% | 5Y: {y5:.2f}%")

with col3:
    st.metric("5s30s Spread", f"{spread_5s30s:.1f} bps")
    st.caption(f"5Y: {y5:.2f}% | 30Y: {y30:.2f}%")

# --- Curve shape interpretation ---
st.subheader("Curve Shape")
if spread_2s10s > 50:
    st.success("Steep curve — market expects rate hikes or higher growth/inflation ahead.")
elif spread_2s10s > 0:
    st.info("Normal curve — modest term premium, no strong signal.")
elif spread_2s10s > -50:
    st.warning("Flat/slightly inverted — market pricing in potential slowdown or rate cuts.")
else:
    st.error("Deeply inverted — historically a strong recession signal.")

# --- Forward rates ---
st.subheader("Implied Forward Rates")
col4, col5 = st.columns(2)

fwd_2y5y = calc_forward_rate(cs, 2, 5)
fwd_5y10y = calc_forward_rate(cs, 5, 10)

with col4:
    st.metric("2y5y Forward", f"{fwd_2y5y:.2f}%")
    st.caption("Market-implied 3Y rate, 2 years from now")

with col5:
    st.metric("5y10y Forward", f"{fwd_5y10y:.2f}%")
    st.caption("Market-implied 5Y rate, 5 years from now")
