from __future__ import annotations

import importlib.util
import sys
from pathlib import Path

import torch


PROJECT_ROOT = Path(__file__).resolve().parents[1]
EXPECTED_MODULES = [
    "numpy",
    "pandas",
    "sklearn",
    "skorch",
    "imblearn",
    "matplotlib",
    "seaborn",
    "jupyterlab",
    "nbformat",
    "reportlab",
]
EXPECTED_NOTEBOOKS = [
    PROJECT_ROOT / "notebooks" / "00_environment_and_pandas.ipynb",
    PROJECT_ROOT / "notebooks" / "01_regression_nyse.ipynb",
    PROJECT_ROOT / "notebooks" / "02_classification_maintenance.ipynb",
]


def main() -> None:
    missing_modules = [
        name for name in EXPECTED_MODULES if importlib.util.find_spec(name) is None
    ]
    missing_notebooks = [str(path) for path in EXPECTED_NOTEBOOKS if not path.exists()]

    print(f"Python  : {sys.version.split()[0]}")
    print(f"PyTorch : {torch.__version__}")
    print(f"Device  : {'cuda' if torch.cuda.is_available() else 'cpu'}")

    if missing_modules or missing_notebooks:
        raise SystemExit(
            f"Modules absents={missing_modules}; notebooks absents={missing_notebooks}"
        )

    print("Installation et structure : OK")


if __name__ == "__main__":
    main()
