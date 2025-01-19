
import random # Імпортуємо модуль random для (хоча тут не використовується, залишено для можливих майбутніх розширень)

def print_board(board):
    """Функція для виведення ігрового поля на екран."""
    for row in board: # Ітеруємось по кожному рядку дошки
        print("|".join(row)) # Виводимо рядок, розділяючи клітинки символом "|"
        print("-" * 5) # Виводимо розділову лінію між рядками

def check_winner(board, player):
    """Функція для перевірки, чи є переможець."""
    for row in board: # Перевірка рядків
        if all(cell == player for cell in row): # Якщо всі клітинки в рядку рівні гравцю, то він переміг
            return True
    for col in range(3): # Перевірка стовпців
        if all(board[row][col] == player for row in range(3)): # Якщо всі клітинки в стовпці рівні гравцю, то він переміг
            return True
    if all(board[i][i] == player for i in range(3)) or all(board[i][2 - i] == player for i in range(3)): # Перевірка діагоналей
        return True
    return False # Якщо жодна з умов не виконана, переможця немає

def is_board_full(board):
    """Функція для перевірки, чи заповнена дошка."""
    return all(all(cell != " " for cell in row) for row in board) # Повертає True, якщо всі клітинки не порожні

def get_available_moves(board):
    """Функція для отримання списку доступних ходів."""
    moves = [] # Створюємо пустий список для ходів
    for row in range(3): # Ітеруємось по рядках
        for col in range(3): # Ітеруємось по стовпцях
            if board[row][col] == " ": # Якщо клітинка порожня
                moves.append((row, col)) # Додаємо координати клітинки до списку ходів
    return moves # Повертаємо список доступних ходів

def minimax(board, depth, is_maximizing, memo):
    """Алгоритм мінімакс з мемоізацією."""
    board_tuple = tuple(map(tuple, board)) # Перетворюємо дошку в кортеж кортежів для використання як ключа в memo
    if board_tuple in memo: # Перевіряємо, чи результат для цього стану вже обчислений
        return memo[board_tuple] # Якщо так, повертаємо збережений результат

    if check_winner(board, "X"): # Якщо переміг "X" (людина), повертаємо -1
        return -1
    if check_winner(board, "O"): # Якщо переміг "O" (комп'ютер), повертаємо 1
        return 1
    if is_board_full(board): # Якщо дошка повна, повертаємо 0 (нічия)
        return 0

    if is_maximizing: # Якщо зараз хід комп'ютера (максимізація)
        best_score = -float('inf') # Ініціалізуємо найкращий рахунок як мінус нескінченність
        for move in get_available_moves(board): # Ітеруємось по доступних ходах
            row, col = move # Отримуємо координати ходу
            board[row][col] = "O" # Робимо хід на дошці
            score = minimax(board, depth + 1, False, memo) # Рекурсивно викликаємо мінімакс для наступного ходу (мінімізація)
            board[row][col] = " " # Відміняємо зроблений хід (важливо для коректної роботи алгоритму)
            best_score = max(best_score, score) # Оновлюємо найкращий рахунок, вибираючи максимум
        memo[board_tuple] = best_score # Запам'ятовуємо результат для цього стану дошки
        return best_score # Повертаємо найкращий рахунок
    else: # Якщо зараз хід людини (мінімізація)
        best_score = float('inf') # Ініціалізуємо найкращий рахунок як плюс нескінченність
        for move in get_available_moves(board): # Ітеруємось по доступних ходах
            row, col = move # Отримуємо координати ходу
            board[row][col] = "X" # Робимо хід на дошці
            score = minimax(board, depth + 1, True, memo) # Рекурсивно викликаємо мінімакс для наступного ходу (максимізація)
            board[row][col] = " " # Відміняємо зроблений хід
            best_score = min(best_score, score) # Оновлюємо найкращий рахунок, вибираючи мінімум
        memo[board_tuple] = best_score # Запам'ятовуємо результат для цього стану дошки
        return best_score # Повертаємо найкращий рахунок

def get_best_move(board):
    """Функція для отримання найкращого ходу для комп'ютера."""
    best_score = -float('inf') # Ініціалізуємо найкращий рахунок
    best_move = None # Ініціалізуємо найкращий хід
    memo = {} # Створюємо словник для мемоізації
    for move in get_available_moves(board): # Ітеруємось по доступних ходах
        row, col = move # Отримуємо координати ходу
        board[row][col] = "O" # Робимо хід на дошці
        score = minimax(board, 0, False, memo) # Обчислюємо рахунок за допомогою мінімакс
        board[row][col] = " " # Відміняємо зроблений хід
        if score > best_score: # Якщо знайдено кращий рахунок
            best_score = score # Оновлюємо найкращий рахунок
            best_move = move # Оновлюємо найкращий хід
    return best_move # Повертаємо найкращий хід

def play_game():
    """Функція для запуску гри."""
    board = [[" " for _ in range(3)] for _ in range(3)] # Створюємо пусту дошку 3x3
    player_turn = "X" # Встановлюємо початкового гравця ("X" - людина)

    while True: # Основний цикл гри
        print_board(board) # Виводимо дошку на екран
        if player_turn == "X": # Якщо хід людини
            while True: # Цикл для валідації вводу користувача
                try:
                    row = int(input("Введіть рядок (0-2): ")) # Отримуємо рядок від користувача
                    col = int(input("Введіть стовпчик (0-2): ")) # Отримуємо стовпчик від користувача
                    if board[row][col] == " ": # Якщо клітинка вільна
                        board[row][col] = "X" # Робимо хід людини
                        break # Виходимо з циклу валідації
                    else:
                        print("Клітинка вже зайнята!") # Повідомляємо, що клітинка зайнята
                except (ValueError, IndexError): # Обробка помилок вводу
                    print("Некоректний ввід. Введіть числа від 0 до 2.") # Повідомляємо про некоректний ввід
        else: # Якщо хід комп'ютера
            print("Хід комп'ютера...") # Виводимо повідомлення про хід комп'ютера
            best_move = get_best_move(board) # Отримуємо найкращий хід від комп'ютера
            if best_move: # Якщо є доступні ходи
                row, col = best_move # Отримуємо координати ходу
                board[row][col] = "O" # Робимо хід комп'ютера
            else: # Якщо немає доступних ходів (нічия)
                break # Виходимо з циклу гри

        if check_winner(board, player_turn): # Перевіряємо, чи є переможець
            print_board(board) # Виводимо дошку
            print(f"Переміг гравець {player_turn}!") # Виводимо повідомлення            break
        if is_board_full(board):
            print_board(board)
            print("Нічия!")
            break

        player_turn = "O" if player_turn == "X" else "X"

if __name__ == "__main__":
    play_game()