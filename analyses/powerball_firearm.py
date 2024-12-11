import pandas as pd
import seaborn as sb
import matplotlib.pyplot as plt

def evenCount(ser):
    count = 0
    countList = []
    for lst in ser:
        for i in lst:
            if int(i)%2 == 0:
                count += 1
        countList.append(count)
        count = 0
    return countList

def oddCount(ser):
    count = 0
    countList = []
    for lst in ser:
        for i in lst:
            if int(i)%2 != 0:
                count += 1
        countList.append(count)
        count = 0
    return countList

flFirearm = pd.read_csv(r"maybeData\nics-firearm-background-checks.csv", usecols=['month', 'state', 'totals'])
powerball = pd.read_csv(r"maybeData\Lottery_Powerball_Winning_Numbers__Beginning_2010.csv", usecols=['Draw Date', "Winning Numbers", "Multiplier"])

flFirearm = flFirearm.query('state == "Florida"')
powerball['Winning Numbers'] = powerball['Winning Numbers'].str.split(pat=" ")
powerball["Draw Date"] = powerball['Draw Date'].str.slice(6) + '-' + powerball['Draw Date'].str.slice(0,2)
powerball.rename(columns={"Draw Date": "month"}, inplace=True)

powerball.sort_values('month')

merged = pd.merge(flFirearm, powerball, "inner", "month")

merged["Even count"] = evenCount(merged['Winning Numbers'])
merged["Odd count"] = oddCount(merged['Winning Numbers'])

corr = merged.corr(numeric_only=True)

sb.heatmap(corr, annot=True)
plt.title("Correlation")
plt.savefig(r'graphs\powerball_firearm_heatmap.png')
plt.show()
