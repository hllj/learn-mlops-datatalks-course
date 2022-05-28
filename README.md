# MLOps Learning Project

This is a project I want to create a techstack for MLOps using a toy dataset.

## Dataset: 
	
We will use an toy dataset for this project - [NY Taxi trips dataset](https://www1.nyc.gov/site/tlc/about/tlc-trip-record-data.page)

## Techstack:

- Experiment Tracking: MLFlow

- Orchestration and ML Pipeline: Prefect, Kubeflow

- Model Deployment: Kinesis/SQS + AWS Lambda

- Model Monitoring

## Problem: 

NY Taxi trips dataset:

Input: Information of a taxi drive

Output: Predict the duration of if the driver is going to be tipped or not.

Goal: Predict the duration of a taxi drive, build an API for driver / customer.

## Design:

NY Taxi trips dataset -> Model -> API

Taxi Driver / Customer -> API -> Duration of taxi drive
