#!/usr/bin/env python3
"""Three bounded checks against hash-verified, public research code."""
from __future__ import annotations

import argparse
import ast
import contextlib
import hashlib
import io
import json
from pathlib import Path
from types import SimpleNamespace
from urllib.parse import quote
from urllib.request import urlopen

import numpy as np
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedShuffleSplit


BASE = Path(__file__).resolve().parent
CACHE = BASE / ".cache"
SOURCES = {
    "ga_notebook": (
        "priyam-03/GA-Feature-Selector-Lung-Cancer",
        "bf1774616f8463b979b65687696b1e1d2a03783a",
        "GA_FeatureSelector_LungCancer.ipynb",
        "aac9eed278d1f47322d8b8643591f313ac58cdd9195b5492b7971b951f2ad782",
    ),
    "arg_script": (
        "ZhenyanZhang/ARG-global",
        "b3a25d6ca422f1e2d5f62baaf30fbc78cc18ce4d",
        "Machine learning/Machine learning model building and assessing.py",
        "d72d1d762cb90b096f83071591934cc561c980df36030553c8ed50c51e5ddece",
    ),
    "gastric_notebook": (
        "Yangzi-Chen2023/GC_NC-Res",
        "7f0711551af667095a9b1d010bac5f722c6eb4b9",
        "GC_diagnosis_model/run.ipynb",
        "80a43d2d50a97513d9750956b9f22417669d75e7411acb9aa6ac1f859dfbff68",
    ),
    "gastric_discovery": (
        "Yangzi-Chen2023/GC_NC-Res",
        "7f0711551af667095a9b1d010bac5f722c6eb4b9",
        "GC_diagnosis_model/Data/discovery_set.xlsx",
        "38a6567c60da3bda1855d11b650e97a10419664a29c436af4cf17bb716d3aff8",
    ),
    "gastric_test": (
        "Yangzi-Chen2023/GC_NC-Res",
        "7f0711551af667095a9b1d010bac5f722c6eb4b9",
        "GC_diagnosis_model/Data/Xtest.xlsx",
        "4b387d58a364aeb67416fca0702ca773fbe3c70d0403811370164fb220900962",
    ),
}


def source(key: str) -> Path:
    repo, commit, path, expected = SOURCES[key]
    target = CACHE / (key + Path(path).suffix)
    if not target.exists():
        CACHE.mkdir(exist_ok=True)
        url = f"https://raw.githubusercontent.com/{repo}/{commit}/{quote(path)}"
        with urlopen(url, timeout=30) as response:
            data = response.read()
        if hashlib.sha256(data).hexdigest() != expected:
            raise ValueError(f"SHA256 mismatch for {key}")
        target.write_bytes(data)
    actual = hashlib.sha256(target.read_bytes()).hexdigest()
    if actual != expected:
        raise ValueError(f"SHA256 mismatch for cached {key}")
    return target


def ga() -> dict:
    notebook = json.loads(source("ga_notebook").read_text())
    cells = ["".join(cell.get("source", [])) for cell in notebook["cells"]]
    assert "pd.concat([predictions_df,test_predictions_df])" in cells[30]
    assert "np.append(y_all,y_test)" in cells[33]
    assert "f_regression(X, yy)" in cells[42]
    assert "train_test_split" in cells[56]
    tree = ast.parse(cells[46])
    fn = next(n for n in ast.walk(tree) if isinstance(n, ast.FunctionDef) and n.name == "compute_PCC")
    namespace = {"np": np}
    exec(compile(ast.fix_missing_locations(ast.Module(body=[fn], type_ignores=[])), "original_compute_PCC", "exec"), namespace)
    x = np.array([0, 0, 1, 1, 0, 1, 0, 1.], dtype=float)
    y = x.copy()
    changed = y.copy()
    changed[4:] = 1 - changed[4:]
    initial = float(namespace["compute_PCC"](None, x, y))
    altered = float(namespace["compute_PCC"](None, x, changed))
    assert np.array_equal(y[:4], changed[:4]) and initial == 1 and altered == 0
    return {"case": "s41598-025-86362-8", "source_sha256": SOURCES["ga_notebook"][3],
            "training_labels_unchanged": True, "score_before": initial, "score_after_reserved_labels_change": altered,
            "limit": "Synthetic mechanism only; corrected published accuracy was not estimated."}


