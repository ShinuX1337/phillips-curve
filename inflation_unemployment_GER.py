import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
import statsmodels.api as sm

data = pd.read_csv('Phillips Curve data 1220 updated.csv')

#Extract Germany
germany_data = data[data['Country Name'] == 'Germany']

#Omit irrelevant rows
unemployment_data = germany_data[germany_data['Series Name'] == 'Unemployment, total (% of total labor force) (national estimate)']
inflation_data = germany_data[germany_data['Series Name'] == 'Inflation, consumer prices (annual %)']

#Year -> numeric
unemployment_data = unemployment_data.rename(columns=lambda x: x.split(' ')[0] if '[YR' in x else x)
inflation_data = inflation_data.rename(columns=lambda x: x.split(' ')[0] if '[YR' in x else x)

#Get inflation/unemployment per year
year_columns = [str(year) for year in range(1999, 2020)] #keep 1999 for change in inflation rate from 1999 to 2000
unemployment_rate = unemployment_data[year_columns].iloc[0].astype(float)
inflation_rate = inflation_data[year_columns].iloc[0].astype(float)

#Setup dataframe
analysis_df = pd.DataFrame({
    "Year": [int(year) for year in year_columns],
    "Unemployment Rate (%)": unemployment_rate.values,
    "Inflation Rate (%)": inflation_rate.values
})

#Change in inflation rate
analysis_df["Change in Inflation (%)"] = analysis_df["Inflation Rate (%)"].diff()

#Exclude 1999
analysis_df = analysis_df[analysis_df["Year"] >= 2000]

#Bar chart for inflation rate per year in percetn
plt.figure(figsize=(10, 6))
plt.bar(analysis_df["Year"], analysis_df["Inflation Rate (%)"], color="skyblue", edgecolor="black")
plt.title("Inflation Rate in Germany (2000–2019) in percent per year")
plt.xlabel("Year")
plt.ylabel("Inflation Rate (%)")
plt.xticks(analysis_df["Year"], rotation=45)
plt.grid(axis='y', linestyle='--', linewidth=0.5)
plt.show()

#Prepare Phillips Curve plot
plt.figure(figsize=(8, 6))
x = analysis_df["Unemployment Rate (%)"].values.reshape(-1, 1)
y = analysis_df["Inflation Rate (%)"].values

#Add trend line
model = LinearRegression()
model.fit(x, y)
trendline = model.predict(x)

#Check for statistical significance
X_with_const = sm.add_constant(x)
ols_model = sm.OLS(y, X_with_const)  #Ordinary-Least-Squares regression
results = ols_model.fit()
print("\nPhillips Curve Regression Summary (Unemployment vs Inflation):")
print(results.summary())

#Plot Phillips Curve
plt.scatter(x, y, color="blue", label="Data Points")
plt.plot(x, trendline, color="red", label="Trend Line", linewidth=2)
plt.title("Phillips Curve: Unemployment vs. Inflation")
plt.xlabel("Unemployment Rate (%)")
plt.ylabel("Inflation Rate (%)")
plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
plt.axvline(0, color="gray", linestyle="--", linewidth=0.8)
plt.legend()
plt.show()

#Prepare modified Phillips Curve
plt.figure(figsize=(8, 6))
x_mod = analysis_df["Unemployment Rate (%)"].values.reshape(-1, 1)
y_mod = analysis_df["Change in Inflation (%)"].values

#Add trend line
model_mod = LinearRegression()
model_mod.fit(x_mod, y_mod)
trendline_mod = model_mod.predict(x_mod)

#Check for statistical significance
X_mod_with_const = sm.add_constant(x_mod)
ols_model_mod = sm.OLS(y_mod, X_mod_with_const)
results_mod = ols_model_mod.fit()
print("\nModified Phillips Curve Regression Summary (Unemployment vs Change in Inflation):")
print(results_mod.summary())

#Plot modified Phillips Curve
plt.scatter(x_mod, y_mod, color="blue", label="Data Points")
plt.plot(x_mod, trendline_mod, color="red", label="Trend Line", linewidth=2)
plt.title("Modified Phillips Curve: Unemployment vs. Change in Inflation")
plt.xlabel("Unemployment Rate (%)")
plt.ylabel("Change in Inflation (%)")
plt.axhline(0, color="gray", linestyle="--", linewidth=0.8)
plt.axvline(0, color="gray", linestyle="--", linewidth=0.8)
plt.legend()
plt.show()