# Intelligent Indoor Air Quality Monitoring and Controlling using Q-Learning

## Overview

This project is an intelligent indoor air quality monitoring and controlling system that analyzes air-quality parameters and provides an air quality assessment, IAQ score, and recommended action using a Q-Learning based approach.

## Features

- Monitors indoor air quality parameters
- Calculates an Indoor Air Quality (IAQ) score
- Classifies air quality as Good, Moderate, Poor, or Very Poor
- Provides recommended actions such as Fan, Ventilation, or Air Purifier
- Flask-based web application
- Interactive web interface for entering air-quality parameters

## Technologies Used

- Python
- Flask
- Pandas
- NumPy
- HTML
- CSS
- JavaScript
- Q-Learning
- Excel Dataset

## Parameters

The system accepts:

- CO
- C6H6
- NOx
- NO2
- Temperature
- Relative Humidity
- Absolute Humidity

## Project Structure

```text
intelligent-indoor-air-quality-monitoring/
│
├── app.py
├── AirQualityUCI.xlsx
└── templates/
    └── index.html
