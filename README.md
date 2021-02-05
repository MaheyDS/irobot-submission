# iRobot-submission

Python based application for using spoonacular food-API

## Installation

Use the package manager [pip](https://pip.pypa.io/en/stable/) to install following packages.

```bash
pip install requests
pip install configparser
```

## Usage
Rename file sample.env to .env file, and enter your spoonacular API_KEY 
API_KEY=''

```python
python FreeFood.py
Enter comma seperated list of ingredients ex. apple,banana: apple
Do you like this recipe??, please enter yes or no: yes
Please find below the Shopping List to buy this item:
[
    {
        'aisleName': 'Spices and Seasonings',
        'estimatedCost': 43.3,
        'ingredientName': 'apple pie spice',
        'quantity': 2.0
    },
    {   'aisleName': 'Canned and Jarred',
        'estimatedCost': 37.22,
        'ingredientName': 'unsweetened applesauce',
        'quantity': 0.5
    }
]
```
## Security Approach
I have seperated API_KEY, and other configuration files just to make sure we can apply some encryption to the .env file or input the value during run-time in Pipeline

## Sample Runs
![Alt text](/c/Users/lenovo/Desktop/irobot-submission/sample-runs/Run_1.jpg?raw=true "SampleRun_Part1")
![Alt text](/c/Users/lenovo/Desktop/irobot-submission/sample-runs/Run2.jpg?raw=true "SampleRun_Part2")
