# C.A.R.E. 
- - -

## Panoramica
- - -


Il progetto __C.A.R.E.__ si pone l'obiettivo di creare un'app Android per raccogliere dati dai sensori di accelerometro e giroscopio montati su uno smartphone; questi vengono inviati in tempo reale ad un algoritmo di Machine Learning che classifica i dati raccolti in una classe del tipo “incidente” o “altro”. Con il termine "altro" si raggruppano tutti gli eventi di accelerazione constante, accelerazione improvvisa, frenata constante, frenata improvvisa, svolta a destra e svolta a sinistra. Se l’evento rilevato è “incidente”, il fenomeno in questione viene memorizzato all’interno di un database MongoDB per essere analizzato meglio in seguito dall’admin dell’app (responsabile della compagnia assicurativa) mediante opportune dashboard.
L'interfaccia è facile ed intuitiva e permette agli utenti di registrarsi, fare il login, di visualizzare in tempo reale i dati di accelerometro e giroscopio e l’evento che è stato rilevato. 

## ARCHITETTURA DEL SISTEMA
- - -

<div align="center">
  <img src="https://i.ibb.co/0GdR93q/Immagine-Whats-App-2024-11-13-ore-18-59-09-a730b518.jpg" alt="Architettura" width="400"/>
</div>



Le componenti principali dell’architettura sono: 

-	__Front end:__ Realizzato con Flutter, prevede inizialmente un’interfaccia di login e registrazione e, una volta loggato, l’utente può navigare all’interno della sua area riservata visualizzando i dati di accelerometro e giroscopio raccolti in tempo reale, lo storico dei suoi incidenti e le sue informazioni personali, con l’opportunità di poterle modificare. 

-	__Android Studio:__ Grazie all’utilizzo di questo IDE si è creata un’app in grado si acquisire dati in tempo reale dai sensori (accelerometro e giroscopio) situati sullo smartphone su cui l’app viene eseguita.
	Una volta acquisiti vengono inviati, grazie al protocollo MQTT, all’algoritmo di ML che classifica i dati in eventi di incidenti ed altro;

-	__Python:__ Si è addestrato un modello di Random Forest che è in grado di classificare, in base ai dati ricevuti in input, un evento, distinguendolo in una di queste due classi: incidente e altro.
Inoltre, grazie al framework Flask, si sono sviluppate delle API che hanno permesso alle varie componenti dell'applicazione di comunicare con il database MongoDB.


## REPOSITORY DEI COMPONENTI:
- - -
- Machine Learning C.A.R.E.: [Link al repository][git-repo-url1]
- Back-end C.A.R.E.: [Link al repository][git-repo-url2]
- Front-end C.A.R.E.: [Link al repository][git-repo-url3]
- [Pagina web][link_pagina_web]

## BACK-END C.A.R.E.
- - - 

## 1. Acquisizione dati
I dati sono stati acquisiti utilizzando delle opportune API di Android che hanno permesso al dispositivo che utilizza l'app di accedere ai propri sensori di accelerometro e giroscopio e di accedere ai loro dati in tempo reale.
Di seguito viene riportata la schermata iniziale dell’utente in cui sono riportati i dati dei sensori in tempo reale e l’evento rilevato:

<div align="center">
  <img src="https://i.ibb.co/N9bSjRp/Immagine-Whats-App-2024-11-13-ore-18-56-44-7f7cf23d.jpg" alt="ALTRO" width="200"/>
  <img src="https://i.ibb.co/CMDxBmy/Immagine-Whats-App-2024-11-13-ore-18-57-32-3aadfd35.jpg" alt="INCIDENTE" width="200"/>
</div>


## 2. API C.A.R.E

<div align="center">
  <img src="https://i.ibb.co/ynqP3GD/Immagine-Whats-App-2024-11-13-ore-20-24-58-0547847d.jpg" alt="API" width="600"/>
</div>

-	/api/utenti/registrazione: Registra un nuovo utente.
-	/api/utenti/login: Effettua il login per un utente esistente.
-	/api/utenti/delete/{username}: Elimina un utente in base al suo username.
-	/api/utenti/find_by_username/{username}: Recupera un utente in base al suo username.
-	/api/utenti/: Recupera tutti gli utenti loggati nel sistema.
-	/api/utenti/update/{username}: Aggiorna le informazioni di un utente in base al suo username.
-	/api/incidenti/add_incidenti: Aggiunge un nuovo incidente nel database.
-	/api/incidenti/get_incidenti_by_username/{username}: Recupera tutti gli incidenti relativi ad un particolare utente.
-	/api/incidenti/delete/{id}: Elimina un incidente in base al suo identificativo.
-	/api/incidenti/: Recupera tutti gli incidenti che sono presenti nel database.

Per maggiori informazioni visitare il file presente al seguente [link][link_API_C.A.R.E.]

## 3. Come iniziare:
1. Ambiente:

    ```
    DATABASE_URL=mongodb://db:27017/database
    DATABASE=database
    PASSWORD=*****
    USERNAME=****
    JWT_SECRET=*******
    ```

2. Build dell'immagine:
    
    ```
    docker-compose build
    ```

3. Avvio servizi:
    ```
    docker-compose up
    ```


  
   [git-repo-url1]: <https://github.com/UniSalento-IDALab-IoTCourse-2023-2024/wot-Sistema-intelligente-per-riconoscere-urti-Machine-Learning>
   
   [git-repo-url2]: <https://github.com/UniSalento-IDALab-IoTCourse-2023-2024/wot-Sistema-intelligente-per-riconoscere-urti-Backend>
    
   [git-repo-url3]: <https://github.com/UniSalento-IDALab-IoTCourse-2023-2024/wot-Sistema-intelligente-per-riconoscere-urti-Frontend>
   
   [link_pagina_web]: <https://unisalento-idalab-iotcourse-2023-2024.github.io/wot-project-presentation-Schirinzi-Paglialonga/>

   [link_API_C.A.R.E.]: <https://github.com/UniSalento-IDALab-IoTCourse-2023-2024/wot-Sistema-intelligente-per-riconoscere-urti-Backend-Schirinzi-Paglialonga/blob/main/app/src/API_C_A_R_E_.pdf>
   
   
   
   
   
   
   
   
   
   
  
