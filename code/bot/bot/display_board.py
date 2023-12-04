import chess
import chess.svg
import cairosvg

def _to_standard_fen(fen):
    fen = fen.split(' ')
    countEmptyCell = 0
    newFen = ''
    # we transform the first part of fen that contains X to a normal fen
    for i in range(len(fen[0])):
        if fen[0][i] == '/':
            if countEmptyCell > 0:
                newFen += str(countEmptyCell)
            newFen += '/'
            countEmptyCell = 0
        elif fen[0][i] == 'X':
            countEmptyCell += 1
        elif fen[0][i].isdigit():
            countEmptyCell += int(fen[0][i])
        else:
            if(countEmptyCell > 0):
                newFen += str(countEmptyCell)
            newFen += fen[0][i]
            countEmptyCell = 0
    if(countEmptyCell > 0):
        newFen += str(countEmptyCell)
    
    print(newFen)

    return ' '.join([newFen]+fen[1:])

def _get_not_visible_squares(fen):
    fen = fen.split(' ')[0]
    col = 0
    row = 7
    position = []
    for i in range(len(fen)):
        if fen[i] == '/':
            row-=1
            col = 0
        elif fen[i].isdigit():
            col+=int(fen[i])
        else:
            col+=1
            if fen[i] == 'X':
                position.append((row,col))

    return position
                

def custom_fen_to_svg(fen):


    positions = list(map(lambda x: chess.square(x[1],x[0])-1 ,
                          _get_not_visible_squares(fen)))

    print(positions)

    board = chess.Board(_to_standard_fen(fen))

    svg = chess.svg.board(
        board,
        fill=dict.fromkeys(positions, "#D3D3D3"),
        size=350,
    )  
    png = cairosvg.svg2png(bytestring=svg.encode('utf-8'))
    return png