import numpy as np
import matplotlib.pyplot as plt


def plot1(data , count) :
    players = list(data.keys())
    names = [data[player]['name'] for player in data]
    zeros = [data[player]['zero'] for player in players]
    singles = [data[player]['single'] for player in players]
    fig , ax = plt.subplots()
    width = 0.4
    ind = np.arange(len(names))

    # Change bar colors to skyblue and salmon
    ax.bar(ind - width / 2 , zeros , width , label=f'Number of both attack missed in past {count} wars' , color='skyblue')
    ax.bar(ind + width / 2 , singles , width , label=f'Number of Single attack missed in past {count} wars' , color='salmon')

    ax.set_ylabel('Number of missed attacks')
    ax.set_title(f'Out of past {count} FWA wars')
    ax.set_xticks(ind)
    ax.set_xticklabels(names)
    ax.legend()
    plt.xticks(rotation=90 , ha='right')
    # Add value at the top of each bar inside the bar
    for i in range(len(ind)) :
        ax.text(ind[i] - width / 2 , zeros[i] / 2 , str(zeros[i]) if zeros[i] != 0 else '' , ha='center' , va='center' , color='black', fontsize=6)
        ax.text(ind[i] + width / 2 , singles[i] / 2 , str(singles[i]) if singles[i] != 0 else '' , ha='center' , va='center' , color='black', fontsize=6)
    plt.subplots_adjust(bottom=0.15)
    plt.show()



# Extract player names and counts
def plot(data,count):
    players = list(data.keys())
    names = [data[player]['name'] for player in data]
    zeros = [data[player]['zero'] for player in players]
    singles = [data[player]['single'] for player in players]

    # Bar width
    bar_width = 0.35

    # Set position of bar on X axis
    r1 = np.arange(len(players))
    r2 = [x + bar_width for x in r1]

    # Plot
    plt.figure(figsize=(12 , 8))
    plt.barh(r1 , zeros , color='skyblue' , height=bar_width , edgecolor='grey' , label='Number of Zero attacks in past 30 wars')
    plt.barh(r2 , singles , color='salmon' , height=bar_width , edgecolor='grey' , label='Number of Single attack in past 30 wars')

    # Add labels and title
    plt.xlabel('Number of missed attacks')
    plt.ylabel('Player')
    plt.title(f'Out of past {count} FWA wars')
    plt.yticks([r + bar_width / 2 for r in range(len(players))] , names)
    plt.legend()
    plt.grid(visible=True , axis='x' , which="both")

    # Show plot
    plt.tight_layout()
    plt.show()
