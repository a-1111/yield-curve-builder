import numpy as np
from scipy.interpolate import CubicSpline


# UK Gilt maturities (years) and yields (%) — sample data

GILT_DATA = {
    "maturities": [0.25, 0.5, 1, 2, 3, 5, 7, 10, 15, 20, 30],
    "yields": [5.20, 5.10, 4.85, 4.45, 4.30, 4.20, 4.25, 4.35, 4.55, 4.60, 4.70],
}


def get_gilt_data():
    return GILT_DATA["maturities"], GILT_DATA["yields"]


def interpolate_curve(maturities, yields, num_points=200):
    cs = CubicSpline(maturities, yields)
    smooth_mats = np.linspace(min(maturities), max(maturities), num_points)
    smooth_yields = cs(smooth_mats)
    return smooth_mats, smooth_yields, cs


def get_yield_at_maturity(cs, maturity):
    return float(cs(maturity))


def calc_spread(cs, short_tenor, long_tenor):
    short_yield = get_yield_at_maturity(cs, short_tenor)
    long_yield = get_yield_at_maturity(cs, long_tenor)
    spread_bps = (long_yield - short_yield) * 100
    return spread_bps, short_yield, long_yield


def calc_forward_rate(cs, t1, t2):
    y1 = get_yield_at_maturity(cs, t1) / 100
    y2 = get_yield_at_maturity(cs, t2) / 100
    forward = ((1 + y2) ** t2 / (1 + y1) ** t1) ** (1 / (t2 - t1)) - 1
    return forward * 100


if __name__ == "__main__":
    mats, ylds = get_gilt_data()
    _, _, cs = interpolate_curve(mats, ylds)

    spread, y2, y10 = calc_spread(cs, 2, 10)
    print(f"2Y Yield:  {y2:.2f}%")
    print(f"10Y Yield: {y10:.2f}%")
    print(f"2s10s Spread: {spread:.1f} bps")

    fwd = calc_forward_rate(cs, 2, 5)
    print(f"\n2y5y Forward Rate: {fwd:.2f}%")
