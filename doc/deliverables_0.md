Authors:
    - Xuanqiang "Angelo" Huang
    - Emanuele Pischetola

# Deliverables sprint - 0

Questo documento contiene alcuni commenti sui deliverables del primo sprint.

- Architettura ad alto livello del nostro sistema
- Un diagramma use-case
- Un mockup dell'interfaccia grafica (wireframes)
- Relazione scrumble
- Autovalutazione scrumble
- Relazione Escape the boom

Inoltre abbiamo prodotto qualche documento in più durante questa prima fase:
- [Analisi delle varianti di scacchi](analisi-chess-variants.md)
- [Analisi delle api-social](analisi-social.md)
- [Descrizione del sistema di deployment](deployment.md)

## Architettura ad alto livello
![architecture](images/architecture.jpg)

Abbiamo immaginato un'architettura a microservizi, in cui ogni servizio è indipendente dagli altri e comunica tramite API REST. In questo modo, è possibile scalare ogni servizio in modo indipendente, e anche sostituirlo con un'implementazione diversa, purché rispetti l'interfaccia.

Gli esempi di microservizi:
- Chess Engine (the bot player)
- Database
- Backend Webapp

Solamente la webapp è accessibile dall'utente, mentre gli altri servizi sono accessibili solamente internamente.
L'api per i social sarà gestito dal backend webapp.

## Diagramma use-case
![use case](images/use_case.png)

Abbiamo immaginato 3 attori:
- Utente non registrato
- Utente registrato (socio FISE)
- Chess Engine

Il primo potrà solamente autenticarsi e registrarsi, mentre il secondo potrà giocare e vedere la classifica degli utenti.
L'ultimo attore è il bot che può giocare o commentare le partite.


## Mockup dell'interfaccia grafica

![mockup1](images/mockup-1.png)
![mockup2](images/mockup-2.png)

Il mockup si può dividere tra *landing page* e *game page*.

- landing page: è la prima pagina che vede l'utente e sono presenti 2 versioni, in base all'autenticazione
- game page: è la pagine in cui l'utente può interagire con la scacchiera e sia in modalità online che contro il bot

## Scrumble - Relazione

Vedere la relazione a parte, [qui](teambuilding/scrumble.md)

## Scrumble - Autovalutazione

|GOAL           |QUESTIONS        |EVALUATION                                                                                                               |Alessandro|Huang|Emanuele|Filippo|Diego|Bernardo|Giovanni|                                                     |                                                            |
|---------------|-----------------|-------------------------------------------------------------------------------------------------------------------------|----------|-----|--------|-------|-----|--------|--------|------------------------------------------------------------|-------------------------------------------------------------------|
|Learn          |Q1               |1 = no idea of the Scrum roles 5 = perfect knowledge of the roles and their jobs                                         |4         |4    |4       |3      |4    |3       |5       |Do team members understand the Scrum roles?                 |Knowledge of Scrum roles by questions                              |
|               |Q2               |1 = couldn't repeat the game  5 = could play the game as a Scrum Master by himself                                       |4         |3    |5       |4      |3    |3       |3       |Do team members feel they learned the process?              | Opinions from the participants                                    |
|               |Q3               |1 = totally lost 5 = leads the game driving the other players                                                            |4         |3    |5       |3      |3    |3       |3       |Does everyone keep up with the other players?               |Check during every sprint retrospective if every one is on point   |
|Practice       |Q4               |1 =  feels the game is unrepeatable 5 =  feels the game could be played in any situation                                 |3         |2    |3       |3      |3    |3       |3       |Are the game mechanics linear and repeatable?               |Opinions from the participants                                     |
|               |Q5               |1 = 0 to 3 stories       2 = 4 to 6     3 = 7 to 9 4 = 10 to 12       5 = 13 to 15                                       |1         |1    |1       |1      |1    |1       |1       |Do team success in completing the game?                     | Number of User Stories completed                                  |
|               |Q6 ONLY DEV TEAM |1 = abnormal difference from the other players 5 = coherent and uniform with the group most of the time                  |4         |5    |X       |5      |X    |4       |5       |Do team members efficiently estimate during sprint planning?|Uniformity in evaluating the size and the priority of user stories |
|Cooperation    |Q7               |1 = never speaks with the other players 5 = talks friendly to anyone in every situation                                  |3         |4    |3       |3      |4    |4       |3       |Do team members know each other better?                     |Level of players' serenity throughout the game                     |
|               |Q8               |1 = never puts effort in doing something  5 = every time is willing to understand what is going on                       |3         |5    |4       |3      |4    |3       |3       |Does the game let all players cooperate?                    |Contribution of every player during the game                       |
|               |Q9               |1 = never asks for an opinion 5 =  wants to discuss about every topic                                                    |4         |4    |4       |4      |4    |4       |4       |Do team member consult each other about a topic?            |Sharing of ideas                                                   |
|Motivation     |Q10              |1 = not involved by the game 5 = always makes sure everyone is on point                                                  |3         |5    |4       |4      |4    |4       |5       |Do team members encourage collegues in need?                |Players explain something other players don't understand           |
|               |Q11 ONLY FOR PO  |1 = poor/absent advices 5 = wise and helpful suggestions when is required                                                |X         |X    |X       |x      |4    |x       |x       |Does PO help the team?                                      |Quality of PO's advices to get better in the next sprints          |
|               |Q12              |1 = doesn't express opinions during retrospective 5 = feels the retrospective fundamental to express opinions            |4         |5    |4       |5      |5    |4       |5       |Does the team come up with good ideas?                      |Effectiveness of sprint retrospective                              |
|Problem Solving|Q13              |On the game board, if the debt pawn is on the lowest stage, the evaluation is 5, for every higher stage it decreases by 1|5         |5    |5       |5      |5    |5       |5       |Do team members behave well when facing a problem?          |Level of the technical debt at the end of the game                 |
|               |Q14 ONLY DEV TEAM|Calculate the average of tasks left for each sprint: 1 = 21+   2 = 16-20   3 = 11-15   4 = 6-10   5 = 0-5                |4         |4    |X       |4      |X    |4       |4       |Does team organize their tasks properly?                    |Average of tasks left at the end of each sprint                    |
|               |Q15 ONLY FOR PO  |Same evaluation as Q14 for the PO                                                                                        |x         |x    |X       |x      |4    |x       |x       |Does PO plan efficiently the Sprint Backlog?                |Average of tasks left at the end of each sprint                    |


## Escape the boom - Relazione

Vedere la relazione a parte, [qui](teambuilding/escape-the-boom.md)