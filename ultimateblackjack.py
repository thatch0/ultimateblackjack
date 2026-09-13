import random, os, time

CARDS = 13
# 1 less than the actual ace value for bugfixing reasons
ACEVALUE = 10
BUSTVALUE = 21
cardvalues = {}

#dont forget to run this, dumbass
#note: i forgot
def initialize():
    os.system('cls' if os.name == 'nt' else 'clear')
    for i in range(1, CARDS+1):
        cardvalues.update({i: {1: True, 2: True, 3: True, 4: False}})

#setup and stuff
class Card:
    def __init__(self, value: int, suit: int, hidden: bool = False):
        # 1-10 = number cards, 11-13 = face cards, 14 = joker
        self.value = value
        # 1 = spade
        # 2 = heart
        # 3 = club
        # 4 = diamond
        self.suit = suit
        self.hidden = hidden
        

    def draw(self) -> list[str]:
        #visual things
        v = ""
        s = ""
        match self.suit:
            case 1:
                s = "♤"
            case 2:
                s = "♥"
            case 3:
                s = "♧"
            case 4:
                s = "♦"
        if self.value <= 10 and self.value > 1:
            v = self.value
        else:
            match self.value:
                case 1:
                    v = "A"
                case 11:
                    v = "J"
                case 12:
                    v = "Q"
                case 13:
                    v = "K"
                case 14:
                    v = "?"
                    s = "?"
        card = [f"{v}---+", f"| {s} |", f"+---{v}"]
        #2 digits = big no-no, alter visual to make me feel better
        if v == 10:
            card = [f"{v}--+", f"| {s} |", f"+--{v}"]
        if self.hidden:
            return ["+---+", "|UBJ|", "+---+"]
        return card

    def color(self):
        return self.suit % 2

    def hide(self):
        self.hidden = True

    def unhide(self):
        self.hidden = False

class Hand:
    def __init__(self, dealer: bool = False):
        self.cards = []
        self.draw_new_card()
        self.draw_new_card()
        if dealer:
            self.cards[1].hide()

    def draw_new_card(self):
        newcard = Card(random.randint(1, CARDS), random.randint(1, 4))
        while cardvalues[newcard.value][newcard.suit] == False:
            newcard = Card(random.randint(1, CARDS), random.randint(1, 4))
        self.cards.append(newcard)
        cardvalues[newcard.value].update({newcard.suit: False})

    def __call__(self):
        return self.cards

    def sum(self):
        total = 0
        ace = False
        for c in self.cards:
            total += c.value
            if c.value == 1:
                ace = True
        if ace and total + ACEVALUE <= BUSTVALUE:
            total += ACEVALUE
        return total

def print_hand(hand: list[Card]):
    p = []
    for c in hand:
        p.append(c.draw())
    for i in range(3):
        for j in range(len(p)):
            print(f"{p[j][i]} ", end="")
        print()

def print_board():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("-=# [Ultimate Blackjack] #=-\n")
    print("[dealer's hand]")
    print_hand(dealer_hand())
    print("[your hand]")
    print_hand(my_hand())

#fake loading sequence for immersion
os.system('cls' if os.name == 'nt' else 'clear')
print("-=# [Ultimate Blackjack] #=-\n")
print("loading", end="", flush=True)
time.sleep(1)
print(".", end="", flush=True)
time.sleep(1)
print(".", end="", flush=True)
time.sleep(1)
print(".", flush=True)
time.sleep(1)

print("loading finished! your game will start shortly...", flush=True)
time.sleep(2)
# actual game

initialize()

dealer_hand = Hand(True)
my_hand = Hand()

while True:
    print_board()

    #check for bust or blackjack
    if my_hand.sum() >= 21:
        break

    #idfk
    move = input("would you like to [h]it or [s]tand\n>>> ")
    match move:
        case "h":
            my_hand.draw_new_card()
        case "s":
            break

#dealer stuff + visual coolness
dealer_hand.cards[1].unhide()
print_board()
time.sleep(1)
while dealer_hand.sum() < 17:
    dealer_hand.draw_new_card()
    print_board()
    time.sleep(1)

#win conditions
if my_hand.sum() == dealer_hand.sum() or (dealer_hand.sum() > 21 and my_hand.sum() > 21):
    print(f"you tied!\nyour sum: {my_hand.sum()}\ndealer sum: {dealer_hand.sum()}")
elif (my_hand.sum() > dealer_hand.sum()  or dealer_hand.sum() > 21) and my_hand.sum() <= 21:
    print(f"you won!\nyour sum: {my_hand.sum()}\ndealer sum: {dealer_hand.sum()}")
else:
    print(f"you lost!\nyour sum: {my_hand.sum()}\ndealer sum: {dealer_hand.sum()}")

#please work