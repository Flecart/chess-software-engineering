Author: Alessandro Neri

# Analisi
Dopo aver svolto alcune ricerche sono giunto alla conclusione che twitter, facebook, telegram e whatsapp siano i social network più semplici da utilizzare per gli scopi richiesti e con altre caratteristiche utili.

In particolare è possibile condividere post e messaggi sui seguenti social tramite i link:
- facebook: https://www.facebook.com/sharer/sharer.php?u= *link alla partita*
- twitter: https://twitter.com/intent/tweet?text= *testo del tweet che comprende il link alla partita*
- whatsapp: https://api.whatsapp.com/send?text= *testo del messaggio che comprende il link alla partita*
- telegram: https://t.me/share/url?text= *testo del messaggio*

Per maggiori informazioni:
- facebook: [qui](https://developers.facebook.com/docs/plugins/share-button/)
- twitter: [qui](https://developer.twitter.com/en/docs/twitter-for-websites/tweet-button/overview)
    - navigando sul sito di twitter si può trovare molta documentazione, ad esempio altri query parameters, [qui](https://developer.twitter.com/en/docs/twitter-for-websites/web-intents/overview)
- telegram: [qui](https://core.telegram.org/widgets/share)
    - navigando sul sito di telegram si può trovare altra documentazione, è ad esempio possibile scaricare l'icona [qui](https://telegram.org/press#telegram-logos)

## Altri strumenti utili e idee per il futuro
Ho in oltre trovato alcune interessanti librerie che potranno essere utili per il futuro. In particolare le api di twitter possono essere utilizzate per creare un'account bot che retweeta i post degli utenti che cercano partite e tweeta quando viene organizzato un torneo.

In particolare esistono librerie per utilizzare queste API in:
- python: [tweepy](https://www.tweepy.org/)
- node: [node-twitter](https://github.com/desmondmorris/node-twitter)

## Osservazioni
L'interfaccia di creazione di un post di facebook non è quella rimodernata attuale, ma è quella di vecchia generazione(bianca e blu).

Whatsapp non ha una documentazione esaustiva.

## Conclusioni
Preso atto dei social presi in considerazione, delle loro potenzialità e dei loro limiti, ritengo che sia vantaggioso scegliere twitter per una condivisione su larga scala e telegram per una condivisione mirata.