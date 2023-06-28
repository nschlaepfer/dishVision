import matplotlib.pyplot as plt

# Create a new figure for the debugging window
fig, ax = plt.subplots()

# Initialize the text elements for the counters
washing_hands_text = ax.text(0.5, 0.6, '', transform=ax.transAxes, fontsize=15, ha='center')
washing_dishes_text = ax.text(0.5, 0.4, '', transform=ax.transAxes, fontsize=15, ha='center')

# Function to update the counters
def update_counters(washing_hands_counter, washing_dishes_counter):
    washing_hands_text.set_text(f'Washing hands: {washing_hands_counter}')
    washing_dishes_text.set_text(f'Washing dishes: {washing_dishes_counter}')
    plt.draw()
    plt.pause(0.001)

# Display the debugging window
plt.show(block=False)
