# Cohen's kappa between the two QUADAS-2 assessors
# Assessor 1: QUADAS_pineda_Ratings.xlsx
# Assessor 2: QUADAS2_Azza_Ratings.xlsx
# Output: results.txt

import random
import openpyxl

DOMAINS = ["Patient Selection", "Index Test", "Reference Standard", "Flow & Timing"]
CATS = ["Low", "Unclear", "High"]

wb1 = openpyxl.load_workbook("QUADAS_pineda_Ratings.xlsx", data_only=True)
ws1 = wb1["QUADAS-2 Figure 6 Ratings"]
r1 = [[row[1], row[2], row[3], row[4]] for row in ws1.iter_rows(min_row=2, values_only=True) if row[0]]

wb2 = openpyxl.load_workbook("QUADAS2_Azza_Ratings.xlsx", data_only=True)
ws2 = wb2["QUADAS-2 Assessment"]
r2 = [[row[3], row[5], row[7], row[9]] for row in ws2.iter_rows(min_row=2, values_only=True) if row[0]]

assert len(r1) == len(r2) == 25, "study count mismatch"

# pairs of (assessor1, assessor2) judgements, per domain and pooled
pairs_by_domain = {d: [] for d in DOMAINS}
for a, b in zip(r1, r2):
    for j, d in enumerate(DOMAINS):
        pairs_by_domain[d].append((a[j], b[j]))
pooled = [p for d in DOMAINS for p in pairs_by_domain[d]]


def kappa(pairs):
    n = len(pairs)
    po = sum(1 for a, b in pairs if a == b) / n
    pe = 0.0
    for c in CATS:
        p1 = sum(1 for a, _ in pairs if a == c) / n
        p2 = sum(1 for _, b in pairs if b == c) / n
        pe += p1 * p2
    return (po - pe) / (1 - pe), po


def bootstrap_ci(pairs, reps=10000, seed=42):
    random.seed(seed)
    vals = []
    n = len(pairs)
    for _ in range(reps):
        sample = [pairs[random.randrange(n)] for _ in range(n)]
        try:
            vals.append(kappa(sample)[0])
        except ZeroDivisionError:
            continue
    vals.sort()
    return vals[int(0.025 * len(vals))], vals[int(0.975 * len(vals))]


def weighted_kappa(pairs):
    # linear weights, Low=0 Unclear=1 High=2
    num = {"Low": 0, "Unclear": 1, "High": 2}
    n = len(pairs)
    w = lambda a, b: 1 - abs(num[a] - num[b]) / 2
    po = sum(w(a, b) for a, b in pairs) / n
    pe = 0.0
    for a in CATS:
        for b in CATS:
            p1 = sum(1 for x, _ in pairs if x == a) / n
            p2 = sum(1 for _, y in pairs if y == b) / n
            pe += w(a, b) * p1 * p2
    return (po - pe) / (1 - pe)


lines = []
k, po = kappa(pooled)
lo, hi = bootstrap_ci(pooled)
lines.append("Cohen's kappa, assessor 1 vs assessor 2 (25 studies x 4 domains = 100 judgements)")
lines.append("")
lines.append(f"Pooled:  kappa = {k:.2f}   95% CI {lo:.2f} to {hi:.2f}   agreement = {po:.0%}")
lines.append(f"Weighted (linear): kappa = {weighted_kappa(pooled):.2f}")
lines.append("")
for dom in DOMAINS:
    kd, pod = kappa(pairs_by_domain[dom])
    lod, hid = bootstrap_ci(pairs_by_domain[dom])
    lines.append(f"{dom}:  kappa = {kd:.2f}   95% CI {lod:.2f} to {hid:.2f}   agreement = {pod:.0%}")
lines.append("")
lines.append("CI: percentile bootstrap, 10,000 resamples.")

with open("results.txt", "w") as f:
    f.write("\n".join(lines) + "\n")
print("\n".join(lines))
