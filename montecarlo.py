import pandas as pd
import numpy as np

folder = "C:/Users/Family/OneDrive - University of Leicester/Pension Project"
file = folder + "/members.xlsx"

ass = pd.read_excel(file, sheet_name="Assumptions")
A = dict(zip(ass["Assumption"], ass["Value"]))

members = pd.read_excel(file, sheet_name="Members")
members = members[["MemberID", "Sex", "Status", "Age", "Salary", "Service"]]
members = members.dropna(subset=["Status"])

disc = A["Discount rate"]
sal_g = A["Salary growth"]
wd = A["Withdrawal rate"]
ret_age = int(A["Retirement age"])
accrual = A["Accrual rate"]
pen_inc = A["Pension increase"]
max_age = int(A["Maximum age"])
assets = A["Scheme assets (£)"]

gomp = {
    "M": (A["Gompertz a (male)"], A["Gompertz b (male)"]),
    "F": (A["Gompertz a (female)"], A["Gompertz b (female)"]),
}

N_RUNS = 1000
rng = np.random.default_rng(42)

prepared = []
for _, row in members.iterrows():
    age = int(row["Age"])
    n = max_age - age
    if n <= 0:
        continue
    t = np.arange(1, n + 1)
    a, b = gomp[row["Sex"]]
    mu = a * np.exp(b * (age + np.arange(n) + 0.5))
    q = 1 - np.exp(-mu)
    v = (1 + disc) ** (-t)

    if row["Status"] == "Active":
        yrs = max(ret_age - age, 0)
        final_salary = row["Salary"] * (1 + sal_g) ** yrs
        pension_at_ret = accrual * final_salary * row["Service"] * (1 - wd) ** yrs
        amount = pension_at_ret * (1 + pen_inc) ** np.maximum(t - yrs, 0)
    else:
        amount = accrual * row["Salary"] * row["Service"] * (1 + pen_inc) ** t

    paid = ((age + t) >= ret_age).astype(float)
    prepared.append((q, amount * paid * v))

totals = np.zeros(N_RUNS)
for run in range(N_RUNS):
    total = 0.0
    for q, pv_if_alive in prepared:
        deaths = rng.random(len(q)) < q
        if deaths.any():
            first_death = np.argmax(deaths)
            alive = np.arange(len(q)) < first_death
        else:
            alive = np.ones(len(q), dtype=bool)
        total += np.sum(pv_if_alive * alive)
    totals[run] = total

mean = totals.mean()
p5, p95 = np.percentile(totals, [5, 95])

print("Simulations:          {}".format(N_RUNS))
print("Mean liability:       {:,.0f}".format(mean))
print("Std deviation:        {:,.0f}".format(totals.std()))
print("5th percentile:       {:,.0f}".format(p5))
print("95th percentile:      {:,.0f}".format(p95))
print("Assets:               {:,.0f}".format(assets))
print("Chance of deficit:    {:.1%}".format((totals > assets).mean()))

pd.DataFrame({"Liability": totals}).to_csv(folder + "/montecarlo_results.csv", index=False)
print("\nSaved montecarlo_results.csv")