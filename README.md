# Yield Curve Builder & Analyser

UK Gilt yield curve construction

## Features
- Interactive yield inputs for all standard Gilt maturities
- Cubic spline interpolation for smooth curve
- Key spreads: 2s10s, 2s5s, 5s30s
- Curve shape interpretation (steep, normal, flat, inverted)
- Implied forward rates (2y5y, 5y10y)

## Run Locally
pip install -r requirements.txt
streamlit run app.py

## Background
Built to demonstrate understanding of the rates market, super important for fic desks