# QUADAS-2 Inter-Rater Agreement Analysis

Data and code for the systematic review of photoplethysmographic (PPG) sensing of peripheral arterial disease (PAD). Two assessors independently rated the 25 included studies with the QUADAS-2 tool (4 domains per study, 100 judgements in total). This repository contains both rating sets and the script used to quantify inter-rater agreement. The assessor-2 workbook also includes the QUADAS-2 applicability assessments for all 25 studies.

## Contents

| File | Description |
|------|-------------|
| `QUADAS_pineda_Ratings.xlsx` | Assessor 1 — QUADAS-2 ratings |
| `QUADAS2_Azza_Ratings.xlsx` | Assessor 2 — ratings with supporting evidence per cell (judgement, reason, verbatim source sentence, section and page) |
| `kappa_analysis.py` | Computes Cohen's kappa between the two assessors |
| `results.txt` | Script output |

## Usage

Requires Python 3 with `openpyxl`:

```
python kappa_analysis.py
```

## Result

Pooled Cohen's kappa = 0.69 (95% CI 0.56 to 0.80) across the 100 domain judgements, with 80% observed agreement. Per-domain values are listed in `results.txt`.

## Confidence intervals

The 95% confidence intervals are percentile bootstrap intervals: the 100 (assessor 1, assessor 2) judgement pairs are resampled with replacement 10,000 times, kappa is recomputed on each resample, and the interval is taken from the 2.5th and 97.5th percentiles of the resulting distribution. The random seed is fixed (42), so rerunning the script reproduces the reported values exactly.
