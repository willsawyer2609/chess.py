""" Chess game. """

# TODO: Allow 'en passant' capture of Pawn on first move.
# TODO: Find website to give credit for icons in welcome screen.

import PySimpleGUI as sg
import gui
from pieces import *


def DarkCell(position):
    """ Returns a PySimpleGUI image element with a black background. """
    return sg.Button(button_color="black", key=position)


def LightCell(position):
    """ Returns a PySimpleGUI image element with a white background. """
    return sg.Button(button_color="white", key=position)


welcome_msg = (
        "Welcome to Chess!\n"
        "\n"
        "This game has been developed by William Sawyer with use of the "
        "PySimpleGUI package."
    )

sg.theme("DarkGrey11")

# Layout for welcome window.
welcome_layout = [
    [sg.Text(welcome_msg, key="out", size=(47, 12), font="Courier")],
    [sg.Button("Start", size=(10, 1))]
]
# Layout for game window.
chessboard = [
    [sg.Button("New Game", key="new_game", size=(15, 1)),
     sg.Text(key="turn", size=(20, 1), justification="center"),
     sg.Text(key="out", size=(50, 1), justification="center")]]\
        + [
    [LightCell((row, column)) if (row + column) % 2 == 0
    else DarkCell((row, column)) for column in range(8)]
    for row in range(8)]

welcome_window = sg.Window("Welcome", welcome_layout, resizable=True,
                           finalize=True).read(close=True)
window = sg.Window("Chess", chessboard, location=(625, 0), size=(716, 700),
                   icon=None, finalize=True)

black, white, initial, destination, winner, count, turns = gui.new_game(window)

# Game loop.
while True:
    event, values = window.read()

    if event == sg.WIN_CLOSED:
        window.close()
        break
    elif event == "new_game":
        black, white, initial, destination, winner, count, turns = \
            gui.new_game(window)
    else:  # A cell is clicked.
        if initial is None:  # The piece to move hasn't been chosen.
            piece = moves.get_piece(black, white, event)
            if piece is not None and piece.get_team() == turns[count % 2]:
                initial = event
        else:
            destination = event
            dest_piece = moves.get_piece(black, white, destination)
            if dest_piece is None:
                if piece.move(destination, black, white, window):
                    count += 1
                    window["turn"].update(f"It's {turns[count % 2]}'s turn.")
                    window["out"].update("")
                    if piece.get_type() == "Pawn" and \
                        destination[0] == piece.get_far():
                        promo_piece = sg.popup_get_text("Which piece do you "
                                                       "want to promote to?",
                                                       "Promotion")
                        black, white = piece.promote(promo_piece, black,
                                                     white, window)
            else:
                if piece.attack(destination, black, white, window):
                    black, white, = dest_piece.kill(black, white)
                    count += 1
                    window["turn"].update(f"It's {turns[count % 2]}'s turn.")
                    window["out"].update("")
                    if piece.get_type() == "Pawn" and destination[0] == \
                            piece.get_far():
                        promo_piece = sg.popup_get_text("Which piece do you "
                                                        "want to promote to?",
                                                        "Promotion")
                        black, white = piece.promote(promo_piece, black,
                                                     white, window)
            initial, destination = None, None
    winner = gui.check_endgame(black, white)
    if winner is not None:
        window["turn"].update("")
        window["out"].update(f"{winner} wins!")
        break

window.close()
