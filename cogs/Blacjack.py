from discord.ext import commands
import random

card_values = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 10, "K": 10, "A": 11 #figure out how to implement ace to equal 1 if the hand dealt with an ace goes above 21.
}
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

#this function will create a deck and run a loop though all the card variations and add them all up in deck.
def create_deck():
        deck = []
        for suit in suits:
              for card, value in card_values.items():
                    deck.append(f"{card} of {suit}")
                    random.shuffle(deck)  # this will shuffle the deck and to help randomise the dealt cards.
                    return deck

# Required setup function
async def setup(bot):
        await bot.add_cog(blackjack(bot))