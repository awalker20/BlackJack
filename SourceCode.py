import random

suits = ('Hearts', 'Diamonds', 'Spades', 'Clubs')
ranks = ('Two', 'Three', 'Four', 'Five', 'Six', 'Seven', 'Eight', 'Nine', 'Ten', 'Jack', 'Queen', 'King', 'Ace')
values = {'Two': 2, 'Three': 3, 'Four': 4, 'Five': 5, 'Six': 6, 'Seven': 7, 'Eight': 8, 'Nine': 9, 'Ten': 10,
          'Jack': 10, 'Queen': 10, 'King': 10, 'Ace': 11}
playing = True


class Card:

    def __init__(self, suit, rank):
        self.suit = suit
        self.rank = rank

    def __str__(self):
        return self.rank + " of " + self.suit


class Deck:

    # load deck of cards
    def __init__(self):
        self.deck = []
        for suit in suits:
            for rank in ranks:
                self.deck.append(Card(suit, rank))

    def __str__(self):
        deck_comp = ""
        for card in self.deck:
            deck_comp += '\n' + card.__str__()
        return "The deck has: " + deck_comp

    # random shuffle deck
    def shuffle(self):
        random.shuffle(self.deck)

    # deal card off top of deck
    def deal(self):
        single_card = self.deck.pop()
        return single_card


class Hand:
    def __init__(self):
        self.cards = []  # start with empty hand
        self.value = 0  # hand value starts at zero
        self.aces = 0  # keep track of aces in hand

    def add_card(self, card):
        # card passed in from Deck.deal() --> single Card( has suit and rank)
        self.cards.append(card)
        # use card rank to look up value of card
        self.value += values[card.rank]

        # track aces
        if card.rank == 'Ace':
            self.aces += 1

    def adjust_for_ace(self):

        # if hand value > 21 and there is an ace in hand
        # then change value of ace to 1 from 11
        while self.value > 21 and self.aces:
            self.value -= 10
            self.aces -= 1


class Chips:

    # user starts with 100 chips
    def __init__(self):
        self.total = 100
        self.bet = 0

    # add bet amount to total chips
    def win_bet(self):
        self.total += self.bet

    # subtract bet amount from total chips
    def lose_bet(self):
        self.total -= self.bet


def take_bet(chips):
    while True:

        # set players bet
        try:
            chips.bet = int(input("How many chips would you like to bet? "))
        except:
            # check for valid input
            print("Please enter a number: ")
        else:
            # check to make sure player bet < player total # of chips
            if chips.bet > chips.total:
                print("Sorry, you do not have enough chips. You have: {}".format(chips.total))
            else:
                break


def hit(deck, hand):
    single_card = deck.deal()  # deal card from deck
    hand.add_card(single_card)  # add card to player hand
    hand.adjust_for_ace()  # check for an ace


def hit_or_stand(deck, hand):
    global playing

    while True:
        x = input("Would you like to Hit or Stand? Enter h or s ")
        print(x)

        if x == "h":
            hit(deck, hand)  # hit() function defined above

        elif x == "s":
            print("Player stands. Dealer is playing.")
            playing = False

        else:
            print("Sorry, please try again.")
            continue
        break


def show_some(player, dealer):
    print("\nDealers hand: ")
    print("<card hidden>")
    print(dealer.cards[1])
    print('\n')
    print("Players hand: ")
    for card in player.cards:
        print(card)
    print("________________________")


def show_all(player, dealer):
    print("\nDealers hand: ")
    for card in dealer.cards:
        print(card)
    print('\nPlayers hand: ')
    for card in player.cards:
        print(card)


def player_busts(player, dealer, chips):
    print("You BUST!")
    chips.lose_bet()


def player_wins(player, dealer, chips):
    print("Player wins!")
    chips.win_bet()


def dealer_busts(player, dealer, chips):
    print("Player wins! Dealer busted!")
    chips.win_bet()


def dealer_wins(player, dealer, chips):
    print("Dealer wins!")
    chips.lose_bet()


def push(player, dealer):
    print("Dealer and player tie!")


while True:
    # opening statement
    print(
        "Welcome to Blackjack!\nRules:\n"
        "-Goal of the game is to get as close to 21 as possible without going over.\n"
        "-Dealer hits until they're at 17 or above.\n"
        "-You start with 100 chips.\n\n"
        "Enjoy!\n")

    # create and shuffle deck, deal two cards to each player
    deck = Deck()
    deck.shuffle()

    # set players hand
    player_hand = Hand()
    player_hand.add_card(deck.deal())
    player_hand.add_card(deck.deal())

    # set dealers hand
    dealer_hand = Hand()
    dealer_hand.add_card(deck.deal())
    dealer_hand.add_card(deck.deal())

    # set players chips
    player_chips = Chips()

    # prompt player for bet
    take_bet(player_chips)

    # show cards, keep one dealer card hidden
    show_some(player_hand, dealer_hand)

    while playing:  # from hit or stand method

        # prompt player to hit or stand
        hit_or_stand(deck, player_hand)

        # show cards, keep one dealer card hidden
        show_some(player_hand, dealer_hand)

        # if players hand exceeds 21, player busts, end game
        if player_hand.value > 21:
            player_busts(player_hand, dealer_hand, player_chips)

            break

    # if player hasn't busted, play dealers hand until dealer reaches 17
    if player_hand.value <= 21:

        while dealer_hand.value < 17:
            hit(deck, dealer_hand)

        # show all cards
        show_all(player_hand, dealer_hand)

        # different win scenarios
        if dealer_hand.value > 21:
            dealer_busts(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value > player_hand.value:
            dealer_wins(player_hand, dealer_hand, player_chips)
        elif dealer_hand.value < player_hand.value:
            player_wins(player_hand, dealer_hand, player_chips)
        else:
            push(player_hand, dealer_hand)

    # display chips total
    print("\n Player's chips: {}".format(player_chips.total))

    # ask to play again
    new_game = input("Would you like to play again? y or n: ")

    if new_game[0].lower() == 'y':
        playing = True
        continue
    else:
        print("Thank you for playing!")
        break
