import pandas as pd
import matplotlib.pyplot as plt

folder = "C:/Users/Family/OneDrive - University of Leicester/Pension Project"
d = pd.read_csv(folder + "/sensitivities.csv")
d = d[d["Scenario"] != "Base case"]

colours = ["red" if x > 0 else "green" for x in d["Change %"]]
plt.figure(figsize=(9, 5))
plt.barh(d["Scenario"], d["Change %"], color=colours)
plt.axvline(0, color="black", linewidth=1)
plt.xlabel("Change in liability vs base case (%)")
plt.title("Sensitivity of pension liability")
plt.tight_layout()
plt.savefig(folder + "/sensitivity_chart.png", dpi=150)
print("Saved sensitivity_chart.png")
