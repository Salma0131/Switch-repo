from Matrix import Matrix
import random
COIN = "coin"
DOT = "."
WALL = "wall"
PLAYER1 = "player1"
PLAYER2 = "player2"
MIN_SCORE = 10
MAX_SCORE = 100
DOWN = "down"
UP = "up"
LEFT = "left"
RIGHT = "right"


class GoldRush(Matrix):

    def __init__(self, rows, cols):
        super().__init__(rows, cols)
        self.score_player1 = 0
        self.score_player2 = 0
        self.winner = ""
        self.total_coins = 0

    def load_board(self):
        if self.rows == 0 and self.cols == 0:
            self.matrix = []
            return

        self.matrix = []
        elements = [COIN, DOT, WALL]
        coins = 0

        for row in range(self.rows):
            self.matrix.append([])
            for col in range(self.cols):
                if row % 2 != 0:
                    rand_index = random.randint(0, 1)
                    rand_element = elements[rand_index]
                    self.matrix[row].append(rand_element)
                    if rand_element == COIN:
                        coins += 1
                else:
                    self.matrix[row].append(elements[2])

            rand = random.randint(1, 2)
            for rand_col in range(1, self.cols, rand):
                rand += 1
                rand_index = random.randint(0, 1)
                rand_element = elements[rand_index]
                self.matrix[row][rand_col] = rand_element
                if rand_element == COIN:
                    coins += 1

        self.matrix[0][0] = PLAYER1
        self.matrix[self.rows - 1][self.cols - 1] = PLAYER2
        self.total_coins = coins

        if coins < MIN_SCORE:
            return self.load_board()
        else:
            return self.matrix

    def _check_winner(self, player):
        player_num = player[-1]
        score = getattr(self, f"score_player{player_num}")
        if score == MAX_SCORE:
            self.winner = player
            return self.winner

    def _check_other_player(self, player):
        otherPlayer = None
        if player == PLAYER1:
            otherPlayer = PLAYER2
            return otherPlayer
        elif player == PLAYER2:
            otherPlayer = PLAYER1
            return otherPlayer

    def _move_update_score(self, curr_row, curr_col, player, delta_row, delta_col):
        other_player = self._check_other_player(player)
        new_row, new_col = curr_row + delta_row, curr_col + delta_col

        if not (0 <= new_row < self.rows and 0 <= new_col < self.cols):
            return

        if self.matrix[new_row][new_col] not in [WALL, other_player]:
            if self.matrix[new_row][new_col] == COIN:
                self._update_score(player)

            self.matrix[curr_row][curr_col] = "."
            self.matrix[new_row][new_col] = player

        return self._check_winner(player)

    def _move_down(self, curr_row, curr_col, player):
        return self._move_update_score(curr_row, curr_col, player, 1, 0)

    def _move_up(self, curr_row, curr_col, player):
        return self._move_update_score(curr_row, curr_col, player, -1, 0)

    def _move_right(self, curr_row, curr_col, player):
        return self._move_update_score(curr_row, curr_col, player, 0, 1)

    def _move_left(self, curr_row, curr_col, player):
        return self._move_update_score(curr_row, curr_col, player, 0, -1)

    def move_player(self, player, direction):
        curr_row, curr_col = None, None

        for i, row in enumerate(self.matrix):
            for j, value in enumerate(row):
                if value == player:
                    curr_row, curr_col = i, j
                    break
            if curr_row is not None:
                break

        if direction == DOWN:
            self._move_down(curr_row, curr_col, player)
        elif direction == UP:
            self._move_up(curr_row, curr_col, player)
        elif direction == RIGHT:
            self._move_right(curr_row, curr_col, player)
        elif direction == LEFT:
            self._move_left(curr_row, curr_col, player)

    def _update_score(self, player):
        player_num = player[-1]
        score_attr = f"score{player_num}"
        setattr(self, score_attr, getattr(self, score_attr) + 10)
        print(getattr(self, score_attr))
