import tkinter as tk
from tkinter import font
from tkinter import messagebox
import random

# Inisialisasi aplikasi
root = tk.Tk()
root.title("Tic Tac Toe")
root.resizable(False, False)
root.geometry("360x640")
root.eval("tk::PlaceWindow . center")
bold_large_font = font.Font(family="Arial", size=20, weight="bold")
bold_font = font.Font(family="Arial", size=11, weight="bold")

#Variable Global
board = [" " for _ in range(9)] # Papan permainan Tic Tac Toe dengan list berukuran 9
buttons = []  # Menyimpan tombol-tombol untuk papan Tic Tac Toe
game_started = False  # Status apakah permainan sedang berjalan
player_turn = "X"  # Menyimpan giliran pemain (X atau O)
mode = tk.StringVar(value="2 Player")  # Variabel untuk menyimpan mode permainan
difficulty = tk.StringVar(value="Easy")  # Variabel untuk menyimpan tingkat kesulitan
player_1_score = 0
player_2_score = 0
ai_score = 0
timer_label = None  # Label untuk menampilkan timer
time_left = 10      # Waktu (dalam detik) untuk setiap giliran
timer_running = False  # Status apakah timer sedang berjalan
after_id = None  # ID untuk menyimpan instance timer yang sedang berjalan
leaderboard = []  # Format: [{"name": "Player", "score": 2, "time": 10}]

# Inisialisasi Warna Aplikasi
BG_COLOR = "#0D92F4"  # Warna latar belakang
FG_COLOR = "#ffffff"  # Warna teks
BOARD_COLOR = "#d1d1d1"  # Warna board
BUTTON_COLOR = "#FF7F3E" # Warna button
BUTTON_TEXT_COLOR = "#ffffff"  # Warna teks tombol

#root warna
#warna ini digunakan untuk menciptakan tampilan konsisten di seluruh aplikasi, 
#termasuk jendela utama dan elemen-elemen UI seperti tombol dan label.
root.configure(bg=BG_COLOR)

# Fungsi untuk menampilkan halaman selamat datang
def show_welcome_page():
    #Menampilkan halaman selamat datang.
    welcome_frame = tk.Frame(
        root, 
        bg=BG_COLOR
    )
    
    welcome_frame.pack(
        expand=True,
    )

    #Tampilin Teks judul Selamat Datang
    welcome_label = tk.Label(
        welcome_frame, 
        text="Selamat Datang\nDi Game XOX", 
        font=bold_large_font,
        bg=BG_COLOR, 
        fg=FG_COLOR
    )

    welcome_label.pack(
        padx=20, 
       anchor='center'
    )

    #Tampilin Teks judul kelompok 2
    welcome_label = tk.Label(
        welcome_frame, 
        text="Kelompok 2", 
        font=bold_large_font,
        fg=BUTTON_TEXT_COLOR,
        bg=BUTTON_COLOR
    )
    
    welcome_label.pack(
        pady=10, 
    )
    
    # Tombol untuk memulai permainan
    start_button = tk.Button(
        welcome_frame, 
        text="Masuk",
        font=bold_font, 
        command=lambda: start_game(welcome_frame),
        bg=BUTTON_COLOR, 
        fg=BUTTON_TEXT_COLOR,
        width=12
    )

    start_button.pack(pady=75, anchor='center')

# Fungsi untuk memulai permainan (berpindah dari halaman welcome ke game)
def start_game(welcome_frame):
    #Awalan Game Memulai
    welcome_frame.destroy() # Menghapus halaman selamat datang
    create_game_interface() # Membuat tampilan antarmuka permainan

def start_game_action():
    global game_started, player_1_score, player_2_score, ai_score
    
    if not game_started:
        # Reset skor
        player_1_score = 0
        player_2_score = 0
        ai_score = 0
        update_score_display()  # Perbarui tampilan skor

        game_started = True  # Permainan dimulai
        reset_board()  # Reset papan permainan
        reset_timer()  # Reset dan mulai timer
        start_timer()  # Memulai timer

def start_timer():
    global timer_running
    if not timer_running:  # Mulai timer hanya jika belum berjalan
        timer_running = True
        update_timer()  # Mulai hitungan mundur

