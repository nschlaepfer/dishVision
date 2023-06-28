import matplotlib.pyplot as plt

# Create a new figure for the debugging window
fig, ax = plt.subplots()

# Initialize the text elements for the counters
washing_hands_text = ax.text(0.5, 0.7, '', transform=ax.transAxes, fontsize=15, ha='center')
washing_dishes_text = ax.text(0.5, 0.5, '', transform=ax.transAxes, fontsize=15, ha='center')
# Initialize the text elements for the counters
other_actions_text = ax.text(0.5, 0.3, '', transform=ax.transAxes, fontsize=15, ha='center')

# Initialize the bar chart
actions = ['Washing hands', 'Washing dishes', 'Other actions']
counters = [0, 0, 0]
bar_chart = ax.bar(actions, counters)

# Function to update the counters
def update_counters(washing_hands_counter, washing_dishes_counter, other_actions_counter):
    washing_hands_text.set_text(f'Washing hands: {washing_hands_counter}')
    washing_dishes_text.set_text(f'Washing dishes: {washing_dishes_counter}')
    other_actions_text.set_text(f'Other actions: {other_actions_counter}')
    
    # Update the bar chart
    counters[0] = washing_hands_counter
    counters[1] = washing_dishes_counter
    counters[2] = other_actions_counter
    for i, rect in enumerate(bar_chart):
        rect.set_height(counters[i])
    
    plt.draw()
    plt.pause(0.001)

# Display the debugging window
plt.show(block=False)
