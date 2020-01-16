import matplotlib.pyplot as plt
import numpy as np
import csv
import collections
import sys

csv.field_size_limit(sys.maxsize)

Datapoint  = collections.namedtuple("Datapoint", ["goal", "gs", "asz", "n_us"])
datapoints = []

#filename = "fake.err" # 'mathlib.err'
filename = "mathlib.err"

topk = 100

print("Reading from file")
with open(filename, "r", encoding="ISO-8859-1") as csv_file:
    reader = csv.reader(csv_file, delimiter=',')#, encoding="ISO-8859-1")
    first = True
    i = 0
    for row in reader:
        i += 1
        if first:
            first = False
            continue
        datapoints.append(Datapoint(goal=row[0], gs=int(row[1]), asz=int(row[2]), n_us=int(row[3])))

print("Num datapoints: ", len(datapoints))

print("\n\nTop-5 by goal string size:\n\n")
datapoints.sort(key=(lambda dp: - dp.gs))
for dp in datapoints[:5]:
    print(dp)

print("\n\nTop-5 by answer string size:\n\n")
datapoints.sort(key=(lambda dp: - dp.asz))
for dp in datapoints[:5]:
    print(dp)

print("\n\nTop-5 by # microseconds:\n\n")
datapoints.sort(key=(lambda dp: - dp.n_us))
for dp in datapoints[:5]:
    print(dp)

vec_us = np.zeros(topk)
vec_gs = np.zeros(topk)
for i, dp in enumerate(datapoints[:topk]):
    vec_us[i] = dp.n_us
    vec_gs[i] = dp.gs

print("\n# Microseconds:\n")
print("Mean: ", np.mean(vec_us))
print("Std: ",  np.std(vec_us))
print("Max: ",  np.amax(vec_us))

n_binss = [10, 20, 40]
fig, axs = plt.subplots(1, len(n_binss), sharey=False, tight_layout=True)

for ax, n_bins in zip(axs, n_binss):
    ax.hist(vec_us, bins=n_bins)

plt.show()
