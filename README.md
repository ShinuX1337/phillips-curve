**For people who have the spreadsheet:**  
Use an online converter to convert the file into a .csv file.
Add it to your workspace with the `inflation_unemployment_GER.py` file (or add it with the absolute path.)

In the main file:  
`Line 9` Change 'Germany' to your desired country as written in the spreadsheet.

`Line 20` Adjust the years to your liking. 
*First number needs to be one year before your desired starting point. Otherwise the change in inflation rate can't be properly calculated*  
*Second number is not inclusive.*  
**Example:** Desired time frame is 1974 to 1995 -> Insert (1973, 1996)

IDE used: Visual Studio Code  
Python 3.12.8
