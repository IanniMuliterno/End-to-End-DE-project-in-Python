# End-to-End Data Engineering Project in Python

This repository contains all the code and resources for an end-to-end data engineering project implemented in Python. The project focuses on handling, processing, and visualizing flight data using various Python tools and libraries.

## Repository Structure

The repository consists of several files, with `avstack.ipynb` and `app.py` being the core components:

- **`avstack.ipynb`**: This Jupyter notebook contains the code for fetching, processing, and analyzing flight data from the AviationStack API. It demonstrates data ingestion, cleaning, transformation, and preliminary data analysis.

- **`app.py`**: A Python Shiny application that allows users to interactively filter, query, and visualize flight data. It supports dynamic data visualization and can be used to generate insights about flight patterns, delays, and overall airline performance.

## Installation

To set up this project, you need to have Python installed on your machine (Python 3.6+ is recommended). Follow these steps to get started:

1. Clone the repository:
   ```bash
   git clone https://github.com/IanniMuliterno/End-to-End-DE-project-in-Python.git
   cd End-to-End-DE-project-in-Python

# Usage
To use the components of this repository, follow these instructions: 


Open the notebook using Jupyter Lab or Jupyter Notebook:
   ```bash
   jupyter notebook avstack.ipynb
   ```
Input your API key, in order to do that, you can add `environ['aviation_key'] = 'your-key'` right below the libraries import, like this:

```python
import requests
from datetime import datetime, timedelta
from os import environ
import pandas as pd
from sqlalchemy import create_engine
import matplotlib.pyplot as plt
import plotly.express as px
from sqlalchemy.engine.url import URL
from sqlalchemy_utils import database_exists, create_database, drop_database

environ['aviation_key'] = 'your-key'
api_key = environ.get('aviation_key')
#[ ... rest of the code]
```
After doing that, your key will be saved in the environment and you won't need to leave it exposed in the code. 

Run the cells sequentially to see how data is fetched, processed, and analyzed.

To start the Shiny application, run:
```bash
python app.py
```
Access the web interface to interact with the data visualization tools.

# Contributing
Contributions to this project are welcome! Please fork the repository and submit a pull request with your enhancements.