def update_timer():
    global time_left, timer_running, after_id, player_turn

    if not game_started:  # Pastikan permainan telah dimulai
        stop_timer()  # Hentikan timer jika permainan belum dimulai
        return

    if timer_running:
        if time_left > 0:
            timer_label.config(text=f"TIMER: {time_left}s")
            time_left -= 1
            after_id = root.after(1000, update_timer)
        else:
            stop_timer()  # Hentikan timer saat waktu habis
            if mode.get() == "vs AI" and player_turn == "X":
                messagebox.showinfo("Tic Tac Toe", "Waktu habis! Giliran Anda dilewati.")
                player_turn = "O"  # Pindah giliran ke AI
                ai_move()  # AI bergerak
                player_turn = "X"  # Kembali ke giliran pemain
                reset_timer()  # Reset timer untuk giliran pemain
            elif mode.get() == "2 Player":
                messagebox.showinfo("Tic Tac Toe", f"Waktu habis! Giliran {player_turn} dilewati.")
                switch_turn()

def switch_turn():
    global player_turn
    player_turn = "O" if player_turn == "X" else "X"
    reset_timer()


def stop_timer():
    global timer_running, after_id
    timer_running = False
    if after_id:  # Jika ada timer yang berjalan, hentikan
        root.after_cancel(after_id)
        after_id = None

def reset_timer():
    global time_left, timer_running
    stop_timer()  # Hentikan semua timer yang berjalan
    time_left = 10  # Atur waktu kembali ke nilai awal
    timer_label.config(text=f"TIMER: {time_left}s")  # Perbarui tampilan timer
    start_timer()  # Mulai timer baru

# Fungsi untuk mengatur ulang papan permainan
def reset_board():
    #Mengatur ulang papan permainan dan giliran pemain ke awal
    global board, player_turn
    board = [" " for _ in range(9)]  # Mengosongkan papan
    player_turn = "X"  # Giliran dimulai dari X
    for button in buttons:
        button.config(
            text=" ", 
            state="normal",
            bg=BOARD_COLOR, 
            fg=BUTTON_TEXT_COLOR
        )  # Reset tampilan tombol
    reset_timer()

# Fungsi untuk memperbarui opsi tingkat kesulitan berdasarkan mode permainan
def update_difficulty_options(*args):
    global game_started, player_1_score, player_2_score, ai_score

    # Hentikan permainan saat mode diubah
    if game_started:
        stop_timer()  # Hentikan timer
        game_started = False  # Set permainan belum dimulai
        reset_board()  # Reset papan permainan
        messagebox.showinfo("Mode Changed", "Mode permainan telah diubah. Tekan tombol 'Start' untuk memulai permainan baru.")
    
    # Reset skor
        player_1_score = 0
        player_2_score = 0
        ai_score = 0
        update_score_display()  # Perbarui tampilan skor


    #Menampilkan atau menyembunyikan opsi tingkat kesulitan berdasarkan mode permainan
    if mode.get() == "vs AI":
        difficulty_label.grid(row=1, column=0)
        difficulty_menu.grid(row=1, column=1)
    else:
        difficulty_label.grid_remove()
        difficulty_menu.grid_remove()

    # Reset timer ketika mode berubah
    reset_timer()

# Fungsi untuk mengecek apakah pemain tertentu menang
def is_winner(player):
    win_conditions = [
        [0, 1, 2], [3, 4, 5], [6, 7, 8],  # Baris
        [0, 3, 6], [1, 4, 7], [2, 5, 8],  # Kolom
        [0, 4, 8], [2, 4, 6]              # Diagonal
    ]
    return any(all(board[i] == player for i in condition) for condition in win_conditions)

# Fungsi untuk mengecek apakah permainan seri (tidak ada pemenang)
def is_draw():
    return " " not in board

# Fungsi langkah AI tingkat easy/mudah (pilih posisi acak yang tersedia)
def ai_move_easy():
    available_moves = [i for i, cell in enumerate(board) if cell == " "]
    move = random.choice(available_moves)
    board[move] = "O"
    buttons[move].config(
        text="O",
        fg="white",
        state="disabled"
    )

# Fungsi langkah AI tingkat medium/menengah (cek langkah menang atau blokir langkah lawan)
def ai_move_medium():
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            if is_winner("O"):
                buttons[i].config(
                    text="O",
                    fg="white", 
                    state="disabled"
                )
                return
            board[i] = " "

    for i in range(9):
        if board[i] == " ":
            board[i] = "X"
            if is_winner("X"):
                board[i] = "O"
                buttons[i].config(
                    text="O",
                    fg="white", 
                    state="disabled"
                )
                return
            board[i] = " "

    # Jika tidak ada langkah menang atau blokir, AI memilih langkah acak
    ai_move_easy()