def arg() -> dict:
    script = source("arg_script")
    tree = ast.parse(script.read_text())
    source_text = script.read_text()
    assert source_text.index("forest.fit(x,y)") < source_text.index("for i in range(k):")
    rng = np.random.default_rng(443)
    x = rng.normal(size=(200, 18))
    x[:, 0] = np.arange(200)
    y = rng.integers(1, 6, 200)
    toy = pd.DataFrame(np.c_[x, y])
    fits = []

    class AuditedForest(RandomForestClassifier):
        def fit(self, X, y, *args, **kwargs):
            fits.append({"rows": len(X), "ids": set(X[:, 0])})
            return super().fit(X, y, *args, **kwargs)

    tree.body = [node for node in tree.body if not isinstance(node, (ast.Import, ast.ImportFrom))]
    namespace = {"np": np, "pd": SimpleNamespace(read_excel=lambda _: toy.copy()),
                 "mpl": SimpleNamespace(rcParams={}), "joblib": SimpleNamespace(dump=lambda *_: None),
                 "RandomForestClassifier": AuditedForest}
    np.random.seed(190)
    with contextlib.redirect_stdout(io.StringIO()):
        exec(compile(tree, str(script), "exec"), namespace)
    data = namespace["Data"]
    fold_size = namespace["num_val_sample"]
    overlap = [len(set(data[i * fold_size:(i + 1) * fold_size, 0]) & fits[0]["ids"])
               for i in range(namespace["k"])]
    assert len(fits) == 1 and fits[0]["rows"] == 200 and overlap == [20] * 10
    return {"case": "MLX17", "source_sha256": SOURCES["arg_script"][3],
            "original_fit_calls": len(fits), "fit_rows": fits[0]["rows"],
            "test_rows_seen_during_fit_per_fold": overlap,
            "limit": "Synthetic data; no published accuracy is reproduced by this check."}


def gastric() -> dict:
    notebook = json.loads(source("gastric_notebook").read_text())
    cells = ["".join(cell.get("source", [])) for cell in notebook["cells"]]
    assert "for i in range(0,10000):" in cells[4]
    assert "sel.fit(Xtrain, ytrain)" in cells[4]
    assert "random_state=i" in cells[4]
    # The final iteration of range(0, 10000) leaves seed 9999 in Xtest.
    assert "model.fit(Xtrain[:,Counts_metas" in cells[5]
    discovery = pd.read_excel(source("gastric_discovery"), index_col=0)
    original_test = pd.read_excel(source("gastric_test"), index_col=0)
    batches = [discovery[discovery["batch"] == f"batch{i}"].reset_index(drop=True)
               for i in (1, 2, 3)]

    def split_ids(seed: int) -> tuple[set[str], set[str]]:
        train, test = set(), set()
        splitter = StratifiedShuffleSplit(n_splits=1, test_size=.33, random_state=seed)
        for batch in batches:
            ti, vi = next(splitter.split(batch, batch["type"]))
            train.update(batch.iloc[ti].sample_id.astype(str))
            test.update(batch.iloc[vi].sample_id.astype(str))
        return train, test

    _, final_test = split_ids(9999)
    seen = set()
    for seed in range(50):
        seen.update(split_ids(seed)[0])
    file_test = set(original_test.sample_id.astype(str))
    overlap = len(final_test & seen)
    file_overlap = len(file_test & seen)
    assert len(discovery) == 426 and len(final_test) == 142
    assert len(file_test) == 142 and overlap == 142 and file_overlap == 142
    return {"case": "MLX02", "notebook_sha256": SOURCES["gastric_notebook"][3],
            "discovery_rows": len(discovery), "final_internal_test_rows": len(final_test),
            "test_ids_in_prior_selection_training": overlap, "selection_rounds_checked": 50,
            "Xtest_file_ids_in_prior_selection_training": file_overlap,
            "Xtest_file_matches_final_loop_split": final_test == file_test,
            "limit": "Checks participant reuse, not 10,000 LASSO fits or performance inflation. Xtest file differs from the final notebook split. External test remains separate."}


def main() -> None:
    cases = {"ga": ga, "arg": arg, "gastric": gastric}
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("case", choices=[*cases, "all"])
    args = parser.parse_args()
    result = {name: fn() for name, fn in cases.items() if args.case in (name, "all")}
    print(json.dumps(result, ensure_ascii=False, indent=2))


if __name__ == "__main__":
    main()
