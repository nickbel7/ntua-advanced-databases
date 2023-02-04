import matplotlib.pyplot as plt
import matplotlib.cm as cm
import numpy as np 
import pandas as pd

# Create a dictionary for the results of each query
with open ("./execution_time.txt") as f:
    lines = f.readlines()
    q_benchmarks = {}
    for line in lines:
        _, _, _, q_name, q_time = line.split()
        q_name = q_name.strip(':')
        if 'RDD' in q_name: 
            continue
        if q_name in q_benchmarks:
            q_benchmarks[q_name].append(float(q_time))
        else: 
            q_benchmarks[q_name] = [float(q_time)]

number_of_benchmarks = len(list(q_benchmarks)[0])
benchmarks = list(q_benchmarks.values())
benchmarks_transposed = []
for i in range(number_of_benchmarks):
    benchmarks_transposed.append([n[i] for n in benchmarks])

benchmarks_df = pd.DataFrame(
    index = q_benchmarks.keys(),
)
for i in range(number_of_benchmarks):
    benchmarks_df[f'{i+1} Workers'] = benchmarks_transposed[i]

ax = benchmarks_df.plot.bar(color=['tab:orange', 'tab:purple'])
plt.title('Execution Time for DataFrame Queries')
filename = './graphs.pdf'
plt.savefig(filename)