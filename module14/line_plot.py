import matplotlib.pyplot as plt
import pandas as pd

df = pd.read_csv("file1.csv")

avg_iq_by_continent = df.groupby('Continent')['Average IQ'].mean()


plt.figure(figsize=(10,6))

avg_iq_by_continent.plot(kind='line',marker='o',color='skyblue')

plt.title('Average IQ by Continent')
plt.xlabel('Continent')
plt.ylabel('Average IQ')

plt.grid(axis='both',linestyle='--',alpha=0.7)
plt.show()


