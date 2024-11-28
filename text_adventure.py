from rich.console import Console
from rich.text import Text
import random


#region input validation
def validate_input(prompt, valid_inputs):
    while True:
        console.print(prompt, style="bold cyan")
        user_input = input("> ").lower()
        if user_input in valid_inputs:
            return user_input
        else:
            console.print("Invalid input. Please try again.", style="bold red")
#endregion

console = Console()

player_name = ""
player_health = 10
next_room = False

#Concactenation
console.print("Welcome to the Gloomy Cave Adventure!", style="bold green")
player_name = input("What's your name, brave adventurer? ")
console.print(f"Hello, " + player_name + "! Your adventure begins now.", style="bold green")


console.print(f"You find yourself in a dark, gloomy cave. What do you do?", style="bold cyan")

while not next_room:
    console.print("Choose an action: explore/investigate/rest", style = "bold white")
    action = input(">")

    if action == "explore":
        next_room = True
        console.print("You notice a tight passageway, and squeeze through", style = "italic green")


    if action == "investigate":

        #random number
        random_number = random.randint(0, 1)

        if random_number == 0:
            console.print("You found a healing herb! +2 health.", style="bold green")
            player_health == player_health + 2
        elif random_number == 1:
            damage = random.randint(0,5)
            console.print("A trap falls down from the ceiling, slightly crushing your toes!! You lost " + str(damage) + " health", style="bold red")
            player_health == player_health - damage
            console.print("You are now at " + str(player_health) + " health!!", style="bold green")

    if action == "rest":
            healing = random.randint(0,3)
            console.print("You take a rest and regain some health. +" + str(healing) + " health.", style="bold green")
            player_health == player_health + 2

    # Check if the player is still alive
    if player_health <= 0:
        console.print("You have succumbed to your injuries. Game Over.", style="bold red")
        exit()


#next room


console.print(f"The passageway leads to an open area which looks like an arena of some sort", style="bold cyan")
console.print(f"You are suddenly attacked by a star-nosed mole and a bat!!!", style="bold red")

#1D array of enemies
enemies = ["mole", "bat"]

next_room = False
while not next_room:
    console.print("Choose an action: fight/explore/investigate/rest", style = "bold white")
    action = input(">")

    if action == "fight":
        
        number_of_enemies = len(enemies)
        #loop for each enemy
        for counter in range(0,number_of_enemies):
            winning_chance = random.randint(0,10)
            if winning_chance <= 5:
                console.print("The enemy " + enemies[counter] + " was defeated!! You got some health", style="bold green")
                console.print("You are now at " + str(player_health) + " health!!", style="bold green")
                player_health = player_health + 8
            else:
                player_health = player_health - 4
                console.print("The enemy " + enemies[counter] + " attacked you!!!. You lost 4 health", style="bold red")
                console.print("You are now at " + str(player_health) + " health!!", style="bold red")
              
    if action == "explore":
        next_room = True
        console.print("You notice a tight passageway, and squeeze through", style = "italic green")


    if action == "investigate":

        #random number
        random_number = random.randint(0, 1)

        if random_number == 0:
            console.print("You found a healing herb! +2 health.", style="bold green")
            player_health == player_health + 2
            console.print("You are now at " + str(player_health) + " health!!", style="bold green")
        elif random_number == 1:
            damage = random.randint(0,5)
            console.print("A trap falls down from the ceiling, slightly crushing your toes!! You lost " + damage + " health", style="bold red")
            player_health == player_health - damage
            console.print("You are now at " + str(player_health) + " health!!", style="bold red")

    if action == "rest":
            healing = random.randint(0,3)
            console.print("You take a rest and regain some health. +" + str(healing) + " health.", style="bold green")
            player_health == player_health + 2

    # Check if the player is still alive
    if player_health <= 0:
            console.print("You have succumbed to your injuries. Game Over.", style="bold red")




