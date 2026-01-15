import os
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO, format='[%(asctime)s]: %(message)s:')

list_of_files = [
    "src",
    "test",
    "src/app.py",
    "src/main.py",
    "src/constants.py",
    "src/api",
    "src/utils",
    "src/api/schemas",
    "src/api/Namespaces",   # fixed typo
    "src/business_logic",
    "src/api/middlewares",
    "src/pipelines/feature_engineering.py",
    "src/pipelines/training_pipeline.py",
    "src/pipelines/inference_pipeline.py",
    "src/pipelines/evaluation_pipeline.py",
    "src/ML_Models/ensemble",
    "src/ML_Models/autoencoder",
    "src/ML_Models/registry.py",
    "src/monitoring/data_drift.py",
    "src/monitoring/model_drift.py",
    "src/monitoring/metrics.py",
    "ci_cd",
    "config/config.properties",
    "requirements.txt",
    "Research/trials.ipynb"
]

for path in list_of_files:
    path = Path(path)

    # If path has a file suffix → treat as file
    if path.suffix:
        os.makedirs(path.parent, exist_ok=True)

        if not path.exists():
            path.touch()
            logging.info(f"Created file: {path}")
        else:
            logging.info(f"File already exists: {path}")

    # Otherwise treat as directory
    else:
        os.makedirs(path, exist_ok=True)
        logging.info(f"Created directory: {path}")