# Fungsi langkah AI hard/tingkat sulit (menggunakan algoritma minimax)
def ai_move_hard():
    best_score = -float("inf")
    move = None
    for i in range(9):
        if board[i] == " ":
            board[i] = "O"
            score = minimax(board, 0, False)
            board[i] = " "
            if score > best_score:
                best_score = score
                move = i
    board[move] = "O"
    buttons[move].config(
        text="O", 
        fg="white",
        state="disabled"
    )

# Fungsi algoritma Minimax untuk langkah AI terbaik
def minimax(board, depth, is_maximizing):
    if is_winner("O"):
        return 1
    elif is_winner("X"):
        return -1
    elif is_draw():
        return 0

    if is_maximizing:
        best_score = -float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "O"
                score = minimax(board, depth + 1, False)
                board[i] = " "
                best_score = max(score, best_score)
        return best_score
    else:
        best_score = float("inf")
        for i in range(9):
            if board[i] == " ":
                board[i] = "X"
                score = minimax(board, depth + 1, True)
                board[i] = " "
                best_score = min(score, best_score)
        return best_score

# Fungsi untuk langkah AI berdasarkan tingkat kesulitan yang dipilih
def ai_move():
    if player_turn == "O":
        if difficulty.get() == "Easy":
            ai_move_easy()
        elif difficulty.get() == "Medium":
            ai_move_medium()
        else:
            ai_move_hard() == "Hard"

# Fungsi untuk memperbarui skor yang ditampilkan
def update_score_display():
    #Untuk update score
    if mode.get() == "2 Player":
        score_label.config(
            font=bold_font,
            text=f"Skor:\nPlayer 1: {player_1_score}\nPlayer 2: {player_2_score}"
        )
    elif mode.get() == "vs AI":
        score_label.config(
            font=bold_font,
            text=f"Skor:\nPlayer: {player_1_score}\nAI: {ai_score}"
        )
        

# Fungsi langkah pemain pada indeks tertentu
def player_move(index):
    global player_turn, player_1_score, player_2_score, ai_score

    if not game_started:
        messagebox.showwarning("Warning", "Tekan tombol 'Start' untuk memulai permainan.")
        return

    if board[index] == " ":
        board[index] = player_turn
        buttons[index].config(
            text=player_turn,
            fg="white", 
            state="disabled"
        )

        if mode.get() == "2 Player":
            if is_winner(player_turn):
                if player_turn == "X":
                    player_1_score += 1
                else:
                    player_2_score += 1

                update_score_display()
                
                # Cek jika skor mencapai 5
                if player_1_score == 2 or player_2_score == 2:
                    winner = "Player 1" if player_1_score == 2 else "Player 2"
                    messagebox.showinfo("Game Over", f"{winner} Wins the Game!")
                    reset_game()
                    return

                messagebox.showinfo("Tic Tac Toe", f"Player {player_turn} Wins!")
                reset_board()
                return

            elif is_draw():
                messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                reset_board()
                return

            # Ganti giliran pemain dan reset timer
            player_turn = "O" if player_turn == "X" else "X"
            reset_timer()

        elif mode.get() == "vs AI":
            # Mode: vs AI
            if is_winner(player_turn):
                if player_turn == "X":
                    player_1_score += 1
                    update_score_display()

                    # Cek jika skor Player mencapai 5
                    if player_1_score == 2:
                        messagebox.showinfo("Game Over", "Congratulations! You Win the Game!")
                        reset_game()
                        return

                messagebox.showinfo("Tic Tac Toe", "Player Wins!")
                reset_board()
                return

            elif is_draw():
                messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                reset_board()
                return

            # Pindah ke giliran AI dan reset timer
            player_turn = "O"
            reset_timer()  # Reset timer sebelum AI bergerak
            ai_move()

            # Check if AI wins
            if is_winner("O"):
                ai_score += 1
                update_score_display()

                # Cek jika skor AI mencapai 5
                if ai_score == 2:
                    messagebox.showinfo("Game Over", "AI Wins the Game! Better luck next time!")
                    reset_game()
                    return

                messagebox.showinfo("Tic Tac Toe", "AI Wins!")
                reset_board()
                return

            # Check if it's a draw after AI's move
            elif is_draw():
                messagebox.showinfo("Tic Tac Toe", "It's a draw!")
                reset_board()
                return

            # Switch back to player turn
            player_turn = "X"
            reset_timer()

