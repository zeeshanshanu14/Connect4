import itertools
import sys

import numpy as np


def execute_player_action(game_board, played_loc, player):
    if played_loc > np.shape(game_board)[1] - 1:
        print(6)
        exit(6)
    success_flag = 0
    changed_board = game_board[:, played_loc]
    # iterate that column in reverse as checker will be stacked to top
    for x in range(len(changed_board), 0, -1):
        index = x - 1
        if not changed_board[index]:
            changed_board[index] = player
            success_flag = 1
            break
    if success_flag:
        game_board[:, played_loc] = changed_board
        # lets send the last location changed to reduce search space of game won
        return game_board, (index, played_loc)
    else:
        # illegal row, return 5 as per test cases
        print(5)
        exit(5)


def construct_game_board(dim):
    return np.zeros((dim[0], dim[1]))


def check_horz_win(game_board, last_played_loc, player, win_length):
    row = last_played_loc[0]
    col = last_played_loc[1]
    counter = 1
    # if player won in horizontal completion then this checker can be anywhere in conbination in a row
    for x in range(col + 1, np.shape(game_board)[1]):
        if game_board[row][x] == player:
            counter += 1
            if counter == win_length:
                return True
            continue
    # if changed location is less the the length and nothing was found on the right, check left as well
    if col + 1 < win_length and counter == 1:
        return 0
    for x in range(col - 1, 0, -1):
        if game_board[row][x] == player:
            counter += 1
            if counter == win_length:
                return player
            continue
        else:
            return 0


def check_ver_win(game_board, last_played_loc, player, win_length):
    col = last_played_loc[1]
    counter = 1
    # if plaer won in vertical then his checker will be on top
    for x in range(last_played_loc[0] + 1, np.shape(game_board)[0]):
        if game_board[x][col] == player:
            counter += 1
            if counter == win_length:
                return player
            continue
        else:
            return 0


def check_diag_win_backslash(game_board, last_played_loc, player, win_length):
    col = last_played_loc[1]
    row = last_played_loc[0]
    # checking backward diagonal
    counter = 1
    col_forwards = list(range(col, np.shape(game_board)[1]))
    row_backwards = list(range(row, 0 - 1, -1))
    diag_list = [i for i in itertools.zip_longest(col_forwards, row_backwards)]  # zip(col_forwards, row_forwards)
    counter = 0
    for col_index, row_index in diag_list:

        # if player won in horizontal completion then this checker can be anywhere in conbination in a row
        if col_index is None or row_index is None:
            continue
        if game_board[row_index][col_index] == player:
            counter += 1
            if counter == win_length:
                return player
            continue
        # if changed location is less the the length and nothing was found on the right, check left as well
    if col < win_length - 1 and counter == 1:
        return 0
    # now check starting from next diag element is curr is already counted
    col_backwards = list(range(col - 1, 0 - 1, -1))
    row_forwards = list(range(row + 1, np.shape(game_board)[0]))
    diag_list_down = [i for i in itertools.zip_longest(col_backwards, row_forwards)]
    # should iterate backwards as we going down
    for col_index, row_index in diag_list_down:

        # if player won in horizontal completion then this checker can be anywhere in conbination in a row
        if col_index is None or row_index is None:
            continue
        if game_board[row_index][col_index] == player:
            counter += 1
            if counter == win_length:
                return player
            continue
    return 0


def check_diag_win_fslash(game_board, last_played_loc, player, win_length):
    col = last_played_loc[1]
    row = last_played_loc[0]
    # checking backward diagonal down first
    col_forwards = list(range(col, np.shape(game_board)[1]))
    row_backwards = list(range(row, np.shape(game_board)[0]))
    diag_list = [i for i in itertools.zip_longest(col_forwards, row_backwards)]  # zip(col_forwards, row_forwards)
    counter = 0
    for col_index, row_index in diag_list:

        # if player won in horizontal completion then this checker can be anywhere in conbination in a row
        if col_index is None or row_index is None:
            continue
        if game_board[row_index][col_index] == player:
            counter += 1
            if counter == win_length:
                return player
            continue
        else:
            break
        # if changed location is less the the length and nothing was found on the right, check left as well
        # if there is not much to be checked and already found match is too less, its not work traversing.
    if col < win_length and counter == 1:
        return 0
    # now check up, current cell is counted for above
    col_backwards = list(range(col - 1, 0 - 1, -1))
    row_backwards = list(range(row - 1, 0 - 1, -1))
    diag_list_up = [i for i in itertools.zip_longest(col_backwards, row_backwards)]
    # should iterate backwards as we going down
    for col_index, row_index in diag_list_up:

        # if player won in horizontal completion then this checker can be anywhere in conbination in a row
        if col_index is None or row_index is None:
            continue
        if game_board[row_index][col_index] == player:
            counter += 1
            if counter == win_length:
                return player
            continue
        else:
            break
    return 0


def check_player_won(game_board, last_played_loc, player, win_length):
    winner = check_diag_win_backslash(game_board, last_played_loc, player, win_length) or check_diag_win_fslash(
        game_board, last_played_loc, player, win_length) or check_horz_win(game_board, last_played_loc,
                                                                           player,
                                                                           win_length) or check_ver_win(
        game_board, last_played_loc, player, win_length)
    if winner:
        return winner
    else:
        return 3


def play(input_file):
    validation_code = validate_file(input_file[0:3])
    if validation_code >0 :
        return validation_code

    game_board = construct_game_board(input_file[0:2])

    player = 1
    attemps_played_total = 1
    wining_length = input_file[2]
    winning_player = 0
    for col in input_file[3:]:
        if winning_player:
            return 4
        played_loc = col - 1
        game_board, chaged_loc = execute_player_action(game_board, played_loc, player)
        if attemps_played_total >= input_file[2] * 2 - 1:
            winner = check_player_won(game_board, chaged_loc, player, wining_length)
            if winner in [1, 2]:
                winning_player = winner
                continue
        if attemps_played_total >= np.size(game_board):
            # draw
            return 0
        #     # incomplete game
        #     return 3
        player = 2 if player == 1 else 1
        attemps_played_total += 1
    if winning_player:
        return winning_player
    elif attemps_played_total < np.size(game_board):
        # incomplete
        return 3


def validate_file(meta_data_array):
    if len(meta_data_array) < 2:
        return 8
    row = meta_data_array[0]
    col = meta_data_array[1]
    winning_length = meta_data_array[2]
    if (winning_length > row and winning_length > col) or (row > winning_length and col < 2) or (
            col > winning_length and row < 2):
        # illegal game
        return 7
    else:
        return 0


if __name__ == '__main__':
    if len(sys.argv) != 2:
        exit('connectz.py: Provide one input file')
    file_name = sys.argv[1]
    try:
        data = np.fromfile(file_name, dtype=int, sep=' ')
        return_code = play(data)
    except IOError:
        return_code = 9
    print(return_code)
    exit(return_code)
