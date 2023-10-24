Author: Xuanqiang "Angelo" Huang

## Argomenti trattati

- [x] studio fattibilità sulle varianti, ricerca di algoritmi online open source che le giochino in maniera efficiente, e conseguente scelta delle 2 più fattibili(produzione di un po' di documentazione sullo stato dell'arte)
- [ ] testare le piattaforme software proposte la loro complessità di utilizzo e conseguente scelta di utilizzo o meno(in caso di software opzionale)
- [ ] sempre per le piattaforme, che dovranno essere tutte self hosted, capire come hostarle e quali sono più convenienti anche sotto questo punto di vista

> Occorre costruire un’app che permetta di giocare online una o più varianti tra quelle elencate nella Sezione 1

Questo significa che sarà una **web app**

## Inizio analisi varianti

### Really Bad Chess
[sito](http://www.reallybadchess.com/)[wiki](https://en.wikipedia.org/wiki/Really_Bad_Chess) . Bisogna scaricarsi una app e provarlo (variante abbastanza recente)

1. Pezzi di ogni giocatore sono random, ma si muovono come gli altri.
2. Non è possibile fare pareggio con la [threefold repetition](https://en.wikipedia.org/wiki/Threefold_repetition)
3. Chi subisce stalemate perde, invece di pareggiare.

Molto semplice da cambiare rispetto al chess standard.
1. Cambiare lo stato iniziale del gioco
2. Cambiare condizioni di vittoria

**AI**: non ho trovato modelli presenti, le ricerche sono inquinate con "Bad chess"

### Dark Chess
[wiki](https://en.wikipedia.org/wiki/Dark_chess) 
Features:
- Vittoria se il re è stato mangiato.
- Un giocatore vede solo le caselle attaccabili dai suoi pezzi
- Le caselle buie sono chiaramente mostrate ai giocatori.
- L'arrocco è consentito anche se le caselle di mezzo sono sotto attacco.

Questa variante, dato il gioco normale, è molto semplice da implementare.
1. oscurare i pezzi avversari
2. Cambiare condizione di vittoria
3. Cambiare la logica d'arrocco (non dovrebbe essere difficile).

**AI**: [ImpCatcher](https://github.com/anoojpatel/ImpCatcher) in Julia language. Si dovrebbe fare un wrapper con un linguaggio che utilizziamo.
**AI2**: [paper](https://dspace.cvut.cz/bitstream/handle/10467/95455/F3-DP-2021-Foret-Vojtech-zaverecna_prace.pdf?isAllowed=y&sequence=-1) , [framework code](https://github.com/google-deepmind/open_spiel)
[qui](https://www.chess.com/forum/view/chess-variants/fog-of-war-chess-engine) affermano che non ci sono modelli per AI, questa variante era presente solo su chess.com.
### Scacchi Reconnaissance Blind
[regole](https://rbc.jhuapl.edu/gameRules)

Features 
- A player cannot see their opponent's pieces.
- Prior to making each move, a player selects a 3x3 region of the chess board to “sense” the pieces in that region. The player is informed of the true piece configuration within the sensed 3x3 region. The opponent is not informed about where the player sensed.
- When a player captures a piece, they are informed that they made a capture, but they are not informed about what piece they captured.
- When a player's piece is captured, they are informed that their piece was captured, but they are not informed about what piece captured it.
- There is no notion of check or mate because players may be unaware of a check relationship.
- A player wins by capturing the opponent's king or when the opponent runs out of time. Each player begins with a cumulative 15-minute clock to make all their moves, and gains 5 seconds on that clock after each turn.
- A game is automatically declared a draw after 50 turns without a pawn move or capture. This mirrors the [50-move rule](https://en.wikipedia.org/wiki/Fifty-move_rule) in chess, except here neither player needs to claim the draw for the game to end.
- If a player tries to move a sliding piece through an opponent's piece, the opponent's piece is captured and the moved piece is stopped where the capture occurred. The moving player is notified of the square where the piece landed, and both players are notified of the capture.
- If a player attempts to make an illegal move, such as moving a pawn diagonally to an empty square, moving a pawn forward to an occupied square, or a castling through an interposing piece, they are notified that the move did not succeed and their turn is over. However, castling through check is allowed because the notion of check is removed.
- There is a "pass" option that a player can select if they prefer to make no move during their turn.

Molto più complesso rispetto le altre varianti.
Ma ha Paper di AI ongoing, quindi l'AI si trova in modo molto semplice.
**AI**: ce ne sono anche troppi, quello più forte è  *strangeFish* [github](https://github.com/ginop/reconchess-strangefish).

### Scacchi invisibili (Kriegspiel)
[wiki](https://en.wikipedia.org/wiki/Kriegspiel_(chess)) , [sito cianca](https://www.cs.unibo.it/~cianca/wwwpages/chesssite/kriegspiel/kriegspiel.html).

Features:
- Nessun pezzo dell'avversario è visibile
- Il giocatore sa se la mossa che ha fatto ha catturato un pezzo o ha fatto scacco.
- Ogni mossa è dichiarata o legale o illegale, se illegale può muovere di nuovo
- È possibile richiedere se ci sono catture legali con pawns.

**AI**: [paper](https://dspace.cvut.cz/bitstream/handle/10467/95455/F3-DP-2021-Foret-Vojtech-zaverecna_prace.pdf?isAllowed=y&sequence=-1) , [framework code](https://github.com/google-deepmind/open_spiel)

### Proposta
Per quanto riguarda la difficoltà di implementazione, si potrebbero implementare Dark Chess e Kriegspiel (anche molto simili fra di loro) che sono sia facili da implementare che con AI già pronta (da collegare).
Random chess non ha buona ai, reconnaisance è più difficile da implementare, ma ha molte AI (on-going competition). Cercando di ottimizzare per tempo investito mi sembra che Dark Chess e KriegSpiel siano adatti.

### Linguaggio
Per la scelta del linguaggio opterei per quello meglio conosciuto dopo le esperienze web.
Avremo un front-end con un framework fra React, Angular e Vue.
Backend potremmo tenerlo in JS oppure typescript che tutti conosciamo dopo web.
Anche la scelta di python potrebbe essere sensata per facilità di integrazione di AI.

### Lista alcuni engines esistenti
- https://github.com/kurt1288/KhepriChess, **typescript** scritta male, un singolo file, necessita refactor
- https://github.com/raydog/deno-chess, **typescript**, scritta bene.
- https://github.com/niklasf/python-chess/ **python**, ben documentato, ma singolo file di engine.