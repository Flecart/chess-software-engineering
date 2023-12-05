import chess
import chess.svg
import cairosvg


def _to_standard_fen(fen):
    fen = fen.split(" ")
    count_empty_cell = 0
    new_fen = ""
    # we transform the first part of fen that contains ? to a normal fen
    for i in range(len(fen[0])):
        if fen[0][i] == "/":
            if count_empty_cell > 0:
                new_fen += str(count_empty_cell)
            new_fen += "/"
            count_empty_cell = 0
        elif fen[0][i] == "?":
            count_empty_cell += 1
        elif fen[0][i].isdigit():
            count_empty_cell += int(fen[0][i])
        else:
            if count_empty_cell > 0:
                new_fen += str(count_empty_cell)
            new_fen += fen[0][i]
            count_empty_cell = 0
    if count_empty_cell > 0:
        new_fen += str(count_empty_cell)

    return " ".join([new_fen] + fen[1:])


def _get_not_visible_squares(fen):
    fen = fen.split(" ")[0]
    col = 0
    row = 7
    position = []
    for i in range(len(fen)):
        if fen[i] == "/":
            row -= 1
            col = 0
        elif fen[i].isdigit():
            col += int(fen[i])
        else:
            col += 1
            if fen[i] == "?":
                position.append((row, col))

    return position


def custom_fen_to_svg(fen):
    positions = list(
        map(lambda x: chess.square(x[1], x[0]) - 1, _get_not_visible_squares(fen))
    )

    board = chess.Board(_to_standard_fen(fen))

    svg = chess.svg.board(
        board,
        fill=dict.fromkeys(positions, "#D3D3D3"),
        size=350,
    )
    png = cairosvg.svg2png(bytestring=svg.encode("utf-8"))
    return png