def reset_game():
    global player_1_score, player_2_score, ai_score,game_started
    
    if player_1_score == 2:
        record_game_result("Player 1", player_1_score)
    elif player_2_score == 2:
        record_game_result("Player 2", player_2_score)
    elif ai_score == 2:
        record_game_result("AI", ai_score)
    
    stop_timer()  # Hentikan semua timer sebelum reset
    player_1_score = 0
    player_2_score = 0
    ai_score = 0
    update_score_display()
    reset_board()  # Reset papan permainan
    game_started = False  # Set permainan belum dimulai
    messagebox.showinfo("Game Over", "Tekan tombol 'Start' untuk memulai permainan baru.")

def show_leaderboard():
    leaderboard_window = tk.Toplevel(root)
    leaderboard_window.title("Leaderboard")
    leaderboard_window.geometry("300x300")
    leaderboard_window.configure(bg=BG_COLOR)
    
    tk.Label(
        leaderboard_window, 
        text="Leaderboard",
        font=bold_large_font,
        bg=BG_COLOR,
        fg=FG_COLOR
    ).pack(pady=10)
    
    for idx, entry in enumerate(leaderboard, start=1):
        tk.Label(
            leaderboard_window, 
            text=f"{idx}. {entry['name']} - Score: {entry['score']}, Time: {entry['time']}s",
            font=bold_font,
            bg=BG_COLOR,
            fg=FG_COLOR
        ).pack(pady=5)
    
    # Tombol Reset Leaderboard
    tk.Button(
        leaderboard_window,
        text="Reset Leaderboard",
        bg=BUTTON_COLOR,
        fg=BUTTON_TEXT_COLOR,
        command=lambda: [reset_leaderboard(), leaderboard_window.destroy()]  # Reset lalu tutup jendela
    ).pack(pady=10)
    
    # Tombol untuk menutup jendela
    tk.Button(
        leaderboard_window,
        text="Close",
        bg=BUTTON_COLOR,
        fg=BUTTON_TEXT_COLOR,
        command=leaderboard_window.destroy
    ).pack(pady=10)

def reset_leaderboard():
    global leaderboard
    leaderboard = []  # Kosongkan leaderboard
    messagebox.showinfo("Reset Leaderboard", "Leaderboard telah direset!")

def record_game_result(player_name, score):
    elapsed_time = 10 - time_left  # Waktu yang dihabiskan dalam giliran terakhir
    update_leaderboard(player_name, score, elapsed_time)
    show_leaderboard()

def update_leaderboard(player_name, score, time):
    global leaderboard
    # Tambahkan data ke leaderboard
    leaderboard.append({"name": player_name, "score": score, "time": time})
    # Sortir leaderboard berdasarkan skor dan waktu (prioritaskan skor lebih tinggi, lalu waktu lebih rendah)
    leaderboard = sorted(leaderboard, key=lambda x: (-x["score"], x["time"]))[:5]  # Top 5


