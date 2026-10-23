# Matching parents and children with SQL: an intergenerational elasticity tutorial

How much of a parent's income advantage reaches their children — and why does the answer depend on *when* income is measured? This repository matches children to their parents in the Panel Study of Income Dynamics (PSID) using SQL inside Python (`sqlite3`), builds parent and child income measures, and estimates the intergenerational income elasticity (IGE) with single-year and multi-year income, showing the life-cycle bias that single-year measures produce.

Published post: https://1iiiiii.github.io/Personal-Website/blog/posts/post6/

## Data

| Source | File / variables | What it contains | Period |
|---|---|---|---|
| PSID, Data Center custom extract (job `J366383`) — individual file merged with family files | `data/raw/J366383.xlsx` (**not committed**; see below) | One row per person ever in the study (85,536) with: permanent person ID (`ER30001`, `ER30002`), sex, father's and mother's IDs (`ER32016/17`, `ER32009/10`); per wave: age, interview number, relationship to head, sequence number; family interview number and total family money income | 1968–2023, 43 waves (annual to 1997, biennial after) |
| PSID cross-year variable index | `data/raw/psid_variable_crosswalk.csv` | Maps each PSID code to a readable name (`fam_income_1990`), its file and wave | — |
| FRED, BLS CPI-U all items (`CPIAUCSL`) | `data/raw/cpi_u_annual.csv` | Annual-average CPI and deflator to the base year (fetched by `01_load_psid.ipynb`; access date in `data/raw/fetch_log.json`) | 1967– |

PSID family income reported in survey year *t* refers to calendar year *t − 1*; incomes are deflated with the CPI of the income year.

**Rebuilding the PSID extract.** PSID's terms of use do not allow redistributing the microdata, so the extract is git-ignored. To rebuild it: register (free) at https://simba.isr.umich.edu, open the Data Center, create a data cart, paste the variable list in `data/raw/psid_variable_list.txt`, and download as "Microsoft Excel Spreadsheet" with "All Individuals". Save the file as `data/raw/J366383.xlsx` (or change `EXTRACT` in notebook 01). The Data Center adds ~45 bookkeeping columns of its own; notebook 01 drops them.

Citation: Panel Study of Income Dynamics, public use dataset. Produced and distributed by the Survey Research Center, Institute for Social Research, University of Michigan, Ann Arbor, MI (2025).

## Setup

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

Open the notebooks in VS Code with the `.venv` kernel selected. No API keys are needed.

## Replication

Run the notebooks in `code/` in order; each reads the previous one's output files.

| Notebook | Reads | Writes |
|---|---|---|
| `01_load_psid.ipynb` | `data/raw/J366383.xlsx`, crosswalk, FRED | `data/processed/psid_wide.parquet` (readable column names), `data/raw/cpi_u_annual.csv`, `data/raw/fetch_log.json` |
| `02_build_database.ipynb` | `data/processed/psid_wide.parquet`, CPI | `data/processed/psid.sqlite` with tables `individuals`, `persons`, `families`; `results/tables/table_counts.csv` |
| `03_match_and_ige.ipynb` | `data/processed/psid.sqlite` | `data/processed/matched.csv`, `results/tables/ige_estimates.csv`, `results/tables/ige_by_child_age.csv` |
| `04_figures.ipynb` | `data/processed/`, `results/tables/` | `results/figures/fig1_*.png`, `results/figures/fig2_*.png` |

### Sample and specification (all in `03_match_and_ige.ipynb`)

- **Child observations:** person-years in which the person is head or spouse of their own family unit (relationship-to-head codes 1–2 before 1983, 10/20/22 from 1983), aged 25–45. Child income is the family's total money income (head plus spouse), CPI-adjusted to 2023 dollars.
- **Parent–child match:** a self-join of `individuals` on the father's permanent ID (`father_id_1968`, `father_person_num`) = (`id_1968`, `person_num`). A LEFT JOIN first counts the children without a matched father (reported in the post); inner joins thereafter.
- **Parent income:** the father's family income in the survey years when the child was aged 13–17. *Single-year* = the year the child was closest to 15; *multi-year* = the average over the observed years (at least two required, so both measures use the same children).
- **Child income:** average over ages 30–40 for the main estimates; a single year at ages 25, 30, 35, 40 and 45 (±1 year, since waves are biennial after 1997) for the life-cycle figure.
- **Estimation:** OLS of log child income on log parent income, standard errors clustered by father. Main sample is the SRC (nationally representative) sample, `id_1968` ≤ 2930; SRC + SEO (low-income oversample) is reported as a robustness row. Non-positive incomes are dropped before logs. Birth year = min(year − age).

### Results (`results/tables/`)

| Parent income | Child income | β | s.e. | N |
|---|---|---|---|---|
| single year (child ≈ 15) | average, ages 30–40 | 0.25 | 0.03 | 3,951 |
| average, child ages 13–17 | average, ages 30–40 | 0.43 | 0.02 | 3,951 |

IGE by the child's age at measurement (parent income = 13–17 average): 0.25 at 25, 0.35 at 30, 0.45 at 35, 0.52 at 40, 0.45 at 45 (`ige_by_child_age.csv`).

## Folder layout

```
code/               notebooks in run order, plus plot_style.py (shared figure style)
data/raw/           PSID extract (git-ignored), variable list and crosswalk, CPI
data/processed/     parquet cache, SQLite database, matched sample (all git-ignored: derived from PSID microdata)
results/figures/    the figures embedded in the post
results/tables/     every number quoted in the post
```
