import random
import os

def clear_screen():
    os.system('clear')

class Deck:
    CARD_VALUES = ['A', '2', '3', '4', '5', '6', '7', '8', '9', '10', 'J', 'Q', 'K']
    CARD_SUITS = ['H', 'S', 'C', 'D']
    
    def __init__(self):
        self.cards = []
        self.shuffle()

    def shuffle(self):
        self.cards = []

        for value in Deck.CARD_VALUES:
            for suit in Deck.CARD_SUITS:
                lst_to_add = [value, suit]

                self.cards.append(lst_to_add)
        
        random.shuffle(self.cards)

    def get_card(self):
        return self.cards.pop()

    

class Participant:

    def __init__(self):
        self.score = 0
        self.hand = []

    def is_busted(self):
        score = self.get_score()
        
        if score > 21:
            return True

        return False

    def get_score(self):
        values = [card_info[0] for card_info in self.hand]
        
        sum_val = 0
        for value in values:
            if value == "A":
                sum_val += 11
            elif value in ["J", "Q", "K"]:
                sum_val += 10
            else:
                sum_val += int(value)
        
        aces = values.count("A")

        while sum_val > 21 and aces:
            sum_val -= 10
            aces -= 1
        
        return sum_val

class Player(Participant):
    def __init__(self):
        # STUB
        # What additional attributes might a player need?
        # Score? Hand? Amount of money available?
        super().__init__()
        self._balance = 5
    
    @property
    def balance(self):
        return self._balance

    @balance.setter
    def balance(self, new):
        self._balance = new



class Dealer(Participant):
    def __init__(self):
        super().__init__()

class TwentyOneGame:
    def __init__(self):
        # STUB
        # What attributes does the game need? A deck? Two
        #   participants?
        self.dealer = Dealer()
        self.player = Player()
        self.deck = Deck()
    
    @staticmethod
    def _join_or(choices, separator=", ", conjunction="and"):
        if len(choices) == 1:
            return str(choices[0])
        if len(choices) == 2:
            return f"{choices[0]} {conjunction} {choices[1]}"

        last = choices[-1]
        initial = choices[:-1]
        initial = [str(choice) for choice in initial]
        prompt = separator.join(initial)
        return f"{prompt}{separator}{conjunction} {last}"

    def start(self):
        self.display_welcome_message()

        while True:
            self.play_round()


            if self.player.balance == 10:
                print()
                input("You're rich! You win!")
                self.display_goodbye_message()
                break
            elif self.player.balance == 0:
                print()
                input("You're broke. You can't play anymore")
                self.display_goodbye_message()
                break

            choice = self.ask_play_again()
            
            if choice == "n":
                self.display_goodbye_message()
                break

    def ask_play_again(self):
        choice = input("Do you want to play again? (y/n)").lower()

        while True:
            if choice in ["y", "n"]:
                return choice
            
            print("That is not a valid choice")
            choice = input("Do you want to play again? (y/n)").lower()

    def play_round(self):
        self.player.hand = []
        self.dealer.hand  = []

        self.deal_cards(self.player, 2)
        self.deal_cards(self.dealer, 2)
        
        self.show_cards()
        self.player_turn()

        if not self.player.is_busted():
            self.dealer_turn()

        self.display_result()



    def deal_cards(self, receiver, num):
        for i in range(num):
            receiver.hand.append(self.deck.cards.pop())

    def show_cards(self, dealer_num=1):
        clear_screen()
        player_score = self.player.get_score()
        dealer_score = self.dealer.get_score()

        if dealer_num == 1:
            dealer_card_to_show = self.dealer.hand[0]
            print(f"Dealer has {dealer_card_to_show[0]} and unknown")
        else:
            vals = [card[0] for card in self.dealer.hand]
            print(f"Dealer has {self._join_or(vals)}")
        
        vals = [card[0] for card in self.player.hand]
        player_cards_str = self._join_or(vals)

        print(f"Player has {player_cards_str}")
        print(f"Player points: {player_score}")
        print(f"Dealer points:{dealer_score}")
        print()


    def get_hit_or_stay(self):
        CHOICES = ["h", "s"]
        choice = ""

        while True:
            choice = input("Hit or stay? (h/s)").lower()

            if choice in CHOICES:
                break

            print("That is not a valid choice")
        
        return choice

    def shuffle_if_needed(self):
        if len(self.deck.cards) == 0:
            self.deck.shuffle()

    def player_turn(self):

        while self.player.get_score() < 22:
            self.shuffle_if_needed()

            hit_or_stay = self.get_hit_or_stay()
            
            if hit_or_stay == "s":
                return

            if hit_or_stay == "h":
                self.deal_cards(self.player, 1)
            
            self.show_cards(2)

        
            
    def dealer_turn(self):
        self.show_cards(2)
        input("Dealer turn")
    
        if self.dealer.get_score() > 16:
            input("Dealer stayed")
            return
        while self.dealer.get_score() < 17:
            self.shuffle_if_needed()
            self.deal_cards(self.dealer, 1)
            self.show_cards(2)
            if self.dealer.get_score() > 21:
                print("Dealer hit")
                input("Dealer bust")
                return
            input("Dealer hit")
        
        self.show_cards(2)
        input("Dealer stayed")
        


    def display_welcome_message(self):
        print("Welcome to 21!")
        input(f"Your balance is {self.player.balance}")

    def display_goodbye_message(self):
        # STUB
        pass

    def get_winner(self):
        if self.player.is_busted():
            return "Dealer"
        elif self.dealer.is_busted() or self.player.get_score() > self.dealer.get_score():
            return "Player"
        elif self.player.get_score() == self.dealer.get_score():
            return "Tie"
        else:
            return "Dealer" 

    def display_result(self):
        winner = self.get_winner()

        print("Result: ")

        self.show_cards(2)

        if winner == "Tie":
            print("It's a tie")
        elif winner == "Player":
            self.player.balance += 1
            print(f"{winner} wins!")
            input(f"Your balance: {self.player.balance}")
        elif winner == "Dealer":
            self.player.balance -= 1
            print(f"{winner} wins!")
            input(f"Your balance: {self.player.balance}")
        
        


game = TwentyOneGame()
game.start()
