import pandas as pd
import matplotlib.pyplot as plt

folder = "C:/Users/Family/OneDrive - University of Leicester/Pension Project"
d = pd.read_csv(folder + "/montecarlo_results.csv")
x = d["Liability"] / 1e6

assets = 9.5
p5 = x.quantile(0.05)
p95 = x.quantile(0.95)

plt.figure(figsize=(9, 5))
plt.hist(x, bins=30, color="steelblue", edgecolor="white")
plt.axvline(assets, color="red", linewidth=2, label="Assets (£9.5m)")
plt.axvline(p5, color="grey", linestyle="--", label="5th percentile")
plt.axvline(p95, color="grey", linestyle="--", label="95th percentile")
plt.xlabel("Total liability (£m)")
plt.ylabel("Number of simulations")
plt.title("Monte Carlo: distribution of pension liability (1,000 runs)")
plt.legend()
plt.tight_layout()
plt.savefig(folder + "/montecarlo_histogram.png", dpi=150)
print("Saved montecarlo_histogram.png")