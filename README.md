
# Solution:

Please make sure to use python 3.11

To start: source setup.sh will set up the python requirements.
Task 1: jupyter notebook - for score analysis, ran src/notebook_score_analyzer.ipynb
Task 2: run_task2_tests.sh will run the tests for the Ads, Ad, and Reimburesement classes
Task 3: python src/data_analysis.py

to run the Task 3 data analysis, 

# Instructions

- Please submit all your code, output, and charts or visualization.
- Ideally use a code Notebook, e.g. Jupyter, to capture all above, except for the demo app.
- You may choose to submit plain .py files or share a code repo.
- If you have questions about the tasks, please make best assumptions and move ahead.
- Please complete the exercise in two (2) days. You may want to budget two evenings to complete
the exercise and submit on the next Morning.
-- E.g. If you received the coding exercise on a Monday, please submit your completed
exercise on Wednesday morning.

## Task 1 - Data Manipulation Basics
Suppose you have a data frame of two columns, score_1 and score_2, as the probability of two different events, respectively. Please complete the following.

1. Create a new column in the data frame called highlighted, which is a Boolean value representing whether a record passes the following logic check:
- Both columns are below 0.35, OR
- score_1 is below 0.20 and score_2 is below 0.90, OR
- score_1 is below 0.15 and score_2 is below 0.80

2. Create a categorical column called risk_1_group, which is based on score_1 values, as following:

| score_1 | score1_group |
| ------- | ------------ |
| x < 0.10 | 'Very Low' |
| 0.10 <= x < 0.30 | 'Medium' |
| 0.30 <= x < 0.80 | 'High' |
| x >= 0.80| 'Very High' |


