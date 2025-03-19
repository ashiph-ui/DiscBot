from discord.ext import commands
import random

# Card values dictionary, Ace is initially 11 (will adjust if needed)
card_values = {
    "2": 2, "3": 3, "4": 4, "5": 5, "6": 6, "7": 7, "8": 8, "9": 9, "10": 10,
    "J": 10, "Q": 10, "K": 10, "A": 11 
}
suits = ["Hearts", "Diamonds", "Clubs", "Spades"]

# This function will create a deck and run a loop through all the card variations and add them to the deck.
def create_deck():
    deck = [f"{card} of {suit}" for suit in suits for card in card_values]
    random.shuffle(deck)  # This will shuffle the deck to help randomize the dealt cards.
    return deck

# This function calculates the value of a player's hand
def calculate_hand_value(hand):
    value = 0
    aces = 0
    for card in hand:
        card_rank = card.split()[0]  # Extract card rank (e.g., "A", "10", "K")
        value += card_values[card_rank]  # Add card value
        if card_rank == "A":
            aces += 1  # Count Aces separately

    # This will change the value of the Ace to 1 if the value goes over 21.
    while value > 21 and aces:
        value -= 10
        aces -= 1

    return value

# Cog for the Blackjack game
class blackjack(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.deck = create_deck()
        self.players = {}  # This will store hands and game states

    # Game start command
    @commands.command(name="startblackjack")
    async def start_blackjack(self, ctx):
        """Start a new Blackjack game."""
        if ctx.author.id in self.players:
            await ctx.send("You are already in a game!")
            return

        if len(self.deck) < 10:  # Prevent deck depletion by recreating a shuffled deck if needed
            self.deck = create_deck()

        # Assign hands to player and dealer
        self.players[ctx.author.id] = {
            "hand": [self.deck.pop(), self.deck.pop()],
            "dealer_hand": [self.deck.pop(), self.deck.pop()],
            "game_over": False
        }

        player_hand = self.players[ctx.author.id]["hand"]
        dealer_hand = self.players[ctx.author.id]["dealer_hand"]

        await ctx.send(f"Your hand: {', '.join(player_hand)} (Value: {calculate_hand_value(player_hand)})")
        await ctx.send(f"Dealer's hand: {dealer_hand[0]}, [Hidden Card]")

    # Hit command
    @commands.command(name="hit")
    async def hit(self, ctx):
        """Draw another card."""
        if ctx.author.id not in self.players or self.players[ctx.author.id]["game_over"]:
            await ctx.send("You are not in a game or the game is over!")
            return

        player_hand = self.players[ctx.author.id]["hand"]
        player_hand.append(self.deck.pop())

        hand_value = calculate_hand_value(player_hand)
        await ctx.send(f"Your hand: {', '.join(player_hand)} (Value: {hand_value})")

        # If player goes over 21, they lose automatically
        if hand_value > 21:
            await ctx.send("Bust! You went over 21. Game over.")
            self.players[ctx.author.id]["game_over"] = True
             # Remove the player from the game
            del self.players[ctx.author.id]

    # Stand command
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

        dealer_value = calculate_hand_value(dealer_hand)
        player_value = calculate_hand_value(player_hand)

        await ctx.send(f"Dealer's hand: {', '.join(dealer_hand)} (Value: {dealer_value})")

        # Determine winner
        if dealer_value > 21:
            await ctx.send("Dealer busts! You win!")
        elif dealer_value > player_value:
            await ctx.send("Dealer wins!")
        elif dealer_value < player_value:
            await ctx.send("You win!")
        else:
            await ctx.send("It's a tie!")

        # Remove the player from the game
        del self.players[ctx.author.id]

# Required setup function to load the cog into the bot
async def setup(bot):
    await bot.add_cog(blackjack(bot))
