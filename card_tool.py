# --- A set of tools for basic operations on cards and sets of cards.
# --
# -- Several of the functions deal with "range vectors", which are probability
# -- vectors over the set of possible private hands. For Leduc Hold'em,
# -- each private hand consists of one card.
# -- @module card_tools
# local game_settings = require 'Settings.game_settings'
# local arguments = require 'Settings.arguments'
# local constants = require 'Settings.constants'
from Settings import game_settings
import math


class CardTool(object):
    def __init__(self):
        self.m = game_settings.basic_setting()

    def hand_is_possible(self, hand):
        assert min(hand) > 0 and max(hand) <= self.m['card_count']
        used_cards = [False] * self.m['card_count']
        print(used_cards)
        for i in range(0, len(hand)):
            if used_cards[hand[i]]:
                return False
            used_cards[hand[i]] = True
        return True

    # --- Gives the private hands which are valid with a given board.
    # -- @param board a possibly empty vector of board cards
    # -- @return a vector with an entry for every possible hand (private card), which
    # --  is `1` if the hand shares no cards with the board and `0` otherwise
    def get_possible_hand_indexes(self, board):
        out = [1] * self.m['card_count']
        if not board:
            return out
        for x in range(0, len(board)):
            out[board[x]] = 0
        return out

    # --- Gives the private hands which are invalid with a given board.
    # -- @param board a possibly empty vector of board cards
    # -- @return a vector with an entry for every possible hand (private card), which
    # -- is `1` if the hand shares at least one card with the board and `0` otherwise
    def get_impossible_hand_indexes(self, board):
        out = self.get_possible_hand_indexes(board)
        for i in range(0, len(out)):
            out[i] = (out[i] - 1) * -1
        return out

    # --- Gives a range vector that has uniform probability on each hand which is
    # -- valid with a given board.
    # -- @param board a possibly empty vector of board cards
    # -- @return a range vector where invalid hands have 0 probability and valid
    # -- hands have uniform probability
    def get_uniform_range(self, board):
        out = self.get_possible_hand_indexes(board)
        total = sum(out)
        for i in range(0, len(out)):
            out[i] = out[i]/(total + 0.0)
        return out





cardTool = CardTool()
print(cardTool.hand_is_possible([3]))
print(cardTool.get_possible_hand_indexes([2,3]))
print(cardTool.get_impossible_hand_indexes([3]))
print(cardTool.get_uniform_range([]))

# --- Randomly samples a range vector which is valid with a given board.
# -- @param board a possibly empty vector of board cards
# -- @param[opt] seed a seed for the random number generator
# -- @return a range vector where invalid hands are given 0 probability, each
# -- valid hand is given a probability randomly sampled from the uniform
# -- distribution on [0,1), and the resulting range is normalized
# function M:get_random_range(board, seed)
#   seed = seed or torch.random()
#
#   local gen = torch.Generator()
#   torch.manualSeed(gen, seed)
#
#   local out = torch.rand(gen, game_settings.card_count):typeAs(arguments.Tensor())
#   out:cmul(self:get_possible_hand_indexes(board))
#   out:div(out:sum())
#
#   return out
# end
#
# --- Checks if a range vector is valid with a given board.
# -- @param range a range vector to check
# -- @param board a possibly empty vector of board cards
# -- @return `true` if the range puts 0 probability on invalid hands and has
# -- total probability 1
# function M:is_valid_range(range, board)
#   local check = range:clone()
#   local only_possible_hands = range:clone():cmul(self:get_impossible_hand_indexes(board)):sum() == 0
#   local sums_to_one = math.abs(1.0 - range:sum()) < 0.0001
#   return only_possible_hands and sums_to_one
# end
#
# --- Gives the current betting round based on a board vector.
# -- @param board a possibly empty vector of board cards
# -- @return the current betting round
# function M:board_to_street(board)
#   if board:dim() == 0 then
#     return 1
#   else
#     return 2
#   end
# end
#
# --- Gives all possible sets of board cards for the game.
# -- @return an NxK tensor, where N is the number of possible boards, and K is
# -- the number of cards on each board
# function M:get_second_round_boards()
#   local boards_count = self:get_boards_count()
#   if game_settings.board_card_count == 1 then
#     local out = arguments.Tensor(boards_count, 1)
#     for card = 1, game_settings.card_count do
#       out[{card, 1}] = card
#     end
#     return out
#   elseif game_settings.board_card_count == 2 then
#     local out = arguments.Tensor(boards_count, 2)
#     local board_idx = 0;
#     for card_1 = 1, game_settings.card_count do
#       for card_2 = card_1 + 1, game_settings.card_count do
#         board_idx = board_idx + 1
#         out[{board_idx, 1}] = card_1
#         out[{board_idx, 2}] = card_2
#       end
#     end
#     assert(board_idx == boards_count, 'wrong boards count!')
#     return out
#   else
#     assert(false, 'unsupported board size' )
#   end
# end
#
# --- Gives the number of possible boards.
# -- @return the number of possible boards
# function M:get_boards_count()
#   if game_settings.board_card_count == 1 then
#     return game_settings.card_count
#   elseif game_settings.board_card_count == 2 then
#     return (game_settings.card_count * (game_settings.card_count - 1)) / 2
#   else
#     assert(false, 'unsupported board size' )
#   end
# end
#
# --- Initializes the board index table.
# -- @local
# function M:_init_board_index_table()
#   if game_settings.board_card_count == 1 then
#     self._board_index_table = torch.range(1, game_settings.card_count):float()
#   elseif game_settings.board_card_count == 2 then
#     self._board_index_table = arguments.Tensor(game_settings.card_count, game_settings.card_count):fill(-1)
#     local board_idx = 0;
#     for card_1 = 1, game_settings.card_count do
#       for card_2 = card_1 + 1, game_settings.card_count do
#         board_idx = board_idx + 1
#         self._board_index_table[card_1][card_2] = board_idx
#         self._board_index_table[card_2][card_1] = board_idx
#       end
#     end
#   else
#     assert(false, 'unsupported board size')
#   end
# end
#
# M:_init_board_index_table()
#
# --- Gives a numerical index for a set of board cards.
# -- @param board a non-empty vector of board cards
# -- @return the numerical index for the board
# function M:get_board_index(board)
#   local index = self._board_index_table
#   for i = 1, board:size(1) do
#     index = index[board[i]]
#   end
#   assert( index > 0, index)
#   return index
# end
#
# --- Normalizes a range vector over hands which are valid with a given board.
# -- @param board a possibly empty vector of board cards
# -- @param range a range vector
# -- @return a modified version of `range` where each invalid hand is given 0
# -- probability and the vector is normalized
# function M:normalize_range(board, range)
#   local mask = self:get_possible_hand_indexes(board)
#   local out = range:clone():cmul(mask)
#   --return zero range if it all collides with board (avoid div by zero)
#   if out:sum() == 0 then
#     return out
#   end
#   out:div(out:sum())
#   return out
# end
#
#
# return M