import pandas as pd
from datetime import datetime

flHealth = pd.read_csv("maybeData\County_Health_Rankings.csv")
banks = pd.read_csv(r"maybeData\failed_banklist.csv")

# dropping unneeded columns/rows
banks.drop(["Cert", "Fund"], axis=1, inplace=True)
flHealth.drop(["State code", "County code", "Measure id", "Confidence Interval Lower Bound","Confidence Interval Upper Bound","Data Release Year","fipscode"],axis=1, inplace=True)
flHealth = flHealth.query('County == "Florida"')
banks = banks.query('State == "FL"')
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

flHealth.rename(columns={"Measure name":"Measure_name"}, inplace=True)


closed = banks.groupby('Year').size().reset_index(name="Banks closed")

merged = pd.merge(flHealth, closed, "inner", "Year")

vCrime = merged.query("Measure_name == 'Violent crime rate'")
unem = merged.query("Measure_name == 'Unemployment'")
unin = merged.query("Measure_name == 'Uninsured'")
std = merged.query("Measure_name == 'Sexually transmitted infections'")
inact = merged.query("Measure_name == 'Physical inactivity'")
obs = merged.query("Measure_name == 'Adult obesity'")

# dropping non number columns
vCrime.drop(["State","County","Measure_name","Numerator","Denominator"],axis=1, inplace=True)
unem.drop(["State","County","Measure_name","Numerator","Denominator"],axis=1, inplace=True)
unin.drop(["State","County","Measure_name","Numerator","Denominator"],axis=1, inplace=True)
std.drop(["State","County","Measure_name","Numerator","Denominator"],axis=1, inplace=True)
inact.drop(["State","County","Measure_name","Numerator","Denominator"],axis=1, inplace=True)
obs.drop(["State","County","Measure_name","Numerator","Denominator"],axis=1, inplace=True)

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