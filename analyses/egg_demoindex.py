import pandas as pd
import matplotlib.pyplot as plt
from datetime import datetime
import matplotlib.ticker as ticker


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
ax1.plot(eggs_dem['year'], eggs_dem['price'], color='blue', marker='o', label='Price (USD)')
ax1.set_xlabel('Time (years)')
ax1.set_ylabel('Egg Price (USD)', color='black')
ax1.tick_params(axis='y', labelcolor='black')

# Create a twin y-axis for 'Democracy score'
ax2 = ax1.twinx()
ax2.plot(eggs_dem['year'], eggs_dem['score'], color='orange', marker='x', label='Democracy Index')
ax2.set_ylabel('Democracy Index', color='black')
ax2.tick_params(axis='y', labelcolor='black')

# Add a title and layout adjustment
plt.title('Egg Price vs Democracy Index (US) over Time')
fig.tight_layout()  # Adjust layout to prevent overlap

lines1, labels1 = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
plt.legend(lines1 + lines2, labels1 + labels2, loc='upper left')

ax1.xaxis.set_major_locator(ticker.MaxNLocator(integer=True))


plt.savefig("./graphs/eggPrice_demoindex.png")

print(eggs_dem.corr())




