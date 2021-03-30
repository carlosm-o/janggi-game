class JanggiGame:
    """
    This class is responsible for storing all the information about the current state of a Janggi game
    and will also be responsible for determining the valid moves at the current state.
    """

    def __init__(self):
        """
        Initializes the board, the piece class, user turn, and game state
        """
        # board is 9x10 2d list, each element of the list has 2 characters.
        # the first character represents the color of the piece, "r" for red
        # or "b" for blue. The second character represents the type of the piece
        # C: Chariot, E: Elephant, H: Horse, G: Guard, K: General, F: Cannon, S: Soldier
        # "--" represents an empty space with no piece

        self._board = [
            ["rC", "rE", "rH", "rG", "--", "rG", "rE", "rH", "rC"],
            ["--", "--", "--", "--", "rK", "--", "--", "--", "--"],
            ["--", "rF", "--", "--", "--", "--", "--", "rF", "--"],
            ["rS", "--", "rS", "--", "rS", "--", "rS", "--", "rS"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["--", "--", "--", "--", "--", "--", "--", "--", "--"],
            ["bS", "--", "bS", "--", "bS", "--", "bS", "--", "bS"],
            ["--", "bF", "--", "--", "--", "--", "--", "bF", "--"],
            ["--", "--", "--", "--", "bK", "--", "--", "--", "--"],
            ["bC", "bE", "bH", "bG", "--", "bG", "bE", "bH", "bC"],
        ]
        self._piece = Piece(self)
        self._blue_turn = True
        self._game_state = "UNFINISHED"

    # Getters

    def get_board(self):
        """
        Returns the current board
        """
        return self._board

    def get_turn(self):
        """
        Returns the current turn
        """
        return self._blue_turn

    def get_game_state(self):
        """
        Returns the curren game state
        """
        return self._game_state

    # Other methods

    def print_board(self):
        """
        Prints the board for a vizual representation 
        """
        for i in range(len(self._board)):
            for j in range(len(self._board[i])):
                print(self._board[i][j], end=" ")
            print()

    def is_in_check(self, color):
        """
        Checks if current player is in check
        """

        if color == "blue":
            blue_gen_pos = []

            for r in range(len(self._board)):
                for c in range(len(self._board[r])):
                    if self._board[r][c][0:2] == "bK":
                        blue_gen_pos.append((r, c))
            
            red_moves = [i[2] for i in self.temp_change_turn() if "r" in i[0]]
        
            if blue_gen_pos[0] in red_moves:
                return True            
            
        elif color == "red":
            red_gen_pos = []

            for r in range(len(self._board)):
                for c in range(len(self._board[r])):
                    if self._board[r][c][0:2] == "rK":
                        red_gen_pos.append((r, c))
            
            blue_moves = [i[2] for i in self.temp_change_turn() if "b" in i[0]]

            if red_gen_pos[0] in blue_moves:
                return True

        return False

    def temp_change_turn(self):
        """
        Temporarily changes whose turn it is in order to verify if current
        player is attackable by the other team
        """

        self._blue_turn = not self._blue_turn
        self._piece.reset_moves_list()
        self._piece.get_all_valid_moves()
        self._blue_turn = not self._blue_turn

        return self._piece.get_all_valid_moves()

    def switch_player(self):
        self._blue_turn = not self._blue_turn

    def get_color(self):

        if self._blue_turn:
            color = "blue"
        else:
            color = "red"

        return color

    def is_checkmated(self):
        """
        Checks to see if the other team is in checkmake
        by attempting all the opposing team's valid moves,
        if no valid moves remain then checkmate has occurred
        """
        # switch player
        self.switch_player()

        # reset player move list
        self._piece.reset_moves_list()
        
        # Make a list of all valid moves
        valid_moves = [(i[1], i[2]) for i in self._piece.get_all_valid_moves()]

        # attempt each move on valid list and check for check
        for i in reversed(valid_moves):

            board_backup = [list(i) for i in self._board]   

            # attempt each move on valid list and check for check
            move_from_row = i[0][0]
            move_from_col = i[0][1]
            move_to_row = i[1][0]
            move_to_col = i[1][1]
            piece_moved = self._board[move_from_row][move_from_col]

            self._board[move_from_row][move_from_col] = "--"
            self._board[move_to_row][move_to_col] = piece_moved
            
            # remove the move if check still occurs
            if self.is_in_check(self.get_color()):
                valid_moves.remove(i)
                self._board = board_backup
                if len(valid_moves) == 3:

                    if self._blue_turn:
                        self._game_state = "RED_WON"
                        return True
                    else:
                        self._game_state = "BLUE_WON"
                        return True
            else:
                self.switch_player()
                self._board = board_backup
                return False

        self.switch_player()

        return False

    def get_move_from_coord(self, start):

        start_sq = self.convert_user_input(start)

        move_from_row = int(start_sq[0])
        move_from_col = int(start_sq[1])

        return (move_from_row, move_from_col)

    def get_move_to_coord(self, end):

        end_sq = self.convert_user_input(end)

        move_to_row = int(end_sq[0])
        move_to_col = int(end_sq[1])

        return (move_to_row, move_to_col)

    def get_piece_moved(self, start):

        piece_moved = self._board[self.get_move_from_coord(start)[0]][self.get_move_from_coord(start)[1]]
        
        return piece_moved

    def get_piece_taken(self, end):
        piece_taken = self._board[self.get_move_to_coord(end)[0]][self.get_move_to_coord(end)[1]]

        return piece_taken
    def make_move(self, start, end):
        """
        Moves the pieces after validating that the move can be 
        made
        """

        # check g state
        if self._game_state != "UNFINISHED":
            return False

        self._piece.reset_moves_list()

        # converts user input to board index notation
        # start_sq = self.convert_user_input(start)
        # end_sq = self.convert_user_input(end)

        # move_from_row = int(start_sq[0])
        # move_from_col = int(start_sq[1])
        # move_to_row = int(end_sq[0])
        # move_to_col = int(end_sq[1])

        # piece_moved = self._board[move_from_row][move_from_col]

        # piece_taken = self._board[move_to_row][move_to_col]

        # pass the turn to the other player
        if start == end and self.get_piece_moved(start) != "--":
            # change player turn
            self.switch_player()
            return True

        # check if piece exists on starting spot
        if self.get_piece_moved(start) == "--":
            return False

        # check if it is correct turn
        if self._blue_turn is False and self.get_piece_moved(start)[0] == "b":
            return False

        if self._blue_turn is True and self.get_piece_moved(start)[0] == "r":
            return False

        # check if piece is trying to capture its own piece
        if self.get_piece_moved(start)[0] == self.get_piece_taken(end)[0]:
            return False
        
        # make a copy of the board before move
        board_backup = [list(i) for i in self._board]

        print(self.get_move_to_coord(end))

        # create validation tuples
        validate = (self.get_piece_moved(start), self.get_move_to_coord(end))

        valid_moves = [(i[0],i[2]) for i in self._piece.get_all_valid_moves()]

        # if all is good, move the piece
        if validate in valid_moves:
            self._board[self.get_move_to_coord(end)[0]][self.get_move_to_coord(end)[1]] = self.get_piece_moved(start)
            self._board[self.get_move_from_coord(start)[0]][self.get_move_from_coord(start)[1]] = "--"            
        else:
            return False

        # verifies that move did not put current color in check
        # and verify checkmate condition
        if self.is_in_check(self.get_color()):
            self._board = board_backup
            return False

        # check if the other team is mated
        if self.is_checkmated():
            return True

        # switch players
        self.switch_player()

        return True

    def convert_user_input(self, input):
        """
        Converts the user input into index value notation
        """
        row_value = input[1:3]
        col_value = input[0]

        convert_rows = {
            "0": "1",
            "1": "2",
            "2": "3",
            "3": "4",
            "4": "5",
            "5": "6",
            "6": "7",
            "7": "8",
            "8": "9",
            "9": "10",
        }

        convert_col = {
            "0": "a",
            "1": "b",
            "2": "c",
            "3": "d",
            "4": "e",
            "5": "f",
            "6": "g",
            "7": "h",
            "8": "i",
        }

        for key, value in convert_rows.items():
            if value == row_value:
                row = key

        for key, value in convert_col.items():
            if value == col_value:
                col = key

        converted_input = row + col

        return converted_input


class Piece:
    """
    Represents pieces of the board that each have their own unique movement
    and tracks all the pieces' valid movements
    """

    def __init__(self, game):
        """
        Initializes the piece class with, the game (parent class), and valid moves list (empty)
        """
        self._game = game
        self._moves = []


    def reset_moves_list(self):
        """
        Resets the moves list
        """
        self._moves.clear()


    def get_all_valid_moves(self):
        """
        Gets all the valid moves for each piece
        """

        for r in range(len(self._game.get_board())):
            for c in range(len(self._game.get_board()[r])):
                color = self._game.get_board()[r][c][0]
                if (color == "b" and self._game.get_turn()) or (
                    color == "r" and not self._game.get_turn()
                ):
                    piece = self._game.get_board()[r][c][1]
                    # C: Chariot, E: Elephant, H: Horse, G: Guard, K: General, F: Cannon, S: Soldier
                    if piece == "C":
                        self.get_chariot_moves(r, c)
                    elif piece == "E":
                        self.get_elephant_moves(r, c)
                    elif piece == "H":
                        self.get_horse_moves(r, c)
                    elif piece == "G":
                        self.get_guard_moves(r, c)
                    elif piece == "K":
                        self.get_general_moves(r, c)
                    elif piece == "F":
                        self.get_cannon_moves(r, c)
                    elif piece == "S":
                        self.get_soldier_moves(r, c)

        return self._moves

    def get_chariot_moves(self, r, c):
        """
        Gets all the valid moves for the chariot piece
        """
        piece = "bC" if self._game.get_turn() else "rC"
        takeable = "r" if self._game.get_turn() else "b"
        board = self._game.get_board()
        move_valid = ["r", "-"] if self._game.get_turn() else ["b", "-"]
        moves = self._moves
        red_palace = self.get_red_palace_moves()
        blue_palace = self.get_blue_palace_moves()

        # move up

        for i in range(1, 11):
            if 0 <= r - i < 9:
                if board[r - i][c][0] in piece:
                    break
                elif board[r - i][c][0] == takeable:
                    moves.append((piece, (r, c), (r - i, c)))
                    break
                else:
                    if board[r - i][c][0] in move_valid:
                        moves.append((piece, (r, c ), (r - i, c)))
        # move down
        for i in range(1, 11):
            if 0 <= r + i < 9:
                if board[r + i][c][0] in piece:
                    break
                elif board[r + i][c][0] == takeable:
                    moves.append((piece, (r, c ), (r + i, c)))
                    break
                else:
                    if board[r + i][c][0] in move_valid:
                        moves.append((piece, (r, c), (r + i, c)))
        # move right
        for i in range(1, 10):
            if 0 <= c + i < 8:
                if board[r][c + i][0] in piece:
                    break
                elif board[r][c + i][0] == takeable:
                    moves.append((piece, (r, c), (r, c + i)))
                    break
                else:
                    if board[r][c + i][0] in move_valid:
                        moves.append((piece, (r, c), (r, c + i)))
        # move left 
        for i in range(1, 10):
            if 0 <= c - i < 8:
                if board[r][c - i][0] in piece:
                    break
                elif board[r][c - i][0] == takeable:
                    moves.append((piece, (r, c), (r, c - i)))
                    break
                else:
                    if board[r][c - i][0] in move_valid:
                        moves.append((piece, (r, c), (r, c - i)))

        # if in red palace

        # if in palace can move diagonally up to the right
        if (
            (r, c) in red_palace
            and (r - 2 >= 0 or r - 1 >= 0)
            and (c + 2 <= 5 or c + 1 <= 5)
            and (r, c) not in [(3, 1), (4, 0), (5, 1), (4, 2)]
        ):
            for i in range(1, 3):
                if board[r - i][c + i][0] in piece:
                    break
                elif board[r - i][c + i][0] == takeable:
                    moves.append((piece, (r, c), (r - i, c + i)))
                    break
                else:
                    if board[r - i][c + i][0] in move_valid:
                        moves.append((piece, (r, c), (r - i, c + i)))
        # if in palace can move diagonally up to the left
        if (
            (r, c) in red_palace
            and (r - 2 >= 0 or r - 1 >= 0)
            and (c - 2 >= 3 or c - 1 >= 3)
            and (r, c) not in [(3, 1), (4, 0), (5, 1), (4, 2)]
        ):
            for i in range(1, 3):
                if board[r - i][c - i][0] in piece:
                    break
                elif board[r - i][c - i][0] == takeable:
                    moves.append((piece, (r, c), (r - i, c + i)))
                    break
                else:
                    if board[r - i][c - i][0] in move_valid:
                        moves.append((piece, (r, c), (r - i, c - i)))
        # if in palace can move diagonally down to the left
        if (
            (r, c) in red_palace
            and (r + 2 <= 2 or r + 1 <= 2)
            and (c - 2 >= 3 or c - 1 >= 3)
            and (r, c) not in [(3, 1), (4, 0), (5, 1), (4, 2)]
        ):
            for i in range(1, 3):
                if board[r + i][c - i][0] in piece:
                    break
                elif board[r + i][c - i][0] == takeable:
                    moves.append((piece, (r, c), (r - i, c - i)))
                    break
                else:
                    if board[r + i][c - i][0] in move_valid:
                        moves.append((piece, (r, c), (r + i, c - i)))
        # if in palace can move diag down to right
        if (
            (r, c) in red_palace
            and (r + 2 <= 2 or r + 1 <= 2)
            and (c + 2 <= 5 or c + 1 <= 5)
            and (r, c) not in [(3, 1), (4, 0), (5, 1), (4, 2)]
        ):
            for i in range(1, 3):
                if board[r + i][c + i][0] in piece:
                    break
                elif board[r + i][c + i][0] == takeable:
                    moves.append((piece, (r, c), (r - i, c + i)))
                    break
                else:
                    if board[r + i][c + i][0] in move_valid:
                        moves.append((piece, (r, c), (r + i, c + i)))

        # if in blue palace

        # if in palace can move diagonally up to the right
        if (
            (r, c) in blue_palace
            and (r - 2 >= 7 or r - 1 >= 7)
            and (c + 2 <= 5 or c + 1 <= 5)
            and (r, c) not in [(7, 4), (8, 3), (8, 5), (9, 4)]
        ):
            for i in range(1, 3):
                if board[r - i][c + i][0] in piece:
                    break
                elif board[r - i][c + i][0] == takeable:
                    moves.append((piece, (r, c), (r - i, c + i)))
                    break
                else:
                    if board[r - i][c + i][0] in move_valid:
                        moves.append((piece, (r, c), (r - i, c + i)))
        # if in palace can move diagonally up to the left
        if (
            (r, c) in blue_palace
            and (r - 2 >= 7 or r - 1 >= 7)
            and (c - 2 >= 3 or c - 1 >= 3)
            and (r, c) not in [(7, 4), (8, 3), (8, 5), (9, 4)]
        ):
            for i in range(1, 3):
                if board[r - i][c - i][0] in piece:
                    break
                elif board[r - i][c - i][0] == takeable:
                    moves.append((piece, (r, c), (r - i, c + i)))
                    break
                else:
                    if board[r - i][c - i][0] in move_valid:
                        moves.append((piece, (r, c), (r - i, c - i)))
        # if in palace can move diagonally down to the left
        if (
            (r, c) in blue_palace
            and (r + 2 <= 0 or r + 1 <= 0)
            and (c - 2 >= 3 or c - 1 >= 3)
            and (r, c) not in [(7, 4), (8, 3), (8, 5), (9, 4)]
        ):
            for i in range(1, 3):
                if board[r + i][c - i][0] in piece:
                    break
                elif board[r + i][c - i][0] == takeable:
                    moves.append((piece, (r, c), (r - i, c - i)))
                    break
                else:
                    if board[r + i][c - i][0] in move_valid:
                        moves.append((piece, (r, c), (r + i, c - i)))
        # if in palace can move diag down to right
        if (
            (r, c) in blue_palace
            and (r + 2 <= 0 or r + 1 <= 0)
            and (c + 2 <= 5 or c + 1 <= 5)
            and (r, c) not in [(7, 4), (8, 3), (8, 5), (9, 4)]
        ):
            for i in range(1, 3):
                if board[r + i][c + i][0] in piece:
                    break
                elif board[r + i][c + i][0] == takeable:
                    moves.append((piece, (r, c), (r - i, c + i)))
                    break
                else:
                    if board[r + i][c + i][0] in move_valid:
                        moves.append((piece, (r, c), (r + i, c + i)))

    def get_elephant_moves(self, r, c):
        """
        Gets all the valid moves for the elephant piece
        """
        piece = "bE" if self._game.get_turn() else "rE"
        board = self._game.get_board()
        move_valid = ["r", "-"] if self._game.get_turn() else ["b", "-"]
        moves = self._moves
        blockers = ["b", "r"]

        # move up moves

        # check up boundaries
        if r - 3 >= 0:
            # check first space for blockers
            if board[r - 1][c][0] not in blockers:
                # check right boundary
                if c + 2 <= 8:
                    # check right for blockers
                    if board[r - 2][c + 1][0] not in blockers:
                        # check final spot for enemy or blank space
                        if board[r - 3][c + 2][0] in move_valid:
                            # append valid moves
                            moves.append((piece, (r, c), (r - 3, c + 2)))

                # check left boundaries
                if c - 2 >= 0:
                    # check left for blockers
                    if board[r - 2][c - 1][0] not in blockers:
                        # check final spot for enemy or blank space
                        if board[r - 3][c - 2][0] in move_valid:
                            # append valid moves
                            moves.append((piece, (r, c), (r - 3, c - 2)))

        # move down moves

        # check down boundaries
        if r + 3 <= 9:
            # check first space for blockers
            if board[r + 1][c][0] not in blockers:
                # check right boundary
                if c + 2 <= 8:
                    # check right for blockers
                    if board[r + 2][c + 1][0] not in blockers:
                        # check final spot for enemy or blank space
                        if board[r + 3][c + 2][0] in move_valid:
                            # append valid moves
                            moves.append((piece, (r, c), (r + 3, c + 2)))
                # check left boundary
                if c - 2 >= 0:
                    # check left for blockers
                    if board[r + 2][c - 1][0] not in blockers:
                        # check final spot for enemy or blank space
                        if board[r + 3][c - 2][0] in move_valid:
                            # append valid moves
                            moves.append((piece, (r, c), (r + 3, c - 2)))

        # move left moves

        # check left boundaries
        if c - 3 >= 0:
            # check first space for blockers
            if board[r][c - 1][0] not in blockers:
                # check up boundary
                if r - 2 >= 0:
                    # check up for blockers
                    if board[r - 1][c - 2][0] not in blockers:
                        # check final spot for enemy or blank space
                        if board[r - 2][c - 3][0] in move_valid:
                            # append valid moves
                            moves.append((piece, (r, c), (r - 2, c - 3)))
                # check down boundary
                if r + 2 <= 9:
                    # check down for blockers
                    if board[r + 1][c - 2][0] not in blockers:
                        # check final spot for enemy or blank space
                        if board[r + 2][c - 3][0] in move_valid:
                            # append valid moves
                            moves.append((piece, (r, c), (r + 2, c - 3)))

        # move right moves

        # check right boundaries
        if c + 3 <= 8:
            # check first space for blockers
            if board[r][c + 1][0] not in blockers:
                # check up boundary
                if r - 2 >= 0:
                    # check up for blockers
                    if board[r - 1][c + 2][0] not in blockers:
                        # check final spot for enemy or blank space
                        if board[r - 2][c + 3][0] in move_valid:
                            # append valid moves
                            moves.append((piece, (r, c), (r - 2, c + 3)))
                # check down boundary
                if r + 2 <= 9:
                    # check down for blockers
                    if board[r + 1][c + 2][0] not in blockers:
                        # check final spot for enemy or blank space
                        if board[r + 2][c + 3][0] in move_valid:
                            # append valid moves
                            moves.append((piece, (r, c), (r + 2, c + 3)))

    def get_horse_moves(self, r, c):
        """
        Gets all the valid moves for the horse piece
        """

        piece = "bH" if self._game.get_turn() else "rH"
        board = self._game.get_board()
        move_valid = ["r", "-"] if self._game.get_turn() else ["b", "-"]

        # check bounds
        if r - 2 >= 0:
            # if not blocked up
            if board[r - 1][c][0] not in ["r", "b"]:
                # Move up left
                if c - 1 >= 0 and r - 2 >= 0:
                    if board[r - 2][c - 1][0] in move_valid:
                        self._moves.append((piece, (r, c), (r - 2, c - 1)))
                # Move up right
                if c + 1 <= 8:
                    if board[r - 2][c + 1][0] in move_valid:
                        self._moves.append((piece, (r, c), (r - 2, c + 1)))
        # check left in bounds
        if c - 2 >= 0:
            # if not blocked left
            if board[r][c - 1][0] not in ["r", "b"]:
                # Move left up
                if c - 2 >= 0 and r - 1 >= 0:
                    if board[r - 1][c - 2][0] in move_valid:
                        self._moves.append((piece, (r, c), (r - 1, c - 2)))
                # Move left down
                if c - 2 >= 0 and r + 1 <= 9:
                    if board[r + 1][c - 2][0] in move_valid:
                        self._moves.append((piece, (r, c), (r + 1, c - 2)))
        # check right in bounds
        if c + 2 <= 8:
            # if not blocked right
            if board[r][c + 1][0] not in ["r", "b"]:
                # Move right up
                if r - 1 >= 0 and c + 2 <= 8:
                    if board[r - 1][c + 2][0] in move_valid:
                        self._moves.append((piece, (r, c), (r - 1, c + 2)))
                # move right down
                if r + 1 <= 9 and c + 2 <= 8:
                    if board[r + 1][c + 2][0] in move_valid:
                        self._moves.append((piece, (r, c), (r + 1, c + 2)))
        # check bottom bounds
        if r + 2 <= 9:
            # if not blocked down
            if board[r + 1][c][0] not in ["r", "b"]:
                # move down left
                if c - 1 >= 0:
                    if board[r + 2][c - 1][0] in move_valid:
                        self._moves.append((piece, (r, c), (r + 2, c - 1)))
                # move down right
                if c + 1 <= 8:
                    if board[r + 2][c + 1][0] in move_valid:
                        self._moves.append((piece, (r, c), (r + 2, c + 1)))

    def get_guard_moves(self, r, c):
        """
        Gets all the valid moves for the guard piece
        """
        bg = "bG"
        rg = "rG"
        board = self._game.get_board()
        blue_move_valid = ["r", "-"]
        red_move_valid = ["b", "-"]
        moves = self._moves

        if self._game.get_turn():
            # if on 7,3
            # check right
            if r == 7 and c == 3:
                if board[r][c + 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c + 1)))
                # check diagonal
                if board[r + 1][c + 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r + 1, c + 1)))
                # check down
                if board[r + 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r + 1, c)))
            # if on 7,4
            if r == 7 and c == 4:
                # check right
                if board[r][c + 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c + 1)))
                # check down
                if board[r + 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r + 1, c)))
                # check left
                if board[r][c - 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c - 1)))
            # if on 7,5
            if r == 7 and c == 5:
                # check left
                if board[r][c - 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c - 1)))
                # check diagonal
                if board[r + 1][c - 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r + 1, c - 1)))
                # check down
                if board[r + 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r + 1, c)))
            # if on 8,3
            if r == 8 and c == 3:
                # check up
                if board[r - 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r - 1, c)))
                # check right
                if board[r][c + 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c + 1)))
                # check down
                if board[r + 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r + 1, c)))
            # if on 8,4
            if r == 8 and c == 4:
                # check up
                if board[r - 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r - 1, c)))
                # check diagonal up right
                if board[r - 1][c + 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r - 1, c + 1)))
                # check right
                if board[r][c + 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c + 1)))
                # check diagonal down right
                if board[r + 1][c + 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r + 1, c + 1)))
                # check down
                if board[r + 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r + 1, c)))
                # check diagonal down left
                if board[r + 1][c - 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r + 1, c - 1)))
                # check left
                if board[r][c - 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c - 1)))
                # check diagonal up left
                if board[r - 1][c - 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r - 1, c - 1)))
            # if on 8,5
            if r == 8 and c == 5:
                # check up
                if board[r - 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r - 1, c)))
                # check left
                if board[r][c - 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c - 1)))
                # check down
                if board[r + 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r + 1, c)))

            # if on 9,3
            if r == 9 and c == 3:
                # check right
                if board[r][c + 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c + 1)))
                # check diag up right
                if board[r - 1][c + 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r - 1, c + 1)))
                # check up
                if board[r - 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r - 1, c)))

            # if on 9,4
            if r == 9 and c == 4:
                # check left
                if board[r][c - 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c - 1)))
                # check right
                if board[r][c + 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c + 1)))
                # check up
                if board[r - 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r - 1, c)))

            # if on 9,5
            if r == 9 and c == 5:
                # check up
                if board[r - 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r - 1, c)))
                # check left
                if board[r][c - 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c - 1)))
                # check diag up left
                if board[r - 1][c - 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r - 1, c - 1)))

        if not self._game.get_turn():  # red turn
            # if on 2,7
            if r == 2 and c == 3:
                # check right
                if board[r][c + 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c + 1)))
                # check diagonal
                if board[r - 1][c + 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r - 1, c + 1)))
                # check up
                if board[r - 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r - 1, c)))
            # if on 3,4
            if r == 2 and c == 4:
                # check right
                if board[r][c + 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c + 1)))
                # check up
                if board[r - 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r - 1, c)))
                # check left
                if board[r][c - 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c - 1)))
            # if on 3,5
            if r == 2 and c == 5:
                # check left
                if board[r][c - 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c - 1)))
                # check diagonal
                if board[r - 1][c - 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r - 1, c - 1)))
                # check up
                if board[r - 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r - 1, c)))
            # if on 1,3
            if r == 1 and c == 3:
                # check up
                if board[r - 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r - 1, c)))
                # check right
                if board[r][c + 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c + 1)))
                # check down
                if board[r + 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r + 1, c)))
            # if on 1,4
            if r == 1 and c == 4:
                # check up
                if board[r - 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r - 1, c)))
                # check diagonal up right
                if board[r - 1][c + 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r - 1, c + 1)))
                # check right
                if board[r][c + 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c + 1)))
                # check diagonal down right
                if board[r + 1][c + 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r + 1, c + 1)))
                # check down
                if board[r + 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r + 1, c)))
                # check diagonal down left
                if board[r + 1][c - 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r + 1, c - 1)))
                # check left
                if board[r][c - 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c - 1)))
                # check diagonal up left
                if board[r - 1][c - 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r - 1, c - 1)))
            # if on 1,5
            if r == 1 and c == 5:
                # check up
                if board[r - 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r - 1, c)))
                # check left
                if board[r][c - 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c - 1)))
                # check down
                if board[r + 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r + 1, c)))

            # if on 0,3
            if r == 0 and c == 3:
                # check right
                if board[r][c + 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c + 1)))
                # check diag down right
                if board[r + 1][c + 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r + 1, c + 1)))
                # check down
                if board[r + 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r + 1, c)))

            # if on 0,4
            if r == 0 and c == 4:
                # check left
                if board[r][c - 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c - 1)))
                # check right
                if board[r][c + 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c + 1)))
                # check down
                if board[r + 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r + 1, c)))

            # if on 0,5
            if r == 0 and c == 5:
                # check down
                if board[r + 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r + 1, c)))
                # check left
                if board[r][c - 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c - 1)))
                # check diag down left
                if board[r + 1][c - 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r + 1, c - 1)))

    def get_general_moves(self, r, c):
        """
        Gets all the valid moves for the general piece
        """
        bg = "bK"
        rg = "rK"
        board = self._game.get_board()
        blue_move_valid = ["r", "-"]
        red_move_valid = ["b", "-"]
        moves = self._moves

        if self._game.get_turn():
            # if on 7,3
            # check right
            if r == 7 and c == 3:
                if board[r][c + 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c + 1)))
                # check diagonal
                if board[r + 1][c + 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r + 1, c + 1)))
                # check down
                if board[r + 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r + 1, c)))
            # if on 7,4
            if r == 7 and c == 4:
                # check right
                if board[r][c + 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c + 1)))
                # check down
                if board[r + 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r + 1, c)))
                # check left
                if board[r][c - 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c - 1)))
            # if on 7,5
            if r == 7 and c == 5:
                # check left
                if board[r][c - 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c - 1)))
                # check diagonal
                if board[r + 1][c - 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r + 1, c - 1)))
                # check down
                if board[r + 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r + 1, c)))
            # if on 8,3
            if r == 8 and c == 3:
                # check up
                if board[r - 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r - 1, c)))
                # check right
                if board[r][c + 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c + 1)))
                # check down
                if board[r + 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r + 1, c)))
            # if on 8,4
            if r == 8 and c == 4:
                # check up
                if board[r - 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r - 1, c)))
                # check diagonal up right
                if board[r - 1][c + 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r - 1, c + 1)))
                # check right
                if board[r][c + 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c + 1)))
                # check diagonal down right
                if board[r + 1][c + 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r + 1, c + 1)))
                # check down
                if board[r + 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r + 1, c)))
                # check diagonal down left
                if board[r + 1][c - 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r + 1, c - 1)))
                # check left
                if board[r][c - 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c - 1)))
                # check diagonal up left
                if board[r - 1][c - 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r - 1, c - 1)))
            # if on 8,5
            if r == 8 and c == 5:
                # check up
                if board[r - 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r - 1, c)))
                # check left
                if board[r][c - 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c - 1)))
                # check down
                if board[r + 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r + 1, c)))

            # if on 9,3
            if r == 9 and c == 3:
                # check right
                if board[r][c + 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c + 1)))
                # check diag up right
                if board[r - 1][c + 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r - 1, c + 1)))
                # check up
                if board[r - 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r - 1, c)))

            # if on 9,4
            if r == 9 and c == 4:
                # check left
                if board[r][c - 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c - 1)))
                # check right
                if board[r][c + 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), (r, c + 1)))
                # check up
                if board[r - 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), bg, (r - 1, c)))

            # if on 9,5
            if r == 9 and c == 5:
                # check up
                if board[r - 1][c][0] in blue_move_valid:
                    moves.append((bg, (r, c), bg, (r - 1, c)))
                # check left
                if board[r][c - 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), bg, (r, c - 1)))
                # check diag up left
                if board[r - 1][c - 1][0] in blue_move_valid:
                    moves.append((bg, (r, c), bg, (r - 1, c - 1)))

        if not self._game.get_turn():  # red turn
            # if on 2,7
            if r == 2 and c == 3:
                # check right
                if board[r][c + 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c + 1)))
                # check diagonal
                if board[r - 1][c + 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r - 1, c + 1)))
                # check up
                if board[r - 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r - 1, c)))
            # if on 3,4
            if r == 2 and c == 4:
                # check right
                if board[r][c + 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c + 1)))
                # check up
                if board[r - 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r - 1, c)))
                # check left
                if board[r][c - 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c - 1)))
            # if on 3,5
            if r == 2 and c == 5:
                # check left
                if board[r][c - 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c - 1)))
                # check diagonal
                if board[r - 1][c - 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r - 1, c - 1)))
                # check up
                if board[r - 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r - 1, c)))
            # if on 1,3
            if r == 1 and c == 3:
                # check up
                if board[r - 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r - 1, c)))
                # check right
                if board[r][c + 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c + 1)))
                # check down
                if board[r + 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r + 1, c)))
            # if on 1,4
            if r == 1 and c == 4:
                # check up
                if board[r - 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r - 1, c)))
                # check diagonal up right
                if board[r - 1][c + 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r - 1, c + 1)))
                # check right
                if board[r][c + 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c + 1)))
                # check diagonal down right
                if board[r + 1][c + 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r + 1, c + 1)))
                # check down
                if board[r + 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r + 1, c)))
                # check diagonal down left
                if board[r + 1][c - 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r + 1, c - 1)))
                # check left
                if board[r][c - 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c - 1)))
                # check diagonal up left
                if board[r - 1][c - 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r - 1, c - 1)))
            # if on 1,5
            if r == 1 and c == 5:
                # check up
                if board[r - 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r - 1, c)))
                # check left
                if board[r][c - 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c - 1)))
                # check down
                if board[r + 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r + 1, c)))

            # if on 0,3
            if r == 0 and c == 3:
                # check right
                if board[r][c + 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c + 1)))
                # check diag down right
                if board[r + 1][c + 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r + 1, c + 1)))
                # check down
                if board[r + 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r + 1, c)))

            # if on 0,4
            if r == 0 and c == 4:
                # check left
                if board[r][c - 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c - 1)))
                # check right
                if board[r][c + 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c + 1)))
                # check down
                if board[r + 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r + 1, c)))

            # if on 0,5
            if r == 0 and c == 5:
                # check down
                if board[r + 1][c][0] in red_move_valid:
                    moves.append((rg, (r, c), (r + 1, c)))
                # check left
                if board[r][c - 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r, c - 1)))
                # check diag down left
                if board[r + 1][c - 1][0] in red_move_valid:
                    moves.append((rg, (r, c), (r + 1, c - 1)))

    def get_cannon_moves(self, r, c):
        """
        Gets all the valid moves for the cannon piece
        """
        piece = "bF" if self._game.get_turn() else "rF"
        takeable = "r" if self._game.get_turn() else "b"
        board = self._game.get_board()
        move_valid = ["r", "-"] if self._game.get_turn() else ["b", "-"]
        moves = self._moves
        red_palace = self.get_red_palace_moves()
        blue_palace = self.get_blue_palace_moves()
        pieces_jumped = 0

        # move up
        pieces_jumped = 0
        for i in range(1, 11):
            if 0 <= r - i <= 9:
                if board[r - i][c][1] == "F":
                    break
                if pieces_jumped != 1:
                    board[r - i][c]
                    if board[r - i][c][0] in "rb":
                        pieces_jumped += 1
                else:
                    if pieces_jumped == 1:
                        if board[r - i][c][0] in piece:
                            break
                        elif board[r - i][c][0] == takeable:
                            moves.append((piece, (r, c), (r - i, c)))
                            break
                        else:
                            if board[r - i][c][0] in move_valid:
                                moves.append((piece, (r, c), (r - i, c)))
        # move down
        pieces_jumped = 0
        for i in range(1, 11):
            if 0 <= r + i <= 9:
                if board[r + i][c][1] == "F":
                    break
                if pieces_jumped != 1:
                    board[r + i][c]
                    if board[r + i][c][0] in "rb":
                        pieces_jumped += 1
                else:
                    if pieces_jumped == 1:
                        if board[r + i][c][0] in piece:
                            break
                        elif board[r + i][c][0] == takeable:
                            moves.append((piece, (r, c), (r + i, c)))
                            break
                        else:
                            if board[r + i][c][0] in move_valid:
                                moves.append((piece, (r, c), (r + i, c)))
        # move right
        pieces_jumped = 0
        for i in range(1, 10):
            if 0 <= c + i <= 8:
                if board[r][c + i][1] == "F":
                    break
                if pieces_jumped != 1:
                    board[r][c + i]
                    if board[r][c + i][0] in "rb":
                        pieces_jumped += 1
                else:
                    if pieces_jumped == 1:
                        if board[r][c + i][0] in piece:
                            break
                        elif board[r][c + i][0] == takeable:
                            moves.append((piece, (r, c), (r, c + i)))
                            break
                        else:
                            if board[r][c + i][0] in move_valid:
                                moves.append((piece, (r, c), (r, c + i)))

        # move left
        pieces_jumped = 0
        for i in range(1, 10):
            if 0 <= c - i <= 8:
                if board[r][c - i][1] == "F":
                    break
                if pieces_jumped != 1:
                    board[r][c - i]
                    if board[r][c - i][0] in "rb":
                        pieces_jumped += 1
                else:
                    if pieces_jumped == 1:
                        if board[r][c - i][0] in piece:
                            break
                        elif board[r][c - i][0] == takeable:
                            moves.append((piece, (r, c), (r, c - i)))
                            break
                        else:
                            if board[r][c - i][0] in move_valid:
                                moves.append((piece, (r, c), (r, c - i)))

        # if in red palace

        # if in palace can move diagonally up to the right
        if (
            (r, c) in red_palace
            and (r - 2 >= 0 or r - 1 >= 0)
            and (c + 2 <= 5 or c + 1 <= 5)
            and (r, c) not in [(3, 1), (4, 0), (5, 1), (4, 2)]
        ):
            pieces_jumped = 0
            for i in range(1, 3):
                if board[r - i][c + i][1] == "F":
                    break
                if pieces_jumped != 1:
                    board[r - i][c + i]
                    if board[r - i][c + i][0] in "rb":
                        pieces_jumped += 1
                else:
                    if board[r - i][c + i][0] in piece:
                        break
                    elif board[r - i][c + i][0] == takeable:
                        moves.append((piece, (r, c), (r - i, c + i)))
                        break
                    else:
                        if board[r - i][c + i][0] in move_valid:
                            moves.append((piece, (r, c), (r - i, c + i)))
        # if in palace can move diagonally up to the left
        if (
            (r, c) in red_palace
            and (r - 2 >= 0 or r - 1 >= 0)
            and (c - 2 >= 3 or c - 1 >= 3)
            and (r, c) not in [(3, 1), (4, 0), (5, 1), (4, 2)]
        ):
            pieces_jumped = 0
            for i in range(1, 3):
                if board[r - i][c - i][1] == "F":
                    break
                if pieces_jumped != 1:
                    board[r - i][c - i]
                    if board[r - i][c - i][0] in "rb":
                        pieces_jumped += 1
                else:
                    if board[r - i][c - i][0] in piece:
                        break
                    elif board[r - i][c - i][0] == takeable:
                        moves.append((piece, (r, c), (r - i, c + i)))
                        break
                    else:
                        if board[r - i][c - i][0] in move_valid:
                            moves.append((piece, (r, c), (r - i, c - i)))
        # if in palace can move diagonally down to the left
        if (
            (r, c) in red_palace
            and (r + 2 <= 2 or r + 1 <= 2)
            and (c - 2 >= 3 or c - 1 >= 3)
            and (r, c) not in [(3, 1), (4, 0), (5, 1), (4, 2)]
        ):
            pieces_jumped = 0
            for i in range(1, 3):
                if board[r + i][c - i][1] == "F":
                    break
                if pieces_jumped != 1:
                    board[r + i][c - i]
                    if board[r + i][c - i][0] in "rb":
                        pieces_jumped += 1
                else:
                    if board[r + i][c - i][0] in piece:
                        break
                    elif board[r + i][c - i][0] == takeable:
                        moves.append((piece, (r, c), (r - i, c - i)))
                        break
                    else:
                        if board[r + i][c - i][0] in move_valid:
                            moves.append((piece, (r, c), (r + i, c - i)))
        # if in palace can move diag down to right
        if (
            (r, c) in red_palace
            and (r + 2 <= 2 or r + 1 <= 2)
            and (c + 2 <= 5 or c + 1 <= 5)
            and (r, c) not in [(3, 1), (4, 0), (5, 1), (4, 2)]
        ):
            pieces_jumped = 0
            for i in range(1, 3):
                if board[r + i][c + i][1] == "F":
                    break
                if pieces_jumped != 1:
                    board[r + i][c + i]
                    if board[r + i][c + i][0] in "rb":
                        pieces_jumped += 1
                else:
                    if board[r + i][c + i][0] in piece:
                        break
                    elif board[r + i][c + i][0] == takeable:
                        moves.append((piece, (r, c), (r - i, c + i)))
                        break
                    else:
                        if board[r + i][c + i][0] in move_valid:
                            moves.append((piece, (r, c), (r + i, c + i)))

        # if in blue palace

        # if in palace can move diagonally up to the right
        if (
            (r, c) in blue_palace
            and (r - 2 >= 7 or r - 1 >= 7)
            and (c + 2 <= 5 or c + 1 <= 5)
            and (r, c) not in [(7, 4), (8, 3), (8, 5), (9, 4)]
        ):
            pieces_jumped = 0
            for i in range(1, 3):
                if board[r - i][c + i][1] == "F":
                    break
                if pieces_jumped != 1:
                    board[r - i][c + i]
                    if board[r - i][c + i][0] in "rb":
                        pieces_jumped += 1
                else:
                    if board[r - i][c + i][0] in piece:
                        break
                    elif board[r - i][c + i][0] == takeable:
                        moves.append((piece, (r, c), (r - i, c + i)))
                        break
                    else:
                        if board[r - i][c + i][0] in move_valid:
                            moves.append((piece, (r, c), (r - i, c + i)))
        # if in palace can move diagonally up to the left
        if (
            (r, c) in blue_palace
            and (r - 2 >= 7 or r - 1 >= 7)
            and (c - 2 >= 3 or c - 1 >= 3)
            and (r, c) not in [(7, 4), (8, 3), (8, 5), (9, 4)]
        ):
            pieces_jumped = 0
            for i in range(1, 3):
                if board[r - i][c - i][1] == "F":
                    break
                if pieces_jumped != 1:
                    board[r - i][c - i]
                    if board[r - i][c - i][0] in "rb":
                        pieces_jumped += 1
                else:
                    if board[r - i][c - i][0] in piece:
                        break
                    elif board[r - i][c - i][0] == takeable:
                        moves.append((piece, (r, c), (r - i, c + i)))
                        break
                    else:
                        if board[r - i][c - i][0] in move_valid:
                            moves.append((piece, (r, c), (r - i, c - i)))
        # if in palace can move diagonally down to the left
        if (
            (r, c) in blue_palace
            and (r + 2 <= 0 or r + 1 <= 0)
            and (c - 2 >= 3 or c - 1 >= 3)
            and (r, c) not in [(7, 4), (8, 3), (8, 5), (9, 4)]
        ):
            pieces_jumped = 0
            for i in range(1, 3):
                if board[r + i][c - i][1] == "F":
                    break
                if pieces_jumped != 1:
                    board[r + i][c - i]
                    if board[r + i][c - i][0] in "rb":
                        pieces_jumped += 1
                else:
                    if board[r + i][c - i][0] in piece:
                        break
                    elif board[r + i][c - i][0] == takeable:
                        moves.append((piece, (r, c), (r - i, c - i)))
                        break
                    else:
                        if board[r + i][c - i][0] in move_valid:
                            moves.append((piece, (r, c), (r + i, c - i)))
        # if in palace can move diag down to right
        if (
            (r, c) in blue_palace
            and (r + 2 <= 0 or r + 1 <= 0)
            and (c + 2 <= 5 or c + 1 <= 5)
            and (r, c) not in [(7, 4), (8, 3), (8, 5), (9, 4)]
        ):
            pieces_jumped = 0
            for i in range(1, 3):
                if board[r + i][c + i][1] == "F":
                    break
                if pieces_jumped != 1:
                    board[r + i][c + i]
                    if board[r + i][c + i][0] in "rb":
                        pieces_jumped += 1
                else:
                    if board[r + i][c + i][0] in piece:
                        break
                    elif board[r + i][c + i][0] == takeable:
                        moves.append((piece, (r, c), (r + i, c + i)))
                        break
                    else:
                        if board[r + i][c + i][0] in move_valid:
                            moves.append((piece, (r, c), (r + i, c + i)))

    def get_soldier_moves(self, r, c):
        """
        Gets all the valid moves for the soldier piece
        """
        piece = "bS" if self._game.get_turn() else "rS"
        valid_move = ["r", "-"] if self._game.get_turn() else ["b", "-"]

        if self._game.get_turn():  # if blue turn
            red_palace = self.get_red_palace_moves()
            # if on final row
            if r == 0:
                # check boundaries
                if c - 1 >= 0:
                    if self._game.get_board()[r][c - 1][0] in valid_move:
                        self._moves.append((piece, (r, c), (r, c - 1)))
                if c + 1 <= 8:
                    if self._game.get_board()[r][c + 1][0] in valid_move:
                        self._moves.append((piece, (r, c), (r, c + 1)))
            # forward move
            if r - 1 >= 0:
                if self._game.get_board()[r - 1][c][0] in valid_move:
                    self._moves.append((piece, (r, c), (r - 1, c)))
            # left horizonal move
            if c - 1 >= 0:
                if self._game.get_board()[r][c - 1][0] in valid_move:
                    self._moves.append((piece, (r, c), (r, c - 1)))
            # right horizonal move
            if c + 1 <= 8:
                if self._game.get_board()[r][c + 1][0] in valid_move:
                    self._moves.append((piece, (r, c), (r, c + 1)))
            # if in palace can move diagonally forward to the right
            if (
                (r, c) in red_palace
                and r - 1 >= 0
                and c + 1 <= 5
                and (r, c) not in [(3, 1), (4, 0), (5, 1), (4, 2)]
            ):
                if self._game.get_board()[r - 1][c + 1] in valid_move:
                    self._moves.append((piece, (r, c), (r - 1, c + 1)))
            # if in palace can move diagonally forward to the left
            if (
                (r, c) in red_palace
                and r - 1 >= 0
                and c - 1 >= 3
                and (r, c) not in [(3, 1), (4, 0), (5, 1), (4, 2)]
            ):
                if self._game.get_board()[r - 1][c - 1] in valid_move:
                    self._moves.append((piece, (r, c), (r - 1, c - 1)))

        if not self._game.get_turn():
            # if not self._g.get_turn(): # if red turn
            blue_palace = self.get_blue_palace_moves()
            # if on final row
            if r == 9:
                if c - 1 >= 0:
                    if self._game.get_board()[r][c - 1][0] in valid_move:
                        self._moves.append((piece, (r, c), (r, c - 1)))
                if c + 1 <= 8:
                    if self._game.get_board()[r][c + 1][0] in valid_move:
                        self._moves.append((piece, (r, c), (r, c + 1)))
            # forward move
            if r + 1 >= 0:
                if self._game.get_board()[r + 1][c][0] in valid_move:
                    self._moves.append((piece, (r, c), (r + 1, c)))
            # left horizonal move
            if c - 1 >= 0:
                if self._game.get_board()[r][c - 1][0] in valid_move:
                    self._moves.append((piece, (r, c), (r, c - 1)))
            # right horizonal move
            if c + 1 <= 8:
                if self._game.get_board()[r][c + 1][0] in valid_move:
                    self._moves.append((piece, (r, c), (r, c + 1)))
            # if in palace can move diagonally forward to the right
            if (
                (r, c) in blue_palace
                and r + 1 <= 9
                and c + 1 <= 5
                and (r, c) not in [(7, 4), (8, 3), (8, 5), (9, 4)]
            ):
                if self._game.get_board()[r + 1][c + 1] in valid_move:
                    self._moves.append((piece, (r, c), (r + 1, c + 1)))
            # if in palace can move diagonally forward to the left
            if (
                (r, c) in blue_palace
                and r + 1 <= 9
                and c - 1 >= 3
                and (r, c) not in [(7, 4), (8, 3), (8, 5), (9, 4)]
            ):
                if self._game.get_board()[r + 1][c - 1] in valid_move:
                    self._moves.append((piece, (r, c), (r + 1, c - 1)))

    def get_red_palace_moves(self):
        """
        Creates a list of all the moves in the red palace
        """
        red_palace_moves = [
            (0, 3),
            (0, 4),
            (0, 5),
            (1, 3),
            (1, 4),
            (1, 5),
            (2, 3),
            (2, 4),
            (2, 5),
        ]
        return red_palace_moves

    def get_blue_palace_moves(self):
        """
        Creates a list of all the moves in the blue palace
        """
        blue_palace_moves = [
            (7, 3),
            (7, 4),
            (7, 5),
            (8, 3),
            (8, 4),
            (8, 5),
            (8, 3),
            (8, 4),
            (8, 5),
        ]
        return blue_palace_moves


if __name__ == "__main__":

    g = JanggiGame()


    g.make_move('a7', 'a6')


    g.print_board()