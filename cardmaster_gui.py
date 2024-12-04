import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QStackedWidget, QCheckBox, QMessageBox, QGridLayout, QScrollArea
from PyQt5.QtCore import Qt

class CardmasterGUI(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("The Cardmaster")
        self.setGeometry(100, 100, 800, 480)  # Set size to fit Raspberry Pi touchscreen

        # Track player positions, current player, and dealing status
        self.total_players = 6
        self.current_player = 1
        self.active_players = []
        self.starting_cards = 0
        self.player_cards = {}
        self.previous_page = None
        self.selected_game = None

        # Central widget and stacked widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        self.stacked_widget = QStackedWidget()
        
        # Create pages
        self.home_page = self.create_home_page()
        self.select_game_page = self.create_select_game_page()
        self.select_seats_page = self.create_select_seats_page()
        self.how_to_play_page = self.create_how_to_play_page()
        self.manage_game_page = self.create_manage_game_page()
        self.confirm_shuffle_page = self.create_confirm_shuffle_page()
        self.confirm_reverse_order_page = self.create_confirm_reverse_order_page()
        
        # Add pages to stacked widget
        self.stacked_widget.addWidget(self.home_page)
        self.stacked_widget.addWidget(self.select_game_page)
        self.stacked_widget.addWidget(self.select_seats_page)
        self.stacked_widget.addWidget(self.how_to_play_page)
        self.stacked_widget.addWidget(self.manage_game_page)
        self.stacked_widget.addWidget(self.confirm_shuffle_page)
        self.stacked_widget.addWidget(self.confirm_reverse_order_page)
        
        # Layout for central widget
        layout = QVBoxLayout()
        layout.addWidget(self.stacked_widget)
        central_widget.setLayout(layout)
        
        # Show home page initially
        self.stacked_widget.setCurrentWidget(self.home_page)

    def create_home_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        title = QLabel("The Cardmaster")
        title.setStyleSheet("font-size: 28px; font-weight: bold; margin-bottom: 20px;")
        title.setAlignment(Qt.AlignCenter)
        layout.addWidget(title)

        button_style = "font-size: 16px; padding: 10px; margin: 5px;"

        start_game_button = QPushButton("Start Game")
        start_game_button.setStyleSheet(button_style)
        start_game_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.select_seats_page))
        layout.addWidget(start_game_button)

        select_game_button = QPushButton("Select Game")
        select_game_button.setStyleSheet(button_style)
        select_game_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.select_game_page))
        layout.addWidget(select_game_button)

        shuffle_cards_button = QPushButton("Shuffle Cards")
        shuffle_cards_button.setStyleSheet(button_style)
        shuffle_cards_button.clicked.connect(lambda: self.navigate_to_confirm_shuffle(self.home_page))
        layout.addWidget(shuffle_cards_button)

        how_to_play_button = QPushButton("How to Play")
        how_to_play_button.setStyleSheet(button_style)
        how_to_play_button.clicked.connect(lambda: self.navigate_to_how_to_play(self.home_page))
        layout.addWidget(how_to_play_button)

        page.setLayout(layout)
        return page

    def create_select_game_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel("Select Game")
        label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        button_style = "font-size: 16px; padding: 10px; margin: 5px;"

        uno_button = QPushButton("UNO")
        uno_button.setStyleSheet(button_style)
        uno_button.clicked.connect(lambda: self.select_game("UNO"))
        layout.addWidget(uno_button)

        phase10_button = QPushButton("Phase 10")
        phase10_button.setStyleSheet(button_style)
        phase10_button.clicked.connect(lambda: self.select_game("Phase 10"))
        layout.addWidget(phase10_button)

        blackjack_button = QPushButton("Blackjack")
        blackjack_button.setStyleSheet(button_style)
        blackjack_button.clicked.connect(lambda: self.select_game("Blackjack"))
        layout.addWidget(blackjack_button)

        back_button = QPushButton("Back")
        back_button.setStyleSheet(button_style)
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.home_page))
        layout.addWidget(back_button)

        page.setLayout(layout)
        return page

    def select_game(self, game):
        self.selected_game = game
        if game == "UNO":
            self.starting_cards = 7
        elif game == "Phase 10":
            self.starting_cards = 10
        elif game == "Blackjack":
            self.starting_cards = 2
        QMessageBox.information(self, "Game Selected", f"{game} selected! Each player will receive {self.starting_cards} cards.")
        self.stacked_widget.setCurrentWidget(self.home_page)

    def create_select_seats_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel("Select Player Seats")
        label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        self.seat_checkboxes = []
        grid_layout = QGridLayout()
        for i in range(1, self.total_players + 1):
            checkbox = QCheckBox(f"Seat {i}")
            checkbox.setStyleSheet("font-size: 16px;")
            self.seat_checkboxes.append(checkbox)
            grid_layout.addWidget(checkbox, (i - 1) // 3, (i - 1) % 3)
        layout.addLayout(grid_layout)

        confirm_button = QPushButton("Confirm Seats")
        confirm_button.setStyleSheet("font-size: 16px; padding: 10px; margin: 5px;")
        confirm_button.clicked.connect(self.confirm_seats)
        layout.addWidget(confirm_button)

        back_button = QPushButton("Back")
        back_button.setStyleSheet("font-size: 16px; padding: 10px; margin: 5px;")
        back_button.clicked.connect(lambda: self.stacked_widget.setCurrentWidget(self.home_page))
        layout.addWidget(back_button)

        page.setLayout(layout)
        return page

    def create_how_to_play_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)

        label = QLabel("How to Play")
        label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        label.setAlignment(Qt.AlignCenter)
        layout.addWidget(label)

        # Create a scroll area for the instructions
        scroll_area = QScrollArea()
        scroll_area.setWidgetResizable(True)

        # Widget to hold the instructions text
        instructions_widget = QWidget()
        instructions_layout = QVBoxLayout()
        instructions_layout.setAlignment(Qt.AlignTop)

        instructions = QLabel(
            "Host Instructions:\n"
            "1. Select a game (UNO, Phase 10, or Blackjack).\n"
            "2. Choose player seats.\n"
            "3. Start the game to deal the starting cards.\n"
            "4. Use the 'Manage Game' screen to shuffle, reverse dealing order, or end the game.\n\n"
            "Player Instructions:\n"
            "1. Player will press their designated 'draw card' button to receive a card during their turn. \n"
            "2. Player will press their designated 'end turn' button so that the Cardmaster can ready itself for the next player.\n\n"
            "Shuffler Instructions:\n"
            "1. Insert a new deck of cards into the loading tray. \n"
            "2. Simply start the shuffle before starting the game, or during. \n\n"
            "Game Instructions:\n"
            "Phase 10: \n"
            "UNO: \n"
            "Blackjack: \n"
        )
        instructions.setStyleSheet("font-size: 16px;")
        instructions.setWordWrap(True)
        instructions_layout.addWidget(instructions)

        instructions_widget.setLayout(instructions_layout)
        scroll_area.setWidget(instructions_widget)

        layout.addWidget(scroll_area)

        # Back button
        back_button = QPushButton("Back")
        back_button.setStyleSheet("font-size: 16px; padding: 10px; margin: 5px;")
        back_button.clicked.connect(self.return_to_previous_page)
        layout.addWidget(back_button)

        page.setLayout(layout)
        return page

    def create_manage_game_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        label = QLabel("Manage Game")
        label.setStyleSheet("font-size: 24px; font-weight: bold; margin-bottom: 20px;")
        layout.addWidget(label)
        
        button_style = "font-size: 16px; padding: 10px; margin: 5px;"

        reverse_order_button = QPushButton("Reverse Dealing Order")
        reverse_order_button.setStyleSheet(button_style)
        reverse_order_button.clicked.connect(lambda: self.navigate_to_confirm_reverse_order(self.manage_game_page))
        layout.addWidget(reverse_order_button)

        shuffle_new_deck_button = QPushButton("Shuffle New Deck")
        shuffle_new_deck_button.setStyleSheet(button_style)
        shuffle_new_deck_button.clicked.connect(lambda: self.navigate_to_confirm_shuffle(self.manage_game_page))
        layout.addWidget(shuffle_new_deck_button)

        view_rules_button = QPushButton("View Game Rules")
        view_rules_button.setStyleSheet(button_style)
        view_rules_button.clicked.connect(lambda: self.navigate_to_how_to_play(self.manage_game_page))
        layout.addWidget(view_rules_button)

        end_game_button = QPushButton("End Game")
        end_game_button.setStyleSheet(button_style)
        end_game_button.clicked.connect(self.end_game)
        layout.addWidget(end_game_button)

        page.setLayout(layout)
        return page

    def create_confirm_shuffle_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        label = QLabel("Are you sure you want to shuffle the cards?")
        label.setStyleSheet("font-size: 18px; margin-bottom: 10px;")
        layout.addWidget(label)

        note = QLabel("Note: A deck of cards should be inserted into the shuffling system.")
        note.setStyleSheet("font-size: 14px;")
        layout.addWidget(note)

        button_style = "font-size: 16px; padding: 10px; margin: 5px;"
        
        yes_button = QPushButton("Yes")
        yes_button.setStyleSheet(button_style)
        yes_button.clicked.connect(self.shuffle_cards)
        layout.addWidget(yes_button)

        no_button = QPushButton("No")
        no_button.setStyleSheet(button_style)
        no_button.clicked.connect(self.return_to_previous_page)
        layout.addWidget(no_button)

        page.setLayout(layout)
        return page

    def create_confirm_reverse_order_page(self):
        page = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignCenter)
        
        label = QLabel("Are you sure you want to reverse the dealing order?")
        label.setStyleSheet("font-size: 18px; margin-bottom: 10px;")
        layout.addWidget(label)

        button_style = "font-size: 16px; padding: 10px; margin: 5px;"

        yes_button = QPushButton("Yes")
        yes_button.setStyleSheet(button_style)
        yes_button.clicked.connect(self.reverse_order)
        layout.addWidget(yes_button)

        no_button = QPushButton("No")
        no_button.setStyleSheet(button_style)
        no_button.clicked.connect(self.return_to_previous_page)
        layout.addWidget(no_button)

        page.setLayout(layout)
        return page

    def navigate_to_confirm_shuffle(self, previous_page):
        self.previous_page = previous_page
        self.stacked_widget.setCurrentWidget(self.confirm_shuffle_page)

    def navigate_to_confirm_reverse_order(self, previous_page):
        self.previous_page = previous_page
        self.stacked_widget.setCurrentWidget(self.confirm_reverse_order_page)

    def navigate_to_how_to_play(self, previous_page):
        self.previous_page = previous_page
        self.stacked_widget.setCurrentWidget(self.how_to_play_page)

    def return_to_previous_page(self):
        if self.previous_page:
            self.stacked_widget.setCurrentWidget(self.previous_page)

    # Other methods remain unchanged


    def confirm_seats(self):
        self.active_players = [i + 1 for i, checkbox in enumerate(self.seat_checkboxes) if checkbox.isChecked()]
        self.player_cards = {player: 0 for player in self.active_players}  # Initialize card count per player
        
        if not self.active_players:
            QMessageBox.warning(self, "No Seats Selected", "Please select at least one seat to continue.")
            return
        
        if self.selected_game is None:
            QMessageBox.warning(self, "No Game Selected", "Please select a game before starting.")
            return
        
        QMessageBox.information(self, "Seats Confirmed", f"Players in seats {self.active_players} will participate.")
        self.initial_deal()

    def initial_deal(self):
        self.current_player_index = 0
        self.deal_one_card()

    def deal_one_card(self):
        if all(cards == self.starting_cards for cards in self.player_cards.values()):
            QMessageBox.information(self, "Dealing Complete", "All players have received their starting cards.")
            self.stacked_widget.setCurrentWidget(self.manage_game_page)
            return
        
        player = self.active_players[self.current_player_index]
        self.player_cards[player] += 1
        QMessageBox.information(self, "Dealing", f"Dealt 1 card to Player {player}. Total cards: {self.player_cards[player]}")
        
        # Move to next player
        self.current_player_index = (self.current_player_index + 1) % len(self.active_players)
        self.deal_one_card()

    # Placeholder methods for actions
    def shuffle_cards(self):
        QMessageBox.information(self, "Shuffling", "The deck is being shuffled.")
        self.return_to_previous_page()

    def reverse_order(self):
        self.active_players.reverse()
        QMessageBox.information(self, "Reverse Order", "Reversing the dealing order.")
        self.return_to_previous_page()

    def end_game(self):
        reply = QMessageBox.question(self, "End Game", "Are you sure you want to end the game?", QMessageBox.Yes | QMessageBox.No)
        if reply == QMessageBox.Yes:
            self.stacked_widget.setCurrentWidget(self.home_page)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = CardmasterGUI()
    window.showFullScreen()
    sys.exit(app.exec_())

