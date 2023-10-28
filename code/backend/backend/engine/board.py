
from .enums import Colors, Pieces
from .figures import Pawn, Rook, Knight, Bishop, Queen, King, Figure
from .const import FIGURES_MAP
from .helpers import coors2pos, onBoard
from .errors import OutOfBoardError, CellIsBusyError, NotFoundError, Draw, WhiteWon, BlackWon


class Board(object):
    _figures: dict[Colors, dict[Pieces, list[Figure]]]  = {}
    _figure_list: list[tuple[Pieces, list[Figure]]] = [] # TODO: check if type is correct
    _moves = []
    _cut = None

    def __init__(self, figures: None | Pieces = None, cut: list[Pieces] =[]):
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
    def figures(self):
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

    def loadFigures(self, line):
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

    def cell2Figure(self, x: int, y: int):
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
        fig = self.cell2Figure(x, y)
        if fig:
            if fig.color == figure.color:
                raise CellIsBusyError
            else:
                if isinstance(fig, King):
                    if fig.color == Colors.WHITE:
                        end_game = BlackWon
                    else:
                        end_game = WhiteWon
                self._figure_list.remove(fig)
                self._cut = fig
                self._cut_list.append((fig.kind, fig.color))
                fig.terminate()
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
