import random


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None

    def append(self, data):
        new_node = Node(data)
        if not self.head:
            self.head = new_node
            return
        curr_node = self.head
        while curr_node.next:
            curr_node = curr_node.next
        curr_node.next = new_node


class Board:

    def __init__(self, n):
        self.n: int = n
        self.board = self.create_board()

    def print_board(self):
        print()
        curr_row = self.board.head
        while curr_row:
            curr_node = curr_row.data.head
            row_str = ''
            while curr_node:
                if curr_node.data is None:
                    row_str += '|   |'
                elif curr_node.data == "\U0001F47D\U0001F916":
                    row_str += f"|{curr_node.data}|"
                else:
                    row_str += f"| {curr_node.data} |"
                curr_node = curr_node.next
            print(row_str)
            curr_row = curr_row.next
        print()

    def create_board(self):
        board = LinkedList()
        for i in range(self.n):
            row = LinkedList()
            for j in range(self.n):
                row.append(None)
            board.append(row)
        return board

    def add_symbols(self):
        white_spaces = self.n * self.n - 2 * self.n
        symbols = ['+'] * self.n + ['-'] * self.n + [' '] * white_spaces

        random.shuffle(symbols)
        curr_row = self.board.head
        while curr_row:
            curr_node = curr_row.data.head
            while curr_node:
                if symbols and curr_node.data is None:
                    curr_node.data = symbols.pop()
                curr_node = curr_node.next
            curr_row = curr_row.next

    def add_predator(self) -> (int, int):
        empty_cells = []
        curr_row = self.board.head
        row_index = 0

        while curr_row:
            curr_node = curr_row.data.head
            col_index = 0

            while curr_node:
                if curr_node.data == ' ':
                    empty_cells.append((row_index, col_index))
                col_index += 1
                curr_node = curr_node.next
            row_index += 1
            curr_row = curr_row.next

        if empty_cells:
            row, col = random.choice(empty_cells)
            self.set_cell(row, col, '\U0001F916')
            return row, col

    def get_alien_start_position(self) -> (int, int):
        print('Ingresa la fila y la columna donde quieres aparecer.')
        while True:
            row = int(input('Fila: ')) - 1
            col = int(input('Columna: ')) - 1
            if self.is_valid_cell(row, col):
                self.set_cell(row, col, '\U0001F47D')
                return row, col
            else:
                print('Posición inválida. Intente de nuevo.')

    def is_valid_cell(self, row, col) -> bool:
        return 0 <= row < self.n and 0 <= col < self.n

    def set_cell(self, row, col, value):
        curr_row = self.board.head
        for _ in range(row):
            curr_row = curr_row.next

        curr_node = curr_row.data.head
        for _ in range(col):
            curr_node = curr_node.next

        curr_node.data = value

    def get_cell_value(self, row, col) -> str:
        curr_row = self.board.head
        for _ in range(row):
            curr_row = curr_row.next

        curr_node = curr_row.data.head
        for _ in range(col):
            curr_node = curr_node.next

        return curr_node.data


