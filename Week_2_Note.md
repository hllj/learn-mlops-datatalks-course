# Introduction to Experiment Tracking 

## Important concepts:

- ML Experiments: The process of building an ML Model

- Experiment run: each trial in an ML experiment

- Run artifact: Any file that is associated with an ML run.

- Experiment metadata


## What's experiment tracking:

- Source code

- Environment

- Data

- Model 

- Hyperparams

- Metrics

Tracking all the relevant information from an ML experiment.

## Why is experiment tracking so important ?

- Reproducibility

- Organization

- Optimization

Tracking experiments in speadsheet ? Good but not enough !!

- Error prone (Human manually edit)

- No standard format

- No visibility & Collaboration (Team working, how data changed, how hyperparams changed)

# Mlflow

## Definition: "An open source platform for the machine learning lifecycle"

[Official Mlflow documentation](mlflow.org)

## Features 

- Tracking

- Models 

- Model registry

- Projects 

## Tracking experiments with Mlflow

MLflow tracking modules allows you tu organize your experiments into runs, and to keep track of:

- Params

- Metrics

- Metadata

- Artifacts

- Models

Extra logs:

- Source code

- Version of code (git commit)

- Start and end time

- Author

## Mlflow note:

- Installation

```bash
pip install mlflow
```

- Setup for mlflow: 

	- Setup for backend-store-uri

	- Set tracking uri 

	- Set experiment with name

- Log at each information you want
