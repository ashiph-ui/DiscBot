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

def calculate_hand_value(hand):
    value = 0 
    aces = 0
    for card in hand:
        card_name = card.split([card_name]) # tis will get the card name
        if card_name == "A":
            aces += 1
    while value > 21 and aces:#this will change the value of the ace to 1 if the value goes over 21.
              value -= 10
              aces -= 1
    return value 
#Cog
class blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deck = create_deck()
        self.players = {}#this will store hands and game state


#Game start command
    @commands.command(name = "startblackjack")
    async def start_blackjack(self, ctx):
        """Start a new Blackjack game."""
        if ctx.author.id in self.players:
            await ctx.send("you are in a game!!")
            return
        #player and B-A-Bs hands
        self.players[ctx.author.id] = {
            "hand": [self.deck.pop(), self.deck.pop()],
            "dealer_hand": [self.deck.pop(), self.deck.pop()],
            "game_over": False
        }
        player_hand = self.players[ctx.author.id]["hand"]
        dealer_hand = self.players[ctx.author.id]["dealer_hand"]
        await ctx.send(f"Your hand: {', '.join(player_hand)} (Value: {calculate_hand_value(player_hand)})")
        await ctx.send(f"Dealer's hand: {dealer_hand[0]}, [Hidden Card]")
    
    #hit command
    @commands.command(name="hit")
    async def hit(self, ctx):
        """Draw another card."""
        if ctx.author.id not in self.players or self.players[ctx.author.id]["game_over"]:
            await ctx.send("You are not in a game or the game is over!")
            return
        player_hand = self.players[ctx.author.id]["hand"]
        player_hand.append(self.deck.pop())
        await ctx.send(f"Your hand: {', '.join(player_hand)} (Value: {calculate_hand_value(player_hand)})")
        if calculate_hand_value(player_hand) > 21:
            await ctx.send("Bust! You went over 21. Game over.")
            self.players[ctx.author.id]["game_over"] = True


    @commands.command(name="stand")
    async def stand(self, ctx):
        """End your turn and let the dealer play."""
        if ctx.author.id not in self.players or self.players[ctx.author.id]["game_over"]:
            await ctx.send("You are not in a game or the game is over!")
            return
        self.players[ctx.author.id]["game_over"] = True
        dealer_hand = self.players[ctx.author.id]["dealer_hand"]
        player_hand = self.players[ctx.author.id]["hand"]
        # Dealer draws until their hand is at least 17
        while calculate_hand_value(dealer_hand) < 17:
            dealer_hand.append(self.deck.pop())
        await ctx.send(f"Dealer's hand: {', '.join(dealer_hand)} (Value: {calculate_hand_value(dealer_hand)})")
        player_value = calculate_hand_value(player_hand)
        dealer_value = calculate_hand_value(dealer_hand)
        if dealer_value > 21:
            await ctx.send("Dealer busts! You win!")
        elif dealer_value > player_value:
            await ctx.send("Dealer wins!")
        elif dealer_value < player_value:
            await ctx.send("You win!")
        else:
            await ctx.send("It's a tie!")
        del self.players[ctx.author.id]  # Remove the player from the game

# Required setup function
async def setup(bot):
        await bot.add_cog(blackjack(bot))