# Final Project - Big Data Tools & Techniques
**Matt Austen**\
**Prof. Ganesh**\
**02 May 2024**

---
## Overview

blah

#### NOMINATE Scores

In political data analysis, Nominate scores, also known as NOMINATE (NOMINAl Three-step Estimation) scores, are a method used to estimate the ideological positions of legislators based on their voting behavior. These scores provide a quantitative measure of a legislator's political ideology along one or more dimensions.

Dimension 1 (D1): Dimension 1 of Nominate scores typically represents the left-right ideological spectrum or the economic dimension. A higher score on Dimension 1 indicates a more conservative or right-leaning position, while a lower score indicates a more liberal or left-leaning position. Legislators with similar Dimension 1 scores are considered to have similar ideological positions on economic issues.
Dimension 2 (D2): Dimension 2 of Nominate scores often represents the social or cultural dimension. It captures ideological differences that may not be fully captured by Dimension 1. A higher score on Dimension 2 may indicate a more socially conservative position, while a lower score may indicate a more socially liberal position. Legislators with similar Dimension 2 scores are considered to have similar ideological positions on social issues.
Nominate scores are typically calculated using roll call voting data, where legislators' votes on various bills are analyzed to determine patterns of agreement and disagreement. By estimating these scores, political scientists can quantitatively analyze ideological trends, party polarization, coalition formation, and legislative behavior over time.

Nominate scores have been widely used in political science research to study legislative behavior, party dynamics, and the ideological composition of political institutions. They provide valuable insights into the ideological positions of legislators and the dynamics of policymaking in representative democracies.

---
## Visualizations

### Data Preparation

`part0_DataPrep.ipynb`

### Part 1 - NOMINATE Scores Over Time

`python part1_ScatterPlot.py`

This script plots the NOMINATE scores of all members of Congress (both chambers) over time. A plot is generated for each Congress from the 1st in 1789 to the current in 2024. The color is determined by the average NOMINATE dimension 1 score of each member's respective party.

![output1](output/output1.mp4)

### Part 2 - Voting Probability Over Time

`python part2_LineGraph.py`

blah blah blah

![output2](output/output2.png)

### Part 3 - Probability Density Party Comparison

`python part3_PartyMapping.py`

blah blah blah

![output3](output/output3.png)