def create_game_interface():
    global difficulty_label, difficulty_menu, score_label, timer_label,game_started
    

    # Hapus elemen lama
    for widget in root.winfo_children():
        widget.destroy()

    # Konfigurasi grid untuk root
    root.rowconfigure(0, weight=1)  # Top Frame (Mode, Difficulty, Timer)
    root.rowconfigure(1, weight=3)  # Board Frame (Papan permainan)
    root.rowconfigure(2, weight=1)  # Bottom Frame (Skor dan Reset)
    root.columnconfigure(0, weight=1)

    # Frame bagian atas (top_frame)
    top_frame = tk.Frame(root, bg=BG_COLOR)
    top_frame.grid(row=0, column=0, sticky="nsew", padx=10, pady=10)

    # Frame bagian tengah (board_frame)
    board_frame = tk.Frame(root, bg=BG_COLOR)
    board_frame.grid(row=1, column=0, sticky="nsew", padx=10, pady=10)

    # Frame bagian bawah (bottom_frame)
    bottom_frame = tk.Frame(root, bg=BG_COLOR)
    bottom_frame.grid(row=2, column=0, sticky="nsew", padx=10, pady=10)

    # --- Konfigurasi top_frame ---
    top_frame.columnconfigure(0, weight=1)
    top_frame.columnconfigure(1, weight=1)

    # --- Konfigurasi bottom_frame ---
    bottom_frame.columnconfigure(0, weight=1)
    bottom_frame.columnconfigure(1, weight=1)


    # Label Mode
    tk.Label(
        top_frame, 
        text="Mode:", 
        bg=BG_COLOR, 
        fg=FG_COLOR,
        font=bold_font
    ).grid(
        row=0, 
        column=0,
        sticky="e",  # Rata kanan
        padx=5,
        pady=10
    )
    
    # Dropdown Mode
    mode_menu = tk.OptionMenu(
        top_frame, 
        mode, 
        "2 Player", 
        "vs AI"
    )
    mode_menu.config(
        bg=BUTTON_COLOR, 
        fg=BUTTON_TEXT_COLOR
    )
    mode_menu.grid(
        row=0, 
        column=1,
        sticky="w",  # Rata kiri
        padx=5,
        pady=10
    )

    # Label Difficulty
    difficulty_label = tk.Label(
        top_frame, 
        text="Difficulty:",
        bg=BG_COLOR, 
        fg=FG_COLOR,
        font=bold_font
    )
    difficulty_label.grid(
        row=1, 
        column=0,
        sticky="e",  # Rata kanan
        padx=5
    )

    # Dropdown Difficulty
    difficulty_menu = tk.OptionMenu(
        top_frame, 
        difficulty, 
        "Easy", 
        "Medium", 
        "Hard"
    )
    difficulty_menu.config(
        bg=BUTTON_COLOR, 
        fg=BUTTON_TEXT_COLOR
    )
    difficulty_menu.grid(
        row=1, 
        column=1,
        sticky="w",  # Rata kiri
        padx=5
    )

     # Label untuk timer
    timer_label = tk.Label(
        top_frame, 
        text=f"TIMER: {time_left}s",
        bg=BG_COLOR, 
        fg="#FFD700",  # Warna emas untuk timer
        font=font.Font(family="Arial", size=18, weight="bold")  # Font besar dan tebal
    )

    timer_label.grid(
        row=2, 
        column=0,
        columnspan=2,
        pady=20
    )

     # --- Konfigurasi board_frame ---
    for i in range(3):  # Konfigurasi 3 baris dan 3 kolom
        board_frame.rowconfigure(i, weight=1)
        board_frame.columnconfigure(i, weight=1)

    # Update opsi berdasarkan mode
    mode.trace_add(
        "write", 
        lambda *args: update_difficulty_options()
    )

    update_difficulty_options()
    
    # Label untuk skor
    score_label = tk.Label(
        bottom_frame, 
        text=f"Skor:\nPlayer 1: {player_1_score}\nPlayer 2: {player_2_score}",
        bg=BG_COLOR, 
        fg="#FFD700",  # Warna emas untuk timer
        font=font.Font(family="Arial", size=13, weight="bold")
    )
    score_label.grid(
        row=6, 
        column=0, 
        columnspan=3, 
        pady=10,
        sticky="n"
    )
    
    # Membuat papan Tic Tac Toe
    for i in range(9):
        button = tk.Button(
            board_frame, 
            text=" ", 
            width=10, 
            height=4,
            command=lambda i=i: player_move(i),
            bg=BOARD_COLOR, 
            fg=BUTTON_TEXT_COLOR
        )
        button.grid(
            row=(i // 3), 
            column=i % 3,
            padx=5,
            pady=5,
            sticky="nsew"
        )
        buttons.append(button)
    
    # --- Konfigurasi bottom_frame ---
    bottom_frame.columnconfigure(0, weight=1)

    # Tombol Reset Game
    tk.Button(
        bottom_frame, 
        text="Reset Game", 
        command=reset_game,
        bg=BUTTON_COLOR, 
        fg=BUTTON_TEXT_COLOR
    ).grid(
        row=0, 
        column=0, 
        padx=10, 
        pady=8, 
        sticky="ew"  # Mengisi lebar kolom
    )

    # Tombol Leaderboard
    tk.Button(
        bottom_frame, 
        text="Leaderboard", 
        command=show_leaderboard,
        bg=BUTTON_COLOR, 
        fg=BUTTON_TEXT_COLOR
    ).grid(
        row=0, 
        column=1, 
        padx=10, 
        pady=8, 
        sticky="ew"  # Mengisi lebar kolom
    )

    # Tombol Start Game
    tk.Button(
        bottom_frame, 
        text="Start", 
        command=start_game_action,
        bg=BUTTON_COLOR, 
        fg=BUTTON_TEXT_COLOR
    ).grid(
        row=1, 
        column=0, 
        columnspan=2, 
        padx=10, 
        pady=8, 
        sticky="ew"
    )

# Menampilkan halaman selamat datang saat program dimulai
show_welcome_page()
root.mainloop()