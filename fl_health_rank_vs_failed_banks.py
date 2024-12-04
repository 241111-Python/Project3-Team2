import pandas as pd
from datetime import datetime

flHealth = pd.read_csv("maybeData\County_Health_Rankings.csv", usecols=['County', 'Measure name', 'Raw value', 'Year span'])
banks = pd.read_csv(r"maybeData\failed_banklist.csv", usecols=['State', 'Closing Date'])

#filter data to be Florida specific, then drop unneeded columns/rows
flHealth = flHealth.query('County == "Florida"')
banks = banks.query('State == "FL"')
flHealth.drop('County', axis=1, inplace=True)
banks.drop('State', axis=1, inplace=True)
flHealth.dropna(inplace=True)
banks.dropna(inplace=True)

# matching names and formates
flHealth.rename(columns={"Year span":"Year"}, inplace=True)
banks.rename(columns={"Closing Date":"Year"}, inplace=True)

flHealth.loc[flHealth["Measure name"] == "Violent crime rate", "Year"] = flHealth["Year"].str.slice(5)
banks["Year"] = banks['Year'].str.slice(7)
banks.loc[banks["Year"].str.len() == 1, "Year"] = "0" + banks["Year"].str.slice()
banks["Year"] = "20" + banks['Year'].str.slice()
banks.sort_values('Year', inplace=True)

# The query method gets a little funky when given a two word variable, so we change this to be one word
flHealth.rename(columns={"Measure name":"Measure_name"}, inplace=True)


closed = banks.groupby('Year').size().reset_index(name="Banks closed")

merged = pd.merge(flHealth, closed, "inner", "Year")

vCrime = merged.query("Measure_name == 'Violent crime rate'")
unem = merged.query("Measure_name == 'Unemployment'")
unin = merged.query("Measure_name == 'Uninsured'")
std = merged.query("Measure_name == 'Sexually transmitted infections'")
inact = merged.query("Measure_name == 'Physical inactivity'")
obs = merged.query("Measure_name == 'Adult obesity'")

vCrime.drop(["Measure_name"],axis=1, inplace=True)
unem.drop(["Measure_name"],axis=1, inplace=True)
unin.drop(["Measure_name"],axis=1, inplace=True)
std.drop(["Measure_name"],axis=1, inplace=True)
inact.drop(["Measure_name"],axis=1, inplace=True)
obs.drop(["Measure_name"],axis=1, inplace=True)

# no fancy heat map because it is 10:30 pm and I am sleepy
print("\nViolent crime")
corr = vCrime.corr()
print(corr)

print("\nUnemployment")
corr = unem.corr()
print(corr)


print("\nUninsured")
corr = unin.corr()
print(corr)

print("\nSexually transmitted infections")
corr = std.corr()
print(corr)

print("\nPhysical inactivity")
corr = inact.corr()
print(corr)

print("\nAdult obesity")
corr = obs.corr()
print(corr)