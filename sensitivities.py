import pandas as pd
import numpy as np

folder = "C:/Users/Family/OneDrive - University of Leicester/Pension Project"
file = folder + "/members.xlsx"

ass = pd.read_excel(file, sheet_name="Assumptions")
A = dict(zip(ass["Assumption"], ass["Value"]))

members = pd.read_excel(file, sheet_name="Members")
members = members[["MemberID", "Sex", "Status", "Age", "Salary", "Service"]]
members = members.dropna(subset=["Status"])

ret_age = int(A["Retirement age"])
accrual = A["Accrual rate"]
pen_inc = A["Pension increase"]
max_age = int(A["Maximum age"])
assets = A["Scheme assets (£)"]
wd = A["Withdrawal rate"]

gomp = {
    "M": (A["Gompertz a (male)"], A["Gompertz b (male)"]),
    "F": (A["Gompertz a (female)"], A["Gompertz b (female)"]),
}

def liability(disc, sal_g, mort_mult=1.0):
    def survival(age, sex, n):
        a, b = gomp[sex]
        ages = age + np.arange(n)
        mu = mort_mult * a * np.exp(b * (ages + 0.5))
        return np.cumprod(np.exp(-mu))

    total = 0.0
    for _, row in members.iterrows():
        age = int(row["Age"])
        n = max_age - age
        if n <= 0:
            continue
        t = np.arange(1, n + 1)
        tpx = survival(age, row["Sex"], n)
        v = (1 + disc) ** (-t)

        if row["Status"] == "Active":
            yrs = max(ret_age - age, 0)
            final_salary = row["Salary"] * (1 + sal_g) ** yrs
            pension_at_ret = accrual * final_salary * row["Service"] * (1 - wd) ** yrs
            amount = pension_at_ret * (1 + pen_inc) ** np.maximum(t - yrs, 0)
        else:
            amount = accrual * row["Salary"] * row["Service"] * (1 + pen_inc) ** t

        paid = (age + t) >= ret_age
        total += float(np.sum(amount * paid * tpx * v))
    return total

base_disc = A["Discount rate"]
base_sal = A["Salary growth"]

scenarios = [
    ("Base case", base_disc, base_sal, 1.0),
    ("Discount rate -1%", base_disc - 0.01, base_sal, 1.0),
    ("Discount rate +1%", base_disc + 0.01, base_sal, 1.0),
    ("Mortality -10% (live longer)", base_disc, base_sal, 0.9),
    ("Mortality +10% (die sooner)", base_disc, base_sal, 1.1),
    ("Salary growth -1%", base_disc, base_sal - 0.01, 1.0),
    ("Salary growth +1%", base_disc, base_sal + 0.01, 1.0),
]

base = liability(base_disc, base_sal, 1.0)
rows = []
for name, d, s, m in scenarios:
    L = liability(d, s, m)
    rows.append({
        "Scenario": name,
        "Liability": round(L),
        "Change vs base": round(L - base),
        "Change %": round(100 * (L / base - 1), 1),
        "Funding level %": round(100 * assets / L, 1),
    })

result = pd.DataFrame(rows)
print(result.to_string(index=False))
result.to_csv(folder + "/sensitivities.csv", index=False)
print("\nSaved sensitivities.csv")