class Game:

    def __init__(self):
        self.board = None
        self.alien_pos = None
        self.predator_pos = None
        self.alien_life = 50
        self.predator_life = 50

    def get_alien_start_position(self):
        self.alien_pos = self.board.get_alien_start_position()

    def add_predator(self):
        self.predator_pos = self.board.add_predator()

    def move_predator(self):
        row, col = self.predator_pos
        possible_moves = [(row-1, col), (row+1, col), (row, col-1), (row, col+1),
                          (row-1, col-1), (row-1, col+1), (row+1, col-1), (row+1, col+1)]
        valid_moves = []
        for move in possible_moves:
            if self.board.is_valid_cell(move[0], move[1]):
                valid_moves.append(move)
        if not valid_moves:
            return
        new_row, new_col = random.choice(valid_moves)
        if self.board.get_cell_value(self.predator_pos[0], self.predator_pos[1]) == '\U0001F47D\U0001F916':
            self.board.set_cell(self.predator_pos[0], self.predator_pos[1], '\U0001F47D')
        else:
            self.board.set_cell(self.predator_pos[0], self.predator_pos[1], None)
        cell_value = self.board.get_cell_value(new_row, new_col)

        if cell_value == '+':
            self.predator_life += 10
            self.board.set_cell(new_row, new_col, '\U0001F916')
            print('El Depredador se movió a una casilla con un "+". Su vida aumentó a', self.predator_life)

        elif cell_value == '-':
            self.predator_life -= 10
            self.board.set_cell(new_row, new_col, '\U0001F916')
            print('El Depredador se movió a una casilla con un "-". Su vida disminuyó a', self.predator_life)

        elif cell_value == '\U0001F47D':
            self.alien_life -= 25
            self.board.set_cell(new_row, new_col, '\U0001F47D\U0001F916')
            print('El Depredador se movió a la casilla donde está el Alien. La vida del Alien disminuyó a', self.alien_life)

        else:
            self.board.set_cell(new_row, new_col, '\U0001F916')
            print('El Depredador se movió a una casilla vacía.')
        self.predator_pos = (new_row, new_col)

    def move_alien(self):
        while True:
            direction = input('Ingrese la dirección en la que quiere mover al Alien (utilice WASD): ').lower()
            new_row, new_col = self.alien_pos
            if direction == 'w':
                new_row -= 1
            elif direction == 's':
                new_row += 1
            elif direction == 'a':
                new_col -= 1
            elif direction == 'd':
                new_col += 1
            else:
                print('Dirección inválida. Intente de nuevo.')
                continue

            if self.board.is_valid_cell(new_row, new_col):
                if self.board.get_cell_value(self.alien_pos[0], self.alien_pos[1]) == '\U0001F47D\U0001F916':
                    self.board.set_cell(self.alien_pos[0], self.alien_pos[1], '\U0001F916')
                else:
                    self.board.set_cell(self.alien_pos[0], self.alien_pos[1], None)

                cell_value = self.board.get_cell_value(new_row, new_col)
                if cell_value == '+':
                    self.alien_life += 10
                    self.board.set_cell(new_row, new_col, '\U0001F47D')
                    print('El Alien se movió a una casilla con un "+". Su vida aumentó a', self.alien_life)

                elif cell_value == '-':
                    self.alien_life -= 10
                    self.board.set_cell(new_row, new_col, '\U0001F47D')
                    print('El Alien se movió a una casilla con un "-". Su vida disminuyó a', self.alien_life)

                elif cell_value == '\U0001F916':
                    self.alien_life -= 25
                    self.board.set_cell(new_row, new_col, '\U0001F47D\U0001F916')
                    print('El Alien se movió a la casilla donde está el Depredador. Su vida disminuyó a', self.alien_life)

                else:
                    self.board.set_cell(new_row, new_col, '\U0001F47D')
                    print('El Alien se movió a una casilla vacía.')
                self.alien_pos = (new_row, new_col)
                return
            else:
                print('La casilla a la que intenas moverte no existe. Intente de nuevo.')

    def attack_predator(self):
        row, col = self.alien_pos
        possible_attacks = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
        for attack in possible_attacks:
            if self.board.is_valid_cell(attack[0], attack[1]) \
                    and self.board.get_cell_value(attack[0], attack[1]) == '\U0001F916':
                self.predator_life -= 10
                print('El Alien atacó al Depredador. La vida del Depredador disminuyó a', self.predator_life)
                return
        print('El Alien no puede atacar al Depredador en este turno.')

    def preparing_game(self):
        n = int(input('Ingrese el tamaño del tablero: '))
        self.board = Board(n)
        self.board.add_symbols()
        self.add_predator()
        print('¡El depredador ha aparecido!')
        self.board.print_board()
        self.get_alien_start_position()
        print('Posición inicial:')
        self.board.print_board()
        input("Pulsa enter para continuar.")

    def aliens_turn(self):
        print('\n--- Turno del Alien ---')
        print('Vida del Alien: ', self.alien_life)
        print('Vida del Depredador: ', self.predator_life, "\n")

        while True:
            action = input('Ingrese la acción que quiere realizar el Alien (mover o atacar): ')
            if action == 'mover':
                self.move_alien()
                break
            elif action == 'atacar':
                self.attack_predator()
                break
            else:
                print('Acción inválida. Intente de nuevo.')
        print('Tablero después del turno del Alien:')
        self.board.print_board()
        input("Pulsa enter para continuar.")

    def predators_turn(self):
        print('\n--- Turno del Depredador ---')
        print('Vida del Alien: ', self.alien_life)
        print('Vida del Depredador: ', self.predator_life, "\n")

        self.move_predator()
        print('Tablero después del turno del Depredador:')
        self.board.print_board()

    def game_is_over(self) -> bool:
        if self.alien_life <= 0:
            print("\n  === FIN DEL JUEGO ===\n")
            print('Has perdido. El Depredador ganó')
            return True
        elif self.predator_life <= 0:
            print("\n  === FIN DEL JUEGO ===\n")
            print('¡Felicidades, El Alien ganó!')
            return True
        return False

    def play(self):
        self.preparing_game()
        while True:
            self.predators_turn()
            if self.game_is_over():
                break
            self.aliens_turn()
            if self.game_is_over():
                break


game = Game()
game.play()
