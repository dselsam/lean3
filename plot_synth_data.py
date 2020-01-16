import matplotlib.pyplot as plt
import numpy as np
import csv
import collections
import sys

csv.field_size_limit(sys.maxsize)

Datapoint  = collections.namedtuple("Datapoint", ["goal", "gs", "n_ms", "n_ls", "asz"])
datapoints = []

#filename = "fake.err" # 'mathlib.err'
filename = "mathlib.err"

topk = 100

print("Reading from file")
with open(filename, 'r') as csv_file:
    reader = csv.reader(csv_file, delimiter=',')
    first = True
    for row in reader:
        if first:
            first = False
            continue
        datapoints.append(Datapoint(goal=row[0][:1000], gs=len(row[0]), n_ms=int(row[1]), n_ls=int(row[2]), asz=int(row[3])))

print("Num datapoints: ", len(datapoints))

print("Top-50 by goal string size:")
datapoints.sort(key=(lambda dp: - dp.gs))
for dp in datapoints[:50]:
    print(dp)

print("Top-50 by answer string size:")
datapoints.sort(key=(lambda dp: - dp.asz))
for dp in datapoints[:50]:
    print(dp)

print("Top-50 by number of milliseconds:")
datapoints.sort(key=(lambda dp: - dp.n_ms))
for dp in datapoints[:50]:
    print(dp)

vec_ms = np.zeros(topk)
vec_gs = np.zeros(topk)
for i, dp in enumerate(datapoints[:topk]):
    vec_ms[i] = dp.n_ms
    vec_gs[i] = dp.gs

print("Mean: ", np.mean(vec_ms))
print("Std: ",  np.std(vec_ms))
print("Max: ",  np.amax(vec_ms))

n_binss = [10, 20, 40]
fig, axs = plt.subplots(1, len(n_binss), sharey=False, tight_layout=True)

for ax, n_bins in zip(axs, n_binss):
    ax.hist(vec_ms, bins=n_bins)

plt.show()
