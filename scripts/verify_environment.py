from __future__ import annotations

import importlib
import platform
import sys


REQUIRED_MODULES = {
    "torch": "PyTorch",
    "numpy": "NumPy",
    "pandas": "pandas",
    "sklearn": "scikit-learn",
    "skorch": "skorch",
    "imblearn": "imbalanced-learn",
    "matplotlib": "Matplotlib",
    "seaborn": "seaborn",
    "jupyterlab": "JupyterLab",
    "nbformat": "nbformat",
    "reportlab": "ReportLab",
}


def version_of(module_name: str) -> str:
    module = importlib.import_module(module_name)
    return str(getattr(module, "__version__", "version non exposée"))


def main() -> None:
    print(f"Python      : {sys.version.split()[0]}")
    print(f"Executable  : {sys.executable}")
    print(f"Système     : {platform.platform()}")

    missing: list[str] = []
    for module_name, display_name in REQUIRED_MODULES.items():
        try:
            print(f"{display_name:<18}: {version_of(module_name)}")
        except Exception as exc:  # diagnostic volontairement large
            missing.append(display_name)
            print(f"{display_name:<18}: ERREUR - {exc}")

    if missing:
        raise SystemExit(f"Dépendances manquantes : {', '.join(missing)}")

    import torch

    print(f"CUDA disponible : {torch.cuda.is_available()}")
    if torch.cuda.is_available():
        print(f"GPU             : {torch.cuda.get_device_name(0)}")
    else:
        print("Device retenu   : CPU")

    x = torch.tensor([[1.0, 2.0], [3.0, 4.0]])
    model = torch.nn.Linear(2, 1)
    output = model(x)
    assert output.shape == (2, 1)
    print("Test PyTorch     : OK")


if __name__ == "__main__":
    main()
