# Pythia Assignment

## Description

This project consists of several Jupyter notebooks, each corresponding to a specific part of the assignment. Please follow the order indicated by the numbers in the notebook filenames. All notebooks are located in the "project_code" folder.

### 1. Notebook: '0_Part_1.ipynb'
**Objective**: Addresses Part I of the assignment: *"EXPLORING THE FIRST SEASON"*.

### 2. Notebook: '1_Part_2_players_feature_engineering.ipynb'
**Objective**: Supports Part II of the assignment: *"PREDICTING THE SECOND SEASON"*.

- This notebook performs feature engineering and generates two Parquet files:
  - 'goalkeeper_games.pq'
  - 'goalkeeper_teams.pq'
- These files are saved in the 'data' folder and will be used in subsequent notebooks.

### 3. Notebook: '2_Part_2_prediction_model.ipynb'
**Objective**: Completes Part II of the assignment: *"PREDICTING THE SECOND SEASON"*.

- Implements a prediction model to produce a probability distribution for each team's ranking in Season 2.
- Outputs:
  - A JSON file, 'predicted_positions.json', saved in the 'data' folder.
  - Probability distribution plots, saved in the 'plots_part_two' folder.

### 4. Notebook: '3_Part_3_data_exploration.ipynb'
**Objective**: Answers Part III of the assignment: *"ANYTHING ELSE?"*.

- Outputs two figures saved in the 'plots_part_three' folder.

## Installation

Run the following command to install the required dependencies:
'''bash
pip install -r requirements.txt
