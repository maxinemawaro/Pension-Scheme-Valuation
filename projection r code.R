# Set the working folder
setwd("C:/Users/Family/OneDrive - University of Leicester/Pension Project")

# Read the data
mort <- read.csv("mortality.csv")

names(mort)
head(mort)
names(mort) <- c("age", "mx_male", "mx_female")
mort <- na.omit(mort)
str(mort)

# Fit Gompertz for males: log(mx) = log(a) + b * age
fit_m <- lm(log(mx_male) ~ age, data = mort)
fit_f <- lm(log(mx_female) ~ age, data = mort)

# Get the parameters
a_m <- exp(coef(fit_m)[1]); b_m <- coef(fit_m)[2]
a_f <- exp(coef(fit_f)[1]); b_f <- coef(fit_f)[2]

print(c(a_m = a_m, b_m = b_m))
print(c(a_f = a_f, b_f = b_f))

# Plot real vs fitted for males
plot(mort$age, log(mort$mx_male), pch = 16, col = "blue",
     xlab = "Age", ylab = "log(mx)", main = "Males: Real vs Gompertz Fit")
lines(mort$age, predict(fit_m), col = "red", lwd = 2)
legend("topleft", legend = c("ONS data", "Gompertz fit"),
       col = c("blue", "red"), pch = c(16, NA), lty = c(NA, 1))

plot(mort$age, log(mort$mx_female), pch = 16, col = "blue",
     xlab = "Age", ylab = "log(mx)", main = "Females: Real vs Gompertz Fit")
lines(mort$age, predict(fit_f), col = "red", lwd = 2)
legend("topleft", legend = c("ONS data", "Gompertz fit"),
       col = c("blue", "red"), pch = c(16, NA), lty = c(NA, 1))