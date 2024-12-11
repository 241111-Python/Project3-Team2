import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime

print("Running pandas version", pd.__version__)
print(datetime.now())

eggs = pd.read_csv("./maybeData/eggs.csv")
eggs = eggs.rename(columns={'DATE': 'date', 'APU0000708111': 'price'})
eggs['date'] =  pd.to_datetime(eggs['date'])
eggs['year'] = eggs['date'].dt.year
print(eggs.head())

plt.plot(eggs['date'], eggs['price'])

plt.xticks(eggs['date'][::60], rotation=45)
plt.xlabel("date")
plt.ylabel("Average price (USD)")
plt.tight_layout()
plt.savefig('./graphs/eggPrice_time.png')
plt.clf()

###########################################################################

dem = pd.read_csv("./maybeData/democracy-index-eiu.csv")
dem_usa = dem[dem['Entity'] == 'United States']
dem_usa = dem_usa.rename(columns={'Year': 'year', 'Democracy score': 'score'})
dem_usa = dem_usa.drop(['Code', 'Entity'], axis=1)
# dem_usa = dem_usa.drop()
print(dem_usa.head())

# Aggregate eggs over years
eggs_agg = eggs.groupby(by='year').mean()
eggs_agg = eggs_agg.drop('date', axis=1)
print(eggs_agg.head())

eggs_dem = pd.merge(left=eggs_agg, right=dem_usa, how='inner', on='year')
print(eggs_dem.head())

fig, ax1 = plt.subplots()

# Plot 'price' on the primary y-axis
ax1.plot(eggs_dem['year'], eggs_dem['price'], color='blue', marker='o', label='Price')
ax1.set_xlabel('Year')
ax1.set_ylabel('Price', color='blue')
ax1.tick_params(axis='y', labelcolor='blue')

# Create a twin y-axis for 'Democracy score'
ax2 = ax1.twinx()
ax2.plot(eggs_dem['year'], eggs_dem['score'], color='green', marker='x', label='Democracy Score')
ax2.set_ylabel('Score', color='green')
ax2.tick_params(axis='y', labelcolor='green')

# Add a title and layout adjustment
plt.title('Price and Democracy Score by Year')
fig.tight_layout()  # Adjust layout to prevent overlap
plt.savefig("./graphs/eggPrice_demoindex.png")

print(eggs_dem.corr())




