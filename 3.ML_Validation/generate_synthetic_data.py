"""
Synthetic data generator for the "Silentes" KPI validation demo.

The real project used company-internal sales and network-traffic data that cannot
be shared. This script builds a SYNTHETIC replacement with the same structure:
one row per sales activation (PCS), the behavioural features described in the
README (section 7) and a target that says whether the sale turned out to be a
low-quality one (the line disconnected within 6 months).

Nothing here is real. Values are randomly generated (seed 2026) from three hidden
customer segments, calibrated so that the original KPI behaves like in the
original study: high precision, low recall. The numbers produced by the demo are
therefore a demonstration of the METHOD, not business results.

Usage:  python generate_synthetic_data.py   ->  data/synthetic_activations.csv
"""
from pathlib import Path

import numpy as np
import pandas as pd

SEED = 2026
N = 80_000
OUT = Path(__file__).parent / "data" / "synthetic_activations.csv"


def logit(p):
    return np.log(p / (1 - p))


def sigmoid(x):
    return 1 / (1 + np.exp(-x))


def generate(n: int = N, seed: int = SEED) -> pd.DataFrame:
    rng = np.random.default_rng(seed)

    # Hidden customer segments (not observed by the analyst):
    #   A = genuine, active users
    #   B = low-adoption users
    #   C = "silent" activations: new account, many accounts opened, almost no usage
    seg = rng.choice(["A", "B", "C"], n, p=[0.66, 0.27, 0.07])
    is_a, is_b, is_c = seg == "A", seg == "B", seg == "C"

    # --- days with traffic in the 21 days after the sale -----------------------
    traffic_days = np.where(is_a, rng.normal(17, 3.5, n),
                    np.where(is_b, rng.normal(9.5, 4.5, n), rng.normal(4, 3.5, n)))
    traffic_days = np.clip(np.round(traffic_days), 0, 21).astype(int)
    zero_prob = np.where(is_a, 0.002, np.where(is_b, 0.02, 0.42))
    traffic_days[rng.random(n) < zero_prob] = 0

    # first day with traffic (99 = never within 21 days)
    scale = np.where(is_a, 2.0, np.where(is_b, 5.0, 9.0))
    first_day = np.ceil(rng.exponential(scale)).astype(int).clip(1, 21)
    first_day = np.minimum(first_day, 21 - traffic_days + 1).clip(1, 21)
    first_day[traffic_days == 0] = 99

    # --- account / customer attributes ----------------------------------------
    customer_old = (rng.random(n) < np.where(is_a, 0.55, np.where(is_b, 0.30, 0.12))).astype(int)
    old_account = (rng.random(n) < np.where(is_a, 0.50, np.where(is_b, 0.22, 0.05))).astype(int)
    accounts_opened = 1 + rng.poisson(np.where(is_a, 0.25, np.where(is_b, 0.6, 2.8)))

    # --- traffic volumes --------------------------------------------------------
    active = traffic_days > 0
    incoming = np.where(active, traffic_days * rng.lognormal(0.6, 0.8, n), 0).round(1)
    outgoing = np.where(active, traffic_days * rng.lognormal(0.9, 0.8, n), 0).round(1)
    mobile_data = np.where(active, traffic_days * rng.lognormal(3.8, 1.0, n), 0).round(0)

    # --- target: low-quality sale (line disconnected within 6 months) ---------
    base = np.where(is_a, 0.13, np.where(is_b, 0.62, 0.64))
    lin = (logit(base)
           - 0.05 * (traffic_days - np.where(is_a, 17, np.where(is_b, 9.5, 4)))
           - 0.9 * old_account
           + 1.1 * (accounts_opened >= 3))
    disconnected = (rng.random(n) < sigmoid(lin)).astype(int)

    return pd.DataFrame({
        "pcs_id": np.arange(1, n + 1),
        "silent_21": (first_day > 21).astype(int),
        "silent_15": (first_day > 15).astype(int),
        "silent_10": (first_day > 10).astype(int),
        "silent_5": (first_day > 5).astype(int),
        "traffic_days_21": traffic_days,
        "customer_old": customer_old,
        "old_account": old_account,
        "accounts_opened": accounts_opened,
        "incoming_calls": incoming,
        "outgoing_calls": outgoing,
        "mobile_data": mobile_data,
        "disconnected_6m": disconnected,
    })


if __name__ == "__main__":
    df = generate()
    OUT.parent.mkdir(parents=True, exist_ok=True)
    df.to_csv(OUT, index=False)
    print(f"{len(df):,} synthetic activations written to {OUT}")
    print(f"share disconnected: {df.disconnected_6m.mean():.1%} | share flagged silent_21: {df.silent_21.mean():.1%}")
