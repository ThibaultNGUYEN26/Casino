from random import choice
import socket

server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(('localhost', 10000))
server_socket.listen(1)

money_path = r'res/money.txt'
history_path = r'res/history.txt'
try:
	number = ["Ace", "2", "3", "4", "5", "6", "7", "8", "9", "10", "Jack", "Queen", "King"]
	color = ["Spades", "Hearts", "Clubs", "Diamonds"]

	with open(money_path, 'r') as m:
		money = m.read()
	with open(history_path, 'r') as h:
		history = h.read()

	money = int(money)

	EOC = '\x1b[0m'
	WHITE = '\x1b[1;37;40m'
	RED = '\x1b[1;31;40m'
	GREEN2 = '\x1b[1;32;40m'
	GREEN = '\x1b[0;32;40m'
	BLUE = '\x1b[1;36;40m'
	PINK = '\x1b[1;35;40m'
	YELLOW = '\x1b[1;33;40m'
	BLACK = '\x1b[1;30;47m'
	RED2 = '\x1b[1;31;40m'

	def info_msg(type, msg):
		if type == "Info":
			print(f"\n{GREEN}[{type}] {WHITE}{msg}\n{EOC}")
		if type == "Game":
			print(f"\n{GREEN}[{type}] {BLUE}{msg}\n{EOC}")
		if type == "Error":
			print(f"\n{RED}[{type}] {WHITE}{msg}\n{EOC}")

	def random_card(number, color):
		return (choice(number), choice(color))

	def display_card(nb, col):
		msg = f"{YELLOW}The card is {'an' if nb in [number[0], number[7]] else 'a'} {nb} of {col} !{EOC}"
		info_msg("Game", msg)

	def set_history_msg(nb, col, status, bonus, bet):
		if status == "win":
			if nb in number[1::2]:
				if col in [color[0], color[2]]:
					msg2 = f"{GREEN2}[+{bonus}$] {YELLOW}{nb} of {col} {WHITE}[{nb} | {col} | EVEN | BLACK]{EOC}"
				elif col in [color[1], color[3]]:
					msg2 = f"{GREEN2}[+{bonus}$] {YELLOW}{nb} of {col} {RED2}[{nb} | {col} | EVEN | RED]{EOC}"
			elif nb in number[0::2]:
				if col in [color[0], color[2]]:
					msg2 = f"{GREEN2}[+{bonus}$] {YELLOW}{nb} of {col} {WHITE}[{nb} | {col} | ODD | BLACK]{EOC}"
				elif col in [color[1], color[3]]:
					msg2 = f"{GREEN2}[+{bonus}$] {YELLOW}{nb} of {col} {RED2}[{nb} | {col} | ODD | RED]{EOC}"
		if status == "lose":
			if nb in number[1::2]:
				if col in [color[0], color[2]]:
					msg2 = f"{RED}[-{bet}$] {YELLOW}{nb} of {col} {WHITE}[{nb} | {col} | EVEN | BLACK]{EOC}"
				elif col in [color[1], color[3]]:
					msg2 = f"{RED}[-{bet}$] {YELLOW}{nb} of {col} {RED2}[{nb} | {col} | EVEN | RED]{EOC}"
			elif nb in number[0::2]:
				if col in [color[0], color[2]]:
					msg2 = f"{RED}[-{bet}$] {YELLOW}{nb} of {col} {WHITE}[{nb} | {col} | ODD | BLACK]{EOC}"
				elif col in [color[1], color[3]]:
					msg2 = f"{RED}[-{bet}$] {YELLOW}{nb} of {col} {RED2}[{nb} | {col} | ODD | RED]{EOC}"
		with open(history_path, 'a') as h:
			h.write(msg2 + '\n')

	def add_bet(bet):
		global money

		money += bet
		with open(money_path, 'w') as m:
			m.write(str(money))

	def sub_bet(bet):
		global money

		money -= bet
		with open(money_path, 'w') as m:
			m.write(str(money))

	def check_money(money):
		if money <= 0:
			info_msg("Info", f"{RED}You don't have enough money.{EOC}")
			return False
		return True

	def check_bet(money, bet):
		if bet < 1:
			info_msg("Info", f"{RED}Enter a valid bet.{EOC}")
			return False
		if money < bet:
			info_msg("Info", f"{RED}You don't have enough money.{EOC}")
			return False
		else:
			sub_bet(bet)
			info_msg("Info", f"You bet {bet}$.")
			return True

	def pick_color():
		global money

		bet = int(input(f"{PINK}Enter an amount to bet : {EOC}"))
		if check_bet(money, bet):
			bonus = bet * 2
			while True:
				try:
					user_col_choice = int(input(f"{WHITE} /--------------------------------------\\\n|* ---------- {PINK}Choose a color{WHITE} ---------- *|\n \\--------------------------------------/\n\n{BLUE}[1] {EOC}Red\n{BLUE}[2] {EOC}Black\n{BLUE}[3] {EOC}Return\n{PINK}Type a number : {EOC}"))
					if user_col_choice < 1 or user_col_choice > 3:
						info_msg("Error", "Type a valid number.")
					elif user_col_choice == 1:
						nb, col = random_card(number, color)
						info_msg("Game", "You choose the color Red.")
						display_card(nb, col)
						set_history_msg(nb, col, "win", bonus, bet) if col in color[1::2] else set_history_msg(nb, col, "lose", bonus, bet)
						info_msg("Info", f"{GREEN2}You won {bonus}$ !{EOC}" if col in color[1::2] else f"{RED}You lost {bet}$...{EOC}")
						if col in color[1::2]:
							add_bet(bonus) 
						break
					elif user_col_choice == 2:
						nb, col = random_card(number, color)
						info_msg("Game", "You choose the color Black.")
						display_card(nb, col)
						set_history_msg(nb, col, "win", bonus, bet) if col in color[0::2] else set_history_msg(nb, col, "lose", bonus, bet)
						info_msg("Info", f"{GREEN2}You won {bonus}$ !{EOC}" if col in color[0::2] else f"{RED}You lost {bet}$...{EOC}")
						if col in color[0::2]:
							add_bet(bonus) 
						break
					else:
						info_msg("Info", "Back to the menu.")
						break
				except ValueError:
					info_msg("Error", "Type a valid number.")

	def pick_parity():
		global money

		bet = int(input(f"{PINK}Enter an amount to bet : {EOC}"))
		if check_bet(money, bet):
			bonus = bet * 2
			while True:
				try:
					user_par_choice = int(input(f"{WHITE} /---------------------------------------\\\n|* ---------- {PINK}Choose a parity{WHITE} ---------- *|\n \\---------------------------------------/\n\n{BLUE}[1]{EOC} Even\n{BLUE}[2]{EOC} Odd\n{BLUE}[3]{EOC} Return\n{PINK}Type a number : {EOC}"))
					if user_par_choice < 1 or user_par_choice > 3:
						info_msg("Error", "Type a valid number.")
					elif user_par_choice == 1:
						nb, col = random_card(number, color)
						info_msg("Game", "You choose Even.")
						display_card(nb, col)
						set_history_msg(nb, col, "win", bonus, bet) if nb in number[1::2] else set_history_msg(nb, col, "lose", bonus, bet)
						info_msg("Info", f"{GREEN2}You won {bonus}$ !{EOC}" if nb in number[1::2] else f"{RED}You lost {bet}$...{EOC}")
						if nb in number[1::2]:
							add_bet(bonus) 
						break
					elif user_par_choice == 2:
						nb, col = random_card(number, color)
						info_msg("Game", "You choose Odd.")
						display_card(nb, col)
						set_history_msg(nb, col, "win", bonus, bet) if nb in number[0::2] else set_history_msg(nb, col, "lose", bonus, bet)
						info_msg("Info", f"{GREEN2}You won {bonus}$ !{EOC}" if nb in number[0::2] else f"{RED}You lost {bet}$...{EOC}")
						if nb in number[0::2]:
							add_bet(bonus)
						break
					else:
						add_bet(bet)
						info_msg("Info", "Back to the menu.")
						break
				except ValueError:
					info_msg("Error", "Type a valid number.")

	def pick_sign():
		global money

		bet = int(input(f"{PINK}Enter an amount to bet : {EOC}"))
		if check_bet(money, bet):
			bonus = bet * 3
			while True:
				try:
					user_sign_choice = int(input(f"{WHITE} /-------------------------------------\\\n|* ---------- {PINK}Choose a sign{WHITE} ---------- *|\n \\-------------------------------------/\n\n{BLUE}[1]{EOC} Spades\n{BLUE}[2]{EOC} Hearts\n{BLUE}[3]{EOC} Clubs\n{BLUE}[4]{EOC} Diamonds\n{BLUE}[5]{EOC} Return\n{PINK}Type a number : {EOC}"))
					if user_sign_choice < 1 or user_sign_choice > 5:
						info_msg("Error", "Type a valid number.")
					if user_sign_choice == 5:
						add_bet(bet)
						info_msg("Info", "Back to the menu.")
						break
					else:
						nb, col = random_card(number, color)
						info_msg("Game", f"You choose {color[user_sign_choice - 1]}.")
						display_card(nb, col)
						if user_sign_choice == 1:
							set_history_msg(nb, col, "win", bonus, bet) if col == color[0] else set_history_msg(nb, col, "lose", bonus, bet)
							info_msg("Info", f"{GREEN2}You won {bonus}$ !{EOC}" if col == color[0] else f"{RED}You lost {bet}$...{EOC}")
							if col in color[0]:
								add_bet(bonus) 
							break
						if user_sign_choice == 2:
							set_history_msg(nb, col, "win", bonus, bet) if col == color[1] else set_history_msg(nb, col, "lose", bonus, bet)
							info_msg("Info", f"{GREEN2}You won {bonus}$ !{EOC}" if col == color[1] else f"{RED}You lost {bet}$...{EOC}")
							if col in color[1]:
								add_bet(bonus)
							break
						if user_sign_choice == 3:
							set_history_msg(nb, col, "win", bonus, bet) if col == color[2] else set_history_msg(nb, col, "lose", bonus, bet)
							info_msg("Info", f"{GREEN2}You won {bonus}$ !{EOC}" if col == color[2] else f"{RED}You lost {bet}$...{EOC}")
							if col in color[2]:
								add_bet(bonus) 
							break
						if user_sign_choice == 4:
							set_history_msg(nb, col, "win", bonus, bet) if col == color[3] else set_history_msg(nb, col, "lose", bonus, bet)
							info_msg("Info", f"{GREEN2}You won {bonus}$ !{EOC}" if col == color[3] else f"{RED}You lost {bet}$...{EOC}")
							if col in color[3]:
								add_bet(bonus)
							break	
				except ValueError:
					info_msg("Error", "Type a valid number.")

	def pick_number():
		global money

		bet = int(input(f"{PINK}Enter an amount to bet : {EOC}"))
		if check_bet(money, bet):
			bonus = bet * 5
			while True:
				try:
					user_nb_choice = int(input(f"{WHITE} /---------------------------------------\\\n|* ---------- {PINK}Choose a number{WHITE} ---------- *|\n \\---------------------------------------/\n\n{BLUE}[1]{EOC} Ace\n{BLUE}[2]{EOC} Two\n{BLUE}[3]{EOC} Three\n{BLUE}[4]{EOC} Four\n{BLUE}[5]{EOC} Five\n{BLUE}[6]{EOC} Six\n{BLUE}[7]{EOC} Seven\n{BLUE}[8]{EOC} Eight\n{BLUE}[9]{EOC} Nine\n{BLUE}[10]{EOC} Ten\n{BLUE}[11]{EOC} Jack\n{BLUE}[12]{EOC} Queen\n{BLUE}[13]{EOC} King\n{BLUE}[14]{EOC} Return\n{PINK}Type a number : {EOC}"))
					if user_nb_choice < 1 or user_nb_choice > 14:
						info_msg("Error", "Type a valid number.")
					elif user_nb_choice == 14:
						add_bet(bet)
						info_msg("Info", "Back to the menu.")
						break
					else:
						nb, col = random_card(number, color)
						nb_choice = number[user_nb_choice - 1]
						info_msg("Game", f"You choose {nb_choice}.")
						display_card(nb, col)
						if nb_choice == nb:
							set_history_msg(nb, col, "win", bonus, bet)
							info_msg("Info", f"{GREEN2}You won {bonus}$ !{EOC}")
							add_bet(bonus)
							break
						else:
							set_history_msg(nb, col, "lose", bonus, bet)
							info_msg("Info", f"{RED}You lost {bet}$...{EOC}")
							break
				except ValueError:
					info_msg("Error", "Type a valid number.")

	def pick_card():
		global money

		bet = int(input(f"{PINK}Enter an amount to bet : {EOC}"))
		if check_bet(money, bet):
			bonus = bet * 10
			while True:
				try:
					user_nb_choice = int(input(f"{WHITE} /---------------------------------------\\\n|* ---------- {PINK}Choose a number{WHITE} ---------- *|\n \\---------------------------------------/\n\n{BLUE}[1]{EOC} Ace\n{BLUE}[2]{EOC} Two\n{BLUE}[3]{EOC} Three\n{BLUE}[4]{EOC} Four\n{BLUE}[5]{EOC} Five\n{BLUE}[6]{EOC} Six\n{BLUE}[7]{EOC} Seven\n{BLUE}[8]{EOC} Eight\n{BLUE}[9]{EOC} Nine\n{BLUE}[10]{EOC} Ten\n{BLUE}[11]{EOC} Jack\n{BLUE}[12]{EOC} Queen\n{BLUE}[13]{EOC} King\n{BLUE}[14]{EOC} Return\n{PINK}Type a number : {EOC}"))
					if user_nb_choice < 1 or user_nb_choice > 14:
						info_msg("Error", "Type a valid number.")
					elif user_nb_choice == 14:
						add_bet(bet)
						info_msg("Info", "Back to the menu.")
						break
					else:
						nb_choice = number[user_nb_choice - 1]
						while True:
							try:
								user_col_choice = int(input(f"{WHITE} /--------------------------------------\\\n|* ---------- {PINK}Choose a color{WHITE} ---------- *|\n \\--------------------------------------/\n\n{BLUE}[1]{EOC} Spades\n{BLUE}[2]{EOC} Hearts\n{BLUE}[3]{EOC} Clubs\n{BLUE}[4]{EOC} Diamonds\n{BLUE}[5]{EOC} Return\n{PINK}Type a number : {EOC}"))
								if user_col_choice < 1 or user_col_choice > 5:
									info_msg("Error", "Type a valid number.")
								elif user_col_choice == 5:
									info_msg("Info", "You left the game.")
									break
								else:
									col_choice = color[user_col_choice - 1]
									nb, col = random_card(number, color)
									info_msg("Game", f"You choose the {nb_choice} of {col_choice} !")
									display_card(nb, col)
									set_history_msg(nb, col, "win", bonus, bet) if col == col_choice and nb == nb_choice else set_history_msg(nb, col, "lose", bonus, bet)
									info_msg("Info", f"{GREEN2}You won {bonus}$ !{EOC}" if col == col_choice and nb == nb_choice else f"{RED}You lost {bet}$...{EOC}")
									if col == col_choice and nb == nb_choice:
										add_bet(bonus)
									break
							except ValueError:
								info_msg("Error", "Type a valid number.")
					break
				except ValueError:
					info_msg("Error", "Type a valid number.")

	def play():
		global money

		while True:
			print(f"\n {WHITE}/----------------------------\\\n|* ---------- {PINK}GAME{WHITE} ---------- *|\n \----------------------------/{EOC}")
			print(f"\n{WHITE}|* ------------------------------ {GREEN}[MONEY] {WHITE}You have {YELLOW}{money}${WHITE} ------------------------------ *|{EOC}\n")
			try:
				user_choice = int(input(f" {WHITE}/-----------------------------------------\\\n|* ---------- {PINK}Choose a guessing{WHITE} ---------- *|\n \\-----------------------------------------/\n\n{BLUE}[1] {EOC}Color\n{BLUE}[2] {EOC}Parity\n{BLUE}[3] {EOC}Sign\n{BLUE}[4] {EOC}Number\n{BLUE}[5] {EOC}Card\n{BLUE}[6] {EOC}Quit\n{PINK}Type a number : {EOC}"))
				if user_choice < 1 or user_choice > 6:
					info_msg("Error", "Type a valid number.")
				elif user_choice == 1:
					if check_money(money):
						info_msg("Info", f"Guess a color. {GREEN2}(Bonus x2){EOC}")
						pick_color()
				elif user_choice == 2:
					if check_money(money):
						info_msg("Info", f"Guess a parity. {GREEN2}(Bonus x2){EOC}")
						pick_parity()
				elif user_choice == 3:
					if check_money(money):
						info_msg("Info", f"Guess a sign. {GREEN2}(Bonus x3){EOC}")
						pick_sign()
				elif user_choice == 4:
					if check_money(money):
						info_msg("Info", f"Guess a number. {GREEN2}(Bonus x5){EOC}")
						pick_number()
				elif user_choice == 5:
					if check_money(money):
						info_msg("Info", f"Guess a card. {GREEN2}(Bonus x10){EOC}")
						pick_card()
				else:
					info_msg("Info", "You left the game.")
					quit()
					
			except ValueError:
				info_msg("Error", "Type a valid number.")

	if __name__ == '__main__':
		play()
finally:
	server_socket.close()