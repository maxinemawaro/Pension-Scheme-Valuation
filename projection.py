import pandas as pd
import numpy as np

folder = "C:/Users/Family/OneDrive - University of Leicester/Pension Project"
file = folder + "/members.xlsx"

ass = pd.read_excel(file, sheet_name="Assumptions")
A = dict(zip(ass["Assumption"], ass["Value"]))
print("Assumptions found:", list(A.keys()))

members = pd.read_excel(file, sheet_name="Members")
members = members[["MemberID", "Sex", "Status", "Age", "Salary", "Service", "Pension"]]
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

def survival(age, sex, n):
    a, b = gomp[sex]
    ages = age + np.arange(n)
    mu = a * np.exp(b * (ages + 0.5))
    return np.cumprod(np.exp(-mu))

def member_pv(row):
    age = int(row["Age"])
    n = max_age - age
    if n <= 0:
        return 0.0
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
    return float(np.sum(amount * paid * tpx * v))

members["Liability"] = members.apply(member_pv, axis=1)

print("\nLiability by status:")
print(members.groupby("Status")["Liability"].sum().round(0))

total = members["Liability"].sum()
print("\nTotal liability: {:,.0f}".format(total))
print("Assets:          {:,.0f}".format(assets))
print("Funding level:   {:.1%}".format(assets / total))

members.to_csv(folder + "/liabilities_python.csv", index=False)
print("\nSaved liabilities_python.csv")