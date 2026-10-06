"""
KPI validation demo ("Silentes"): baseline KPI vs decision-tree-derived rules.

Reads data/synthetic_activations.csv (synthetic, see generate_synthetic_data.py),
and produces:
  * the performance of the ORIGINAL KPI (no traffic in 21 days) as a baseline,
  * a depth-3 decision tree trained to explain the low-quality outcome,
  * two rule proposals taken from the tree's "Silent" branch,
  * figures in figures/ and a short markdown report in report.md.

The tree is used as an interpretability tool (rules extraction), not as a
production classifier.

Usage:  python validate_kpi.py
"""
from pathlib import Path

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.tree import DecisionTreeClassifier, export_text, plot_tree

HERE = Path(__file__).parent
FIG = HERE / "figures"
FIG.mkdir(exist_ok=True)
DARK_RED, LIGHT_RED, GREY = "#b22222", "#f4a29a", "#9a9a9a"

df = pd.read_csv(HERE / "data" / "synthetic_activations.csv")
TARGET = "disconnected_6m"
FEATURES = ["silent_21", "silent_15", "silent_10", "silent_5", "traffic_days_21",
            "customer_old", "old_account", "accounts_opened",
            "incoming_calls", "outgoing_calls", "mobile_data"]

train, test = train_test_split(df, test_size=0.3, random_state=2026, stratify=df[TARGET])


def pr(y_true, y_pred):
    tp = int(((y_pred == 1) & (y_true == 1)).sum())
    fp = int(((y_pred == 1) & (y_true == 0)).sum())
    fn = int(((y_pred == 0) & (y_true == 1)).sum())
    tn = int(((y_pred == 0) & (y_true == 0)).sum())
    precision = tp / (tp + fp) if tp + fp else 0.0
    recall = tp / (tp + fn) if tp + fn else 0.0
    return dict(tp=tp, fp=fp, fn=fn, tn=tn, precision=precision, recall=recall, flagged=tp + fp)


# ---------------------------------------------------------------- 1. baseline KPI
base = pr(test[TARGET].values, test["silent_21"].values)

# ---------------------------------------------------------------- 2. decision tree
tree = DecisionTreeClassifier(max_depth=3, min_samples_leaf=150, random_state=2026)
tree.fit(train[FEATURES], train[TARGET])
rules_text = export_text(tree, feature_names=FEATURES, show_weights=True)
imp = pd.Series(tree.feature_importances_, index=FEATURES).sort_values(ascending=False)
imp = imp[imp > 0]

# ---------------------------------------------------------------- 3. rules from the tree
# Proposal 1: full decision path of the "Silent" branch.
# Proposal 2: the same path with one condition relaxed (more coverage, lower precision).
# The thresholds are read from the fitted tree: the leaf with the highest share of
# low-quality sales among those that contain at least 1% of the training data.
t = tree.tree_
leaf_ids = np.where(t.children_left == -1)[0]
paths = {}


def tighten(conds):
    # keep only the tightest threshold per (feature, operator)
    best = {}
    for f, op, thr in conds:
        k = (f, op)
        if k not in best or (op == '<=' and thr < best[k]) or (op == '>' and thr > best[k]):
            best[k] = thr
    return [(f, op, thr) for (f, op), thr in best.items()]


def walk(node, conds):
    if t.children_left[node] == -1:
        paths[node] = conds
        return
    f, thr = FEATURES[t.feature[node]], t.threshold[node]
    walk(t.children_left[node], conds + [(f, "<=", thr)])
    walk(t.children_right[node], conds + [(f, ">", thr)])


walk(0, [])
leaf_stats = []
for leaf in leaf_ids:
    v = t.value[leaf][0]
    rate = v[1] / v.sum()
    leaf_stats.append((leaf, rate, t.n_node_samples[leaf]))
best_leaf = max([s for s in leaf_stats if s[2] >= 0.01 * len(train)], key=lambda s: s[1])[0]
best_path = paths[best_leaf]


def apply(df_, conds):
    mask = np.ones(len(df_), dtype=bool)
    for f, op, thr in conds:
        mask &= (df_[f] <= thr) if op == "<=" else (df_[f] > thr)
    return mask.astype(int)


p1 = pr(test[TARGET].values, apply(test, best_path))
# Proposal 2 relaxes the single condition whose removal gives the most coverage (recall)
candidates = []
for i in range(len(best_path)):
    sub = best_path[:i] + best_path[i + 1:]
    candidates.append((pr(test[TARGET].values, apply(test, sub))["recall"], i, sub))
_, dropped_idx, path2 = max(candidates)
dropped = best_path[dropped_idx]
p2 = pr(test[TARGET].values, apply(test, path2))
fmt = lambda c: " AND ".join(f"{f} {op} {thr:.1f}" for f, op, thr in c)

# ---------------------------------------------------------------- figures
# 1. confusion matrix of the original KPI
fig, ax = plt.subplots(figsize=(5.2, 4.2))
cm = np.array([[base["tp"], base["fn"]], [base["fp"], base["tn"]]])
ax.imshow(cm, cmap="Reds", vmin=0, vmax=cm.max() * 1.6)
for i in range(2):
    for j in range(2):
        ax.text(j, i, f"{cm[i, j]:,}", ha="center", va="center", fontsize=13, fontweight="bold")
