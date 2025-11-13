# WCA Competition Round Simulator

Want to spice up your practice routine before your next competition? Use this app to "compete" against some of the greatest speedcubers of all time

## How to run this app on your computer?

### Prerequisites

- Python3
- customtkinter
- cubescrambler
- requests
- numpy
- pandas

You can install the necessary packages by running this command in your terminal:

`pip install customtkinter cubescrambler requests numpy pandas`

### Run in terminal

Simply ensure you're in the src/ directory and  run the following command in your terminal

`python3 app.py`

## App Instructions

1. For the cubers you wish to compete against, enter their WCA IDs, and select the event you'd like to practice
2. Click enter to start the round
3. A scramble should be generated, once you've done the scramble, enter your time. Other people's times should be displayed and players are ranked by their fastest single (for the first 4 solves)
4. By the fourth solve, competitors' BPA / WPA* will be displayed
5. After you're done with the average, you are ranked against other cubers and can choose to either restart the round with the same competitors, or go back to the start screen to change the event or the competitors

*BPA/WPA = Best Possible and Worst Possible Average of a particular competitor

## Notes

- Player's times are randomly generated via a normal distribution of their last official 98 (non-DNF) WCA times
- Every generated cuber has the same chance of getting a DNF (as of now is 2%) regardless of their DNF rate in competition
- Selecting a different event will clear the entered players (i.e., you will have to enter everybody's WCA IDs again)
- Mo3 hasn't been implemented for certain events
- FMC results are not proper

## Keyboard Shortcuts

| Key   | Action    |
|--------------- | --------------- |
| Enter   | Either enters the inputted WCA ID or your time   |
| +   | Starts the round from the start screen  |
| [ | Opens a CSV file to import players|
| ] | Saves the inputted players to a CSV file |
| C  | Goes back to the start screen from the round screen to change competitors|
| R | Restarts the round   |
| Up/Down Arrow | Changes the chosen event |
| - | View the stats (from the start screen)|

## Acknowledgements

This app relies on the WCA Rest API made by Robin Ingelbrecht for simulating player times.
