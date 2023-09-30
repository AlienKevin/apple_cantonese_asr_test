import matplotlib.pyplot as plt
import numpy as np

# Dataset names
services = ['macOS Sonoma', 'Google', 'Microsoft']

# CER Scores for Top Predictions and Closest Predictions
top_predictions_cer = [7.417, 11.392, 22.549]
closest_predictions_cer = [5.869, 5.718, 8.960]

# X-axis positions
x = np.arange(len(services))

# Bar width
width = 0.35

fig, ax = plt.subplots()

# Plotting the bars
rects1 = ax.bar(x - width/2, top_predictions_cer, width, label='Top Predictions CER Score')
rects2 = ax.bar(x + width/2, closest_predictions_cer, width, label='Closest Predictions CER Score')

# Add some text for labels, title and custom x-axis tick labels
ax.set_ylabel('CER Score (%)')
ax.set_title('Comparison of ASR Services on Common Voice 15 Yue Dataset')
ax.set_xticks(x)
ax.set_xticklabels(services)
ax.legend()

# Label with specially formatted floats
ax.bar_label(rects1, fmt='%.2f%%')
ax.bar_label(rects2, fmt='%.2f%%')

plt.show()
