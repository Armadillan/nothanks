import random
from typing import Union

from dataclasses import dataclass, field

import neat

@dataclass
class Player:
    net: "neat.nn.FeedForwardNetwork | neat.nn.RecurrentNetwork"
    chips: int
    cards: [int] = field(default_factory=list)

    @property
    def total(self):
        score = 0
        for card in self.cards:
            if card - 1 not in self.cards:
                score += card
        score -= self.chips

        return score

class NoThanks:

    CHIPS_PER_PLAYER = {
    # num players: chips per player
        3: 11,
        4: 11,
        5: 11,
        6: 9,
        7: 7
    }

    def __init__(self, *args):
        self.cards = []
        self.players = []

    def get_new_cards(self):
        self.cards = [x for x in range(3, 36)]
        for _ in range(9):
            self.cards.pop(random.randrange(len(self.cards)))
        random.shuffle(self.cards)

    def make_players(self, group):
        num_players = len(group)
        if not (3 <= num_players <= 7):
            raise ValueError(f"group must have a length between 3 and 7, has length {num_players}")
        players = []

        for network in group:
            players.append(Player(network, self.CHIPS_PER_PLAYER[num_players]))

        self.players = players

    def choice(self, player_index, card, chips):

        if self.players[player_index].chips == 0:
            return True

        # input = cards + chips of each player + current card + current chips
        # current player is always player 1

        #cards
        input_array = [0] * 33
        for i, player in enumerate(self.players):
            for card in player.cards:
                if i == player_index:
                    input_array[card-3] = 1
                elif i < player_index:
                    input_array[card-3] = i+2
                else:
                    input_array[card-3] = i+1

        #player 1 chips
        input_array.append(self.players[player_index].chips)
        #other player's chips
        for i, player in enumerate(self.players):
            if i == player_index:
                continue
            input_array.append(player.chips)

        #current card and current chips
        input_array.extend([card, chips])

        choice = self.players[player_index].net.activate(input_array)

        if choice[0] < 0.5:
            return False
        return True

    def play(self, network_group):

        self.get_new_cards()
        self.make_players(network_group)

        current_player = 0

        for card in self.cards:

            chips = 0

            while True:

                #take card and chips
                if self.choice(current_player, card, chips):
                    self.players[current_player].chips += chips
                    self.players[current_player].cards.append(card)
                    break

                #put down chip
                self.players[current_player].chips -= 1
                chips += 1
                #and next player
                current_player += 1
                current_player %= len(self.players)

        return [player.total for player in self.players]

    def temp_test(self, group):
        i = 0
        scores = []
        for network in group:
            scores.append(self.i)
            self.i+=1
        return scores
