# Reproducible code checks

These three checks concern **publicly listed** observations in this audit. The scripts download the authors' own public code at fixed commits, verify SHA-256, and run bounded tests. No private correspondence, patient-level data, or full model training is included here. The audit is AI assisted. These checks are not editorial or independent peer review.

## Run

Python 3.11 or newer and an internet connection are required for the first run.

```bash
python3 -m venv .venv
.venv/bin/python -m pip install -r requirements.txt
.venv/bin/python reproducir.py all
```

Run one check with `ga`, `arg`, or `gastric` instead of `all`. Downloaded originals remain in `.cache/`, which Git ignores. Every downloaded file is checked against its pinned SHA-256. The script fails if an original changes or a stated condition does not hold.

## Checks and limits

| Case | Source and fixed version | Direct observation | Limit |
| --- | --- | --- | --- |
| [s41598-025-86362-8](https://doi.org/10.1038/s41598-025-86362-8) | [Official notebook](https://github.com/priyam-03/GA-Feature-Selector-Lung-Cancer/blob/bf1774616f8463b979b65687696b1e1d2a03783a/GA_FeatureSelector_LungCancer.ipynb), commit `bf17746`, cells 30, 33, 42, 46, 56 | The notebook combines training and test labels before supervised feature scoring. Executing its original `compute_PCC` on synthetic labels changes the score from 1 to 0 when only reserved labels change. | Demonstrates information flow. It does not estimate corrected article accuracy. |
| [MLX17](https://doi.org/10.1038/s41467-022-29283-8) | [Original script](https://github.com/ZhenyanZhang/ARG-global/blob/b3a25d6ca422f1e2d5f62baaf30fbc78cc18ce4d/Machine%20learning/Machine%20learning%20model%20building%20and%20assessing.py), commit `b3a25d6`, lines 45–60 | Executing the original statements with synthetic data calls `fit` once on all 200 rows. All 20 evaluation rows in each of ten folds were already seen during fitting. | Demonstrates the evaluation protocol in code. It does not reproduce a published accuracy. |
| [MLX02](https://doi.org/10.1038/s41467-024-46043-y) | [Official notebook](https://github.com/Yangzi-Chen2023/GC_NC-Res/blob/7f0711551af667095a9b1d010bac5f722c6eb4b9/GC_diagnosis_model/run.ipynb) and [discovery data](https://github.com/Yangzi-Chen2023/GC_NC-Res/blob/7f0711551af667095a9b1d010bac5f722c6eb4b9/GC_diagnosis_model/Data/discovery_set.xlsx), commit `7f07115`, cells 4–5 | Replaying the first 50 of 10,000 stratified splits finds all 142 final internal-test participants in earlier feature-selection training subsets. The separate `Xtest.xlsx` also overlaps all 142, but its membership differs from the notebook's final split. | The script does not rerun LASSO or estimate performance inflation. The external test of 95 patients remains separate. |

The generated output identifies the exact hashes and observations. A failing assertion signals that the pinned source or our reading needs review. Corrections or counterexamples are welcome through this repository's issues.

Technical questions were posted to the relevant code repositories: [feature selection](https://github.com/priyam-03/GA-Feature-Selector-Lung-Cancer/issues/1), [fold evaluation](https://github.com/ZhenyanZhang/ARG-global/issues/3), and [internal test selection](https://github.com/Yangzi-Chen2023/GC_NC-Res/issues/4). An open issue records a question, not agreement with the audit.
