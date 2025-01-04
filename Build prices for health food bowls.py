#last updated 8/2/2023
import pandas as pd
import numpy as np
import itertools
import matplotlib.pyplot as plt
from scipy.stats import percentileofscore
from matplotlib.ticker import PercentFormatter
ingedient_costs = "Ingredient Costs.xlsx"
bowl_combinations_costs = "Bowls and Costs.xlsx"
#read bowls combo sheet. May want to add a second extra for when both avo and bacon are added
df = pd.read_excel(ingedient_costs)
combos = itertools.permutations(range(11), 5)
df2 = np.empty((0,2))
for i, combo in enumerate(combos):
    if combo[0] > 5 or combo[2] > 9 or combo[3] > 9 or combo[4] > 2:
        continue
    else: 
        base = df["Base"][combo[0]]
        protein = df["Protein"][combo[1]]
        side1 = df["Sides 1"][combo[2]]
        side2 = df["Sides 2"][combo[3]]
        extra = df["Extras"][combo[4]]
        base_cost = df["Base Cost"][combo[0]]
        protein_cost = df["Protein Cost"][combo[1]]
        side1_cost = df["Side Costs 1"][combo[2]]
        side2_cost = df["Side Costs 2"][combo[3]]
        extra_cost = df["Extras Costs"][combo[4]]
        df2 = np.append(df2, [[f"{base}, {protein}, {side1}, {side2}, {extra}", base_cost + protein_cost + side1_cost + side2_cost + extra_cost]], axis = 0)

df3 = pd.DataFrame(df2, dtype = df2.dtype)
df3.columns = ['Combo', 'Cost']
with pd.ExcelWriter(bowl_combinations_costs, mode = "w") as writer:
    df3.to_excel(writer, "Totals")


df4 = pd.read_excel(bowl_combinations_costs)
data = [["Max Cost", np.max(df4["Cost"])],
["Max Price", np.max(df4["Cost"])/.3],
["Min Cost", np.min(df4["Cost"])],
["Min Price", np.min(df4["Cost"])/.3],
["Average Cost", np.mean(df4["Cost"])],
["Average Price", np.mean(df4["Cost"])/.3],
["Median Cost", np.median(df4["Cost"])],
["Median Price", np.median(df4["Cost"])/.3],
["Standard Deviation Cost", np.std(df4["Cost"])],
["Standard Deviation Price", np.std(df4["Cost"])/.3],
["Price < $15.95, %", percentileofscore(df4["Cost"]/.3, 15.95)],
["Price < $16.50, %", percentileofscore(df4["Cost"]/.3, 16.50)],
["Price < $17.00, %", percentileofscore(df4["Cost"]/.3, 17.00)]]

stats = np.array(data)
df5 = pd.DataFrame(stats, columns= ["Statistic", "Result"])
with pd.ExcelWriter("Bowls Stats.xlsx", mode = "w") as writer:
    df5.to_excel(writer, "Statistics")

df4 = pd.read_excel(bowl_combinations_costs)

plt.style.use("seaborn")
fig, ax = plt.subplots()
ax.hist(df4["Cost"], bins=11, range=(2, 7.5), density=True, edgecolor="grey", linewidth=.75)
ax.set_title("Bowl Combinations")
ax.set_xlabel("Product Cost, $")
ax.set_ylabel("Possible Bowl Combos")
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.savefig("Bowls.png")

fig, ax = plt.subplots()
ax.hist(df4["Cost"]/.3, bins=18, range=(7, 25), density=True, edgecolor="grey", linewidth=.75)
ax.set_title(r"Bowl Combinations at 30% Food cost")
ax.set_xlabel("Recommended Price, $")
ax.set_ylabel("Possible Bowl Combos")
plt.gca().yaxis.set_major_formatter(PercentFormatter(1))
plt.savefig("Bowls Price.png")
