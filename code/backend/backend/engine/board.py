
from .enums import Colors, Pieces
from .figures import Pawn, Rook, Knight, Bishop, Queen, King, Figure
from .const import FIGURES_MAP
from .helpers import coors2pos, onBoard
from .errors import OutOfBoardError, CellIsBusyError, NotFoundError, Draw, WhiteWon, BlackWon


class Board(object):
    _figures: dict[Colors, dict[Pieces, list[Figure]]]  = {}
    _figure_list: list[tuple[Pieces, list[Figure]]] = []
    _moves = []
    _cut = None

    def __init__(self, figures: None | str = None, cut: list[Pieces] =[]):
        if figures is not None:
            self.loadFigures(figures)
        else:
            self.standFigures()
        self._cut_list = []
        if cut:
            for fig in cut:
                cls, color = FIGURES_MAP[fig]
                self._cut_list.append((cls.kind, color))

    def __str__(self):
        return ','.join(map(str, self.figures))

    @property
    def figures(self) -> list[Figure]:
        return self._figure_list
    
    @property
    def moves(self):
        return self._moves
    
    @property
    def lastCut(self):
        return self._cut

    @property
    def cuts(self):
        return self._cut_list

    def standFigures(self):
        self._figures = {
            Colors.WHITE: {
                Pieces.PAWN: [Pawn(x, 2, Colors.WHITE, self) for x in range(1, 9)],
                Pieces.ROOK: [Rook(x, 1, Colors.WHITE, self) for x in (1, 8)],
                Pieces.KNIGHT: [Knight(x, 1, Colors.WHITE, self) for x in (2, 7)],
                Pieces.BISHOP: [Bishop(x, 1, Colors.WHITE, self) for x in (3, 6)],
                Pieces.QUEEN: [Queen(4, 1, Colors.WHITE, self)],
                Pieces.KING: King(5, 1, Colors.WHITE, self)
            },
            Colors.BLACK: {
                Pieces.PAWN: [Pawn(x, 7, Colors.BLACK, self) for x in range(1, 9)],
                Pieces.ROOK: [Rook(x, 8, Colors.BLACK, self) for x in (1, 8)],
                Pieces.KNIGHT: [Knight(x, 8, Colors.BLACK, self) for x in (2, 7)],
                Pieces.BISHOP: [Bishop(x, 8, Colors.BLACK, self) for x in (3, 6)],
                Pieces.QUEEN: [Queen(4, 8, Colors.BLACK, self)],
                Pieces.KING: King(5, 8, Colors.BLACK, self)
            }
        }
        self._figure_list = []
        for color in (Colors.WHITE, Colors.BLACK):
            for figs in self._figures.get(color).values():
                if (isinstance(figs, list)):
                    for fig in figs:
                        self._figure_list.append(fig)
                else:
                    self._figure_list.append(figs)

    def loadFigures(self, line:str):
        figures = {
            Colors.WHITE: {Pieces.PAWN: [], Pieces.ROOK: [], Pieces.KNIGHT: [], Pieces.BISHOP: [], Pieces.QUEEN: [], Pieces.KING: None},
            Colors.BLACK: {Pieces.PAWN: [], Pieces.ROOK: [], Pieces.KNIGHT: [], Pieces.BISHOP: [], Pieces.QUEEN: [], Pieces.KING: None}
        }
        figure_list = []
        for fig in line.split(','):
            cls, color = FIGURES_MAP[fig[0]]
            x, y = coors2pos(fig[1:3])
            figure = cls(x, y, color, self)
            if cls == King:
                figures[color][cls.kind] = figure
            else:
                figures[color][cls.kind].append(figure)
            figure_list.append(figure)
        self._figures = figures
        self._figure_list = figure_list

    def cell2Figure(self, x: int, y: int) -> Figure | None:
        if not onBoard(x, y):
            raise OutOfBoardError
        for fig in self.figures:
            if fig.x == x and fig.y == y:
                return fig

    def isProtected(self, x, y, color):
        # deprecated because king can be cut
        if not onBoard(x, y):
            raise OutOfBoardError
        for fig in self.figures:
            if fig.color != color:
                continue
            if isinstance(fig, King):
                moves = fig.royalAura()
            else:
                moves = fig.getMoves()
            if (x, y) in moves:
                return True
        return False

    def move(self, figure, x: int, y: int):
        self._cut = None
        end_game = None

        if isinstance(figure, Pawn):
            self.__pawn_en_passant_capture_check(figure, x, y)

        fig = self.cell2Figure(x, y)
        if fig:
            if fig.color == figure.color:
                raise CellIsBusyError

            if isinstance(fig, King):
                if fig.color == Colors.WHITE:
                    end_game = BlackWon
                else:
                    end_game = WhiteWon

            self.__remove_piece(fig)

        #TODO(gio): refactor si può mettere in una classe l'oggetto mossa e inoltre non credo 
        # la figura ma basta sapere la figura come enum e il colore, non l'oggetto (che poi rimane in memoria a caso)
        # anche perché poi è difficile loadarle da una serie di mosse

        self._moves.append({
            'figure': figure, 
            'x1': figure.x,
            'y1': figure.y,
            'x2': x,
            'y2': y,
        })
        figure.x, figure.y = x, y
        self.updateFigures()
        if end_game:
            raise end_game
        for fig in self.figures:
            if fig.color == figure.color:
                continue
            if len(fig.getMoves()):
                return
        raise Draw

    def updateFigures(self):
        for fig in self.figures:
            fig.reset()
        for fig in self.figures:
            fig.update()

    def getFigure(self, color, kind, index=0):
        try:
            figs = self._figures[color][kind]
            if not figs:
                raise NotFoundError
            if isinstance(figs, list):
                return figs[index]
            return figs
        except Exception as e:
            raise NotFoundError

    def castle(self, king, rook):
        if rook.x == 8:
            king.x, rook.x = 7, 6
        else:
            king.x, rook.x = 3, 4
        self.updateFigures()

    def denyCastle(self, color, short=None):
        if short is None:
            self.getFigure(color, Pieces.KING)._moved = True
            return
        y = 1 if color == Colors.WHITE else 8
        rook_x = 8 if short else 1
        try:
            rook = self.cell2Figure(x=rook_x, y=y)
        except (NotFoundError, OutOfBoardError):
            return
        if rook:
            rook._moved = True

    def transform(self, pawn):
        queen = Queen(pawn.x, pawn.y, pawn.color, self)
        self._figures[pawn.color][Pieces.QUEEN].append(queen)
        self._figure_list.append(queen)
        self._figure_list.remove(pawn)
        pawn.terminate()

    def get_view(self, color: Colors) -> str:
        """Returns the view of the board from the perspective of the color

        """
        view = [
            ['.' for _ in range(8)] for _ in range(8)
        ]

        for fig in self.figures:
            view[fig.y - 1][fig.x - 1] = fig.symbol

        # create not visible mask
        mask: list[bool] = [
            [True for _ in range(8)] for _ in range(8)
        ]

        for fig in self.figures:
            if fig.color == color:
                mask[fig.y - 1][fig.x - 1] = False
                for x, y in fig.getVisibleCells():
                    mask[y - 1][x - 1] = False

        # apply mask
        for y in range(8):
            for x in range(8):
                if mask[y][x]:
                    view[y][x] = 'X'

        return '\n'.join(''.join(row) for row in view)

    def compute_fen(self, current_player: Colors) -> str:
        """ Return the Forsyth-Edwards Notation of the board
        
        Reference: https://en.wikipedia.org/wiki/Forsyth%E2%80%93Edwards_Notation
        """
        rows = [] 
        TABLE_SIZE = 8
        for y in range(TABLE_SIZE, 0, -1): # invert so that the white is at bottom
            empty_space_count = 0
            row_string = ""
            for x in range(1, TABLE_SIZE + 1):
                piece_in_current_cell = self.cell2Figure(x, y)
                
                if piece_in_current_cell is None:
                    empty_space_count += 1
                else:
                    if empty_space_count > 0:
                        row_string += str(empty_space_count)
                        empty_space_count = 0
                    row_string += piece_in_current_cell.symbol

            if empty_space_count > 0:
                row_string += str(empty_space_count)
            rows.append(row_string)

        current_player = "w" if current_player == Colors.WHITE else "b"

        # TODO "-" is instead for en passant and isn't implemented yet
        # also the number of semimoves is debatable in this verion of chess

        black_moves = len(self._moves) // 2
        return f"{'/'.join(rows)} {current_player} {self.__compute_castle_string()} - 0 {1 + black_moves}" 

    def toTextChessBoard(self) -> str:
        # TODO: use me
        out = [['.' for _ in range(8)] for _ in range(8) ]
        for piece in self._figure_list:
            out[piece.y - 1][piece.x - 1] = piece.symbol

        return out.join('\n')

    def resetEnPassant(self):
        for fig in self.figures:
            if isinstance(fig, Pawn):
                fig.en_passant = False

    def __compute_castle_string(self) -> str:
        # Check if white king can castle
        white_king: King = self.getFigure(Colors.WHITE, Pieces.KING)
        white_rook_short: Rook = self.cell2Figure(x=8, y=1)
        white_rook_long: Rook = self.cell2Figure(x=1, y=1)
        final_string = ""

        if not white_king.moved:
            if white_rook_short is not None and not white_rook_short.moved:
                final_string += "K"
            if white_rook_long is not None  and not white_rook_long.moved:
                final_string += "Q"

        # Check if black king can castle
        black_king = self.getFigure(Colors.BLACK, Pieces.KING)
        black_rook_short = self.cell2Figure(x=8, y=8)
        black_rook_long = self.cell2Figure(x=1, y=8)

        if not black_king.moved:
            if black_rook_short is not None and not black_rook_short.moved:
                final_string += "k"
            if black_rook_long is not None and not black_rook_long.moved:
                final_string += "q"
        
        if len(final_string) == 0:
            return "-"

        return final_string

    def __pawn_en_passant_capture_check(self, pawn: Pawn, x: int, y: int) -> None:
        if pawn.x == x: # same column = no capture
            return
        
        fig = self.cell2Figure(x, y)
        if fig is not None:
            return # normal capture, pawn captured a piece

        captured_fig = None
        if pawn.color == Colors.WHITE:
            captured_fig = self.cell2Figure(x, y - 1)
        else:
            captured_fig = self.cell2Figure(x, y + 1)

        self.__remove_piece(captured_fig)

    def __remove_piece(self, figure: Figure):
        self._figure_list.remove(figure)
        self._cut = figure
        self._cut_list.append((figure.kind, figure.color))
        figure.terminate()