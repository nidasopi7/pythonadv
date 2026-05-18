import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
df = pd.read_csv('avgIQpercountry.csv')

# Group by continent and calculate total Nobel Prizes per continent
nobel_prizes_by_continent = df.groupby('Continent')['Nobel Prices'].sum()

# Find the number of continents
no_of_continents = nobel_prizes_by_continent.count()

print(no_of_continents)  # Output: 8

# Creating a list of 8 colors, per each continent
colors = ['gold', 'lightcoral', 'yellow', 'thistle', 'orange', 'lightskyblue', 'aquamarine', 'burlywood']

# Plotting a pie chart
plt.figure(figsize=(10, 10))

# Plotting the pie chart using the colors list
nobel_prizes_by_continent.plot(kind='pie', colors=colors, autopct='%1.1f%%')

# Adding title and adjusting layout
plt.title('Distribution of Nobel Prizes by Continent')
# Equal aspect ratio ensures that pie is drawn as a circle.
plt.axis('equal')
# Remove the default y-label which can be 'Nobel Prizes'
plt.ylabel('')

# Adjust the layout to ensure everything fits without overlapping
plt.tight_layout()

# Display the plot
plt.show()