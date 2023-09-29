import matplotlib.pyplot as plt
import numpy as np

# Dataset names
datasets = ['CV 15 yue', 'CV 11 yue', 'CV 11 zh-HK', 'Guangzhou']

# CER Scores for Ventura
ventura_best = [10.525, 10.335, 9.831, 8.681]
ventura_closest = [5.999, 5.886, 7.028, 6.348]

# CER Scores for Sonoma
sonoma_best = [7.417, 7.381, 8.114, 7.409]
sonoma_closest = [5.869, 5.819, 6.625, 5.160]

# X-axis positions
x = np.arange(len(datasets))

# Bar width
width = 0.4

# Create the bar chart
fig, ax = plt.subplots()

rects1 = ax.bar(x - width/2, ventura_best, width, label='Ventura Top Predictions', color=(237/255, 72/255, 19/255))
rects2 = ax.bar(x + width/2, sonoma_best, width, label='Sonoma Top Predictions', color=(67/255, 130/255, 2/255))

rects3 = ax.bar(x - width/2, ventura_closest, width, label='Ventura Closest Predictions', color=(253/255, 166/255, 45/255))
rects4 = ax.bar(x + width/2, sonoma_closest, width, label='Sonoma Closest Predictions', color=(11/255, 182/255, 6/255))

# Add labels and title
ax.set_ylabel('CER Score (%)')
ax.set_title('CER of Cantonese ASR in Ventura vs Sonoma')
ax.set_xticks(x)
ax.set_xticklabels(datasets)
ax.legend(loc="lower right")

# Add numerical labels above bars
def add_labels(rects):
    for rect in rects:
        height = rect.get_height()
        ax.annotate(f'{height}',
                    xy=(rect.get_x() + rect.get_width() / 2, height),
                    xytext=(0, 3),  # 3 points vertical offset
                    textcoords="offset points",
                    ha='center', va='bottom')

add_labels(rects1)
add_labels(rects2)
add_labels(rects3)
add_labels(rects4)

plt.savefig('cer_comparison.png')

plt.show()
