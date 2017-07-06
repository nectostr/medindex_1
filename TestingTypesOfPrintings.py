import numpy as np
import matplotlib.pyplot as plt

# example data
x = np.arange(0.1, 4, 0.5)
print(type(x))

y = np.exp(-x)

# example error bar values that vary with x-position
error = 0.1 + 0.2 * x
print(type(error))
#fig, (ax0, ax1) = plt.subplots(nrows=2, sharex=True)
#plt.errorbar(x, y, yerr=error, fmt='-o')
#plt.set_title('variable, symmetric error')

# error bar values w/ different -/+ errors that
# also vary with the x-position
lower_error = 0.4 * error
upper_error = error
asymmetric_error = [lower_error, upper_error]

plt.errorbar(x, y, xerr=asymmetric_error, fmt='o')
#plt.set_title('variable, asymmetric error')
#plt.set_yscale('log')
plt.show()