ax.set_xticks([0, 1], ["Flagged Silent", "Not flagged"])
ax.set_yticks([0, 1], ["Disconnected\n(low quality)", "Did not\ndisconnect"])
ax.set_title("Original KPI vs actual outcome (test set)")
fig.tight_layout(); fig.savefig(FIG / "kpi_confusion_matrix.png", dpi=130); plt.close(fig)

# 2. feature importance
fig, ax = plt.subplots(figsize=(6.4, 3.6))
imp.sort_values().plot.barh(ax=ax, color=DARK_RED)
ax.set_xlabel("Importance"); ax.set_title("Variable importance - Decision Tree")
fig.tight_layout(); fig.savefig(FIG / "feature_importance.png", dpi=130); plt.close(fig)

# 3. tree
fig, ax = plt.subplots(figsize=(15, 6.2))
plot_tree(tree, feature_names=FEATURES, class_names=["Not low quality", "Low quality"],
          filled=True, impurity=False, proportion=False, fontsize=8, ax=ax)
ax.set_title("Decision tree (depth 3)", loc="left", fontsize=14, fontstyle="italic")
fig.tight_layout(); fig.savefig(FIG / "decision_tree.png", dpi=130); plt.close(fig)

# 4. comparison of definitions
labels = ["Current KPI", "Proposal 1\n(full path)", "Proposal 2\n(subset)"]
prec = [base["precision"], p1["precision"], p2["precision"]]
rec = [base["recall"], p1["recall"], p2["recall"]]
x = np.arange(3)
fig, ax = plt.subplots(figsize=(7.2, 4))
b1 = ax.bar(x - 0.18, prec, 0.36, color=DARK_RED, label="Precision")
b2 = ax.bar(x + 0.18, rec, 0.36, color=LIGHT_RED, label="Recall")
for bars in (b1, b2):
    for b in bars:
        ax.text(b.get_x() + b.get_width() / 2, b.get_height() + 0.01, f"{b.get_height():.0%}", ha="center")
ax.set_xticks(x, labels); ax.set_ylim(0, 1.05); ax.legend(frameon=False)
ax.set_title("Proposal comparison (test set, synthetic data)")
fig.tight_layout(); fig.savefig(FIG / "proposal_comparison.png", dpi=130); plt.close(fig)

# ---------------------------------------------------------------- report
prev = df[TARGET].mean()
report = f"""# KPI validation demo (synthetic data)

> **These results come from SYNTHETIC data** generated by `generate_synthetic_data.py`.
> They demonstrate the method (baseline KPI -> decision tree -> rule proposals) and
> were calibrated to behave like the original study (high-precision, low-recall KPI);
> they are **not** the original business results, which are in the main README.

Dataset: {len(df):,} activations, {prev:.1%} low-quality (disconnected within 6 months).
Train/test split: 70/30, stratified. All metrics below are on the **test set** ({len(test):,} activations).

## 1. Baseline: original KPI (no traffic within 21 days)

| | Value |
|---|---:|
| True positives | {base['tp']:,} |
| False positives | {base['fp']:,} |
| False negatives | {base['fn']:,} |
| True negatives | {base['tn']:,} |
| **Precision** | **{base['precision']:.1%}** |
| **Recall** | **{base['recall']:.1%}** |

![confusion matrix](figures/kpi_confusion_matrix.png)

## 2. Decision tree (depth 3)

Variable importance:

| Variable | Importance |
|---|---:|
""" + "\n".join(f"| {k} | {v:.1%} |" for k, v in imp.items()) + f"""

![importance](figures/feature_importance.png)
![tree](figures/decision_tree.png)

Tree rules:

```text
{rules_text}```

## 3. Rule proposals from the "Silent" branch

* **Proposal 1** (full decision path): `{fmt(best_path)}`
* **Proposal 2** (relaxing `{fmt([dropped])}`): `{fmt(path2)}`

| Definition | Precision | Recall | Flagged |
|---|---:|---:|---:|
| Current KPI | {base['precision']:.1%} | {base['recall']:.1%} | {base['flagged']:,} |
| Proposal 1 | {p1['precision']:.1%} | {p1['recall']:.1%} | {p1['flagged']:,} |
| Proposal 2 | {p2['precision']:.1%} | {p2['recall']:.1%} | {p2['flagged']:,} |

![comparison](figures/proposal_comparison.png)

**Reading:** stricter rules give higher precision but lower recall; relaxing a condition
increases coverage at the cost of precision. This is the trade-off the business has to
decide on (for instance, the cost of wrongly decommissioning a line vs the cost of
missing a low-quality sale).
"""
(HERE / "report.md").write_text(report, encoding="utf-8")

print(f"baseline  precision={base['precision']:.3f} recall={base['recall']:.3f} flagged={base['flagged']}")
print(f"proposal1 precision={p1['precision']:.3f} recall={p1['recall']:.3f} flagged={p1['flagged']}  | {fmt(best_path)}")
print(f"proposal2 precision={p2['precision']:.3f} recall={p2['recall']:.3f} flagged={p2['flagged']} | {fmt(path2)}")
print("importance:", imp.round(3).to_dict())
