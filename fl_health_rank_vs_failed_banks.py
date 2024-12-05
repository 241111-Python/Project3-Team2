import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

flHealth = pd.read_csv("maybeData\County_Health_Rankings.csv", usecols=['County', 'Measure name', 'Raw value', 'Year span'])
banks = pd.read_csv(r"maybeData\failed_banklist.csv", usecols=['State', 'Closing Date'])

#filter data to be Florida specific, then drop unneeded columns/rows
flHealth = flHealth.query('County == "Florida"')
banks = banks.query('State == "FL"')
flHealth.drop('County', axis=1, inplace=True)
banks.drop('State', axis=1, inplace=True)

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

merged = pd.merge(flHealth, closed, "inner", "Year").sort_values("Banks closed")

vCrime = merged.query("Measure_name == 'Violent crime rate'")
unem = merged.query("Measure_name == 'Unemployment'")
unin = merged.query("Measure_name == 'Uninsured'")
std = merged.query("Measure_name == 'Sexually transmitted infections'")
inact = merged.query("Measure_name == 'Physical inactivity'")
obs = merged.query("Measure_name == 'Adult obesity'")

a = plt.plot(vCrime['Banks closed'],vCrime['Raw value'],)
b = plt.plot(unem['Banks closed'],unem['Raw value'])
c = plt.plot(unin['Banks closed'],unin['Raw value'])
d = plt.plot(std['Banks closed'],std['Raw value'])
e = plt.plot(inact['Banks closed'],inact['Raw value'])
f = plt.plot(obs['Banks closed'],obs['Raw value'])
plt.xlabel("Banks Closed")
plt.ylabel("Raw Value")
plt.savefig('plot.png')
plt.close()

sb.heatmap(vCrime.corr(numeric_only=True), annot=True)
plt.title("Violent Crime")
plt.savefig("violentCrime.png")
plt.close()

sb.heatmap(unem.corr(numeric_only=True), annot=True)
plt.title("Unemployment")
plt.savefig("unemployement.png")
plt.close()

sb.heatmap(unin.corr(numeric_only=True), annot=True)
plt.title("Uninsured")
plt.savefig("uninsured.png")
plt.close()

sb.heatmap(std.corr(numeric_only=True), annot=True)
plt.title("Sexually Transmitted Diseases")
plt.savefig("std.png")
plt.close()

sb.heatmap(inact.corr(numeric_only=True), annot=True)
plt.title("Physical Inactivity")
plt.savefig("physicalInactivity.png")
plt.close()

sb.heatmap(obs.corr(numeric_only=True), annot=True)
plt.title("Adult Obesity")
plt.savefig("adultObesity.png")
plt.close()
