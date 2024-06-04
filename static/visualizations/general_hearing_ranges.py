import matplotlib.pyplot as plt

# Data: General hearing ranges in Hz
data = {
    'Category': ['Humans', 'General Mammals', 'Birds', 'Reptiles', 'Insects'],
    'Low Hz': [20, 40, 1000, 50, 100],
    'High Hz': [20000, 60000, 4000, 4000, 100000]
}

# Creating the plot
plt.figure(figsize=(12, 6))

# Plotting the hearing ranges
for i, category in enumerate(data['Category']):
    plt.plot([data['Low Hz'][i], data['High Hz'][i]], [category, category], marker='o')

# Adding labels and title
plt.xlabel('Frequency (Hz)')
plt.ylabel('Category')
plt.title('General Hearing Ranges of Humans and Various Animal Categories')
plt.xscale('log')
plt.grid(True, which="both", linestyle='--', linewidth=0.5)

# Annotate ranges
for i, category in enumerate(data['Category']):
    plt.text((data['Low Hz'][i] + data['High Hz'][i]) / 2, category, 
             f"{data['Low Hz'][i]} - {data['High Hz'][i]} Hz",
             va='center', ha='center', fontsize=10, color='black', backgroundcolor='white')

plt.show()
