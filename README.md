# Pente-game
Setup and Installation
Follow these steps to set up the environment and install all necessary dependencies.

1.1 Prerequisites
Python 3.8+

1.2 Installation Steps
Clone the Repository (if applicable) or navigate to the project folder:

Bash

cd PENTE-AI-PROJECT
Install Required Libraries: All necessary Python packages are listed in requirements.txt. Use pip to install them:

Bash

pip install -r requirements.txt
(This command installs pygame, numpy, matplotlib, and pandas.)

▶️ 2. Execution Instructions
The game is run via the main application file, main.py.

2.1 Starting the Game
Run the following command from the project's root directory:

Bash

python main.py
2.2 Game Modes
Upon launching, use the menu to select a game mode:

Player vs. Player (PVP): Classic two-player game.

Player vs. AI: Select your color and choose a difficulty level (which corresponds to the search depth).

⚙️ 3. AI Benchmarking and Analysis
This project includes internal benchmarking tools to analyze the performance of the Alpha-Beta Pruning algorithm (relevant for Section 6 of the report).

3.1 Live Data Logging
When playing against the AI, performance data is logged directly to the terminal:

Data Logged: Execution Time, Nodes Explored, and Search Depth.

Purpose: This data is used for quantitative analysis in the final report.

3.2 Generating Graphs and Tables
To reproduce the analysis tables and graphs used in the report:

Collect Data: Run the game and record the average time and nodes logged for Depths 1, 2, 3, and 4.

Update Script: Open analyze_results.py and replace the placeholder data with your collected average figures.

Run Analysis: Execute the analysis script to generate the visualizations and formatted tables:

Bash

python analyze_results.py