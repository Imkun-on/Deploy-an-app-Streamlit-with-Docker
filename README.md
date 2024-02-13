<!DOCTYPE html>
<html>

<body>

<h1>Progetto Cloud Computing</h1>
<h2>L'applicazione</h2>
<p> Ai fini di questo progetto, ho utilizzato un'applicazione Streamlit che fornisce informazioni dettagliate sulle carte di Yu-Gi-Oh! a partire dal 2000 fino ad oggi. </p> 
<p> Questa applicazione è progettata per capire quali sono le carte più apprezzate, visualizzate, bannate e criticate per la loro potenza o rarità.</p>

<h2>Quali sono i passaggi?</h2>
<p> L’idea è quella di distribuire l’applicazione utilizzando Amazon Web Services (AWS) ed i suoi prodotti basati su cloud.</p>
<p> Per avere un’applicazione funzionante sul cloud, questi sono i passaggi che ho seguito: </p>
<ul>
<li>Creazione di un’immagine Docker dell’applicazione e delle relative dipendenze.</li>
<li>Creazione delle istanze virtuali con AWS EC2.</li>
<li>Creazione di uno Swarm Docker composto da un gestore e tre nodi worker.</li>
<li>Creazione di servizi Postgre, Apache e Redis.</li>
<li>Creazione di uno Stack Docker in modo che nessuno stack venga eseguito sul nodo Manager.</li>
<li>Archiviazione su Docker Hub.</li>
</ul>
<br> </br>
<h2> Creazione di un’immagine Docker dell’applicazione e delle relative dipendenze.</h2>
<p>
La creazione dell’immagine docker l’ho applicata per creare tutto ciò di cui ho bisogno per eseguire il software, quindi codice, librerie, variabili; cioè a distribuire quel pacchetto ed eseguire il software in un ambiente containerizzato.
Prima di creare l’immagine Docker sono andato a creare prima un file in formato testo denominato “requirements.txt” dove al suo interno sono incluse tutte le librerie con le specifiche versioni sia per l’analisi descrittiva dei dati che per la creazione dell’applicazione streamlit.
</p>

<p>Dopo aver creato il file “requirements.txt”, sono andato a creare il file Docker utilizzando questi codici:</p>

<pre>
<code>
# Usa un'immagine base di Python
FROM python:3.8

# Imposta una directory di lavoro
WORKDIR /app

# Copia i file necessari nell'immagine
COPY . /app

# Installa le dipendenze
RUN pip install -r requirements.txt

# Espone la porta 8501 (porta predefinita di Streamlit)
EXPOSE 8501

# Comando per eseguire l'applicazione
CMD ["streamlit", "run", "app.py"]
</code>
</pre>

<p>Dopo aver creato il file Docker sono andato a trasferire tutti i file sul mio profilo github.</p>

<br> </br>

<h2>Creazione delle istanze virtuali con AWS EC2.</h2>
<p>
Per la creazione delle istanze virtuali ho utilizzato Amazon Web Service (AWS) ed ho utilizzato Amazon Elastic Compute Cloud (EC2) per crearne 4 che risultano idonee al piano gratuito. Per la creazione delle istanze virtuali idonee alla mia applicazione ho selezionato:
</p>
<ul>
<li><strong>Tipologia di istanza</strong>: t2.micro</li>
<li><strong>Autorizzazione del traffico </strong>: HTTPS & HTTP  per configurare un endpoint, ad esempio durante la creazione di un server Web)</li>
<li><strong>Autorizzazione del modulo di traffico </strong>: SSH (per connettermi alla mia istanza virtuale)</li>
<li><strong> Amazon Machine Image (AMI) </strong>: Ubuntu Server 22.04 LTS (HVM).</li>
<li><strong> Creazione di una coppia di chiavi </strong>: per la registrazione in formato pem per l’utilizzo con OpenSSH.</li>
</ul>

<p>Dopo aver creato queste 4 istanze ho dovuto aggiungere ulteriori regole di sicurezza oltre a quelle già predefinite.</p>

<table>
<tr>
<th>PROTOCOLLO</th>
<th>INTERVALLO PORTE</th>
<th>ORIGINE</th>
<th>DESCRIZIONE</th>
</tr>
<tr>
<td>TCP</td>
<td>2376</td>
<td>0.0.0.0/0</td>
<td>Questa porta è necessaria per il funzionamento di Docker Machine. Docker Machine viene usato per orchestrare gli host Docker.</td>
</tr>
<tr>
<td>TCP</td>
<td>2377</td>
<td>0.0.0.0/0</td>
<td>Usata per la comunicazione tra i nodi di uno sciame Docker o di un cluster.</td>
</tr>
<tr>
<td>TCP</td>
<td>7946</td>
<td>0.0.0.0/0</td>
<td>Usata per la comunicazione tra i nodi (container network discovery).</td>
</tr>
<tr>
<td>TCP</td>
<td>8501</td>
<td>0.0.0.0/0</td>
<td>Usata come porta predefinita per le applicazioni Streamlit.</td>
</tr>
<tr>
<td>UDP</td>
<td>4789</td>
<td>0.0.0.0/0</td>
<td> Usata per il traffico di rete sovrapposto (rete in entrata del contenitore).</td>
</tr>
</table>

<p>Per avere un organizzazione migliore con queste istanze vado ad attribuirgli un nome ossia:</p>
<ul>
<li>Node_Master</li>
<li>Node_1</li>
<li>Node_2</li>
<li>Node_3</li>
</ul>
<p>Questo per poter utilizzare meglio Docker Swarm.</p>

<br></br>

<h2>Creazione di uno Swarm Docker composto da un gestore e tre nodi worker.</h2>
<p>
Per l’assegnazione dei ruoli alle istanze utilizzo Docker Swarm per creare uno sciame Docker composto da un manager e 3 utenti.
</p>
<p>
Quindi comincio con l’avviare il Node_Master e inserisco nel terminale questi comandi:
</p>

<p> Aggiorno l'elenco dei pacchetti disponibili e le loro versioni, ma non installa o aggiorna alcun pacchetto. sudo consente di eseguire il comando come superutente (root), garantendo i permessi necessari per aggiornare gli elenchi dei pacchetti. </p> 
<p> apt è il gestore di pacchetti utilizzato nelle distribuzioni Debian e Ubuntu.</p>
<pre><code>
sudo apt update
</code></pre>
<p> Installo Docker dalla repository di pacchetti ufficiale del tuo sistema operativo. Anche qui, sudo permette di eseguire il comando con privilegi di root, che sono necessari per installare software sul sistema. </p>
<p> docker.io è il nome del pacchetto di Docker nelle repository di pacchetti ufficiali di Ubuntu e altre distribuzioni basate su Debian. </p>
<pre><code>
sudo apt install docker.io
</code></pre>
<p> Avvio il servizio Docker utilizzando systemctl, che è un sistema di gestione dei servizi per Linux che usa systemd. Questo comando fa sì che Docker (il programma in background) venga avviato, permettendo l'esecuzione di container Docker sul sistema. Anche in questo caso, sudo è necessario per ottenere i permessi adeguati per avviare i servizi di sistema. </p>
<pre><code>
sudo systemctl start docker
</code></pre>
<p> Abilito il servizio Docker a essere avviato automaticamente all'avvio del sistema. Questo assicura che Docker sia disponibile anche dopo un riavvio del sistema, senza che sia necessario avviarlo manualmente ogni volta. systemctl con enable crea dei collegamenti simbolici necessari per avviare il servizio Docker durante il processo di avvio del sistema. </p>
<pre><code>
sudo systemctl enable docker
</code></pre>
<p> Aggiungo l'utente corrente al gruppo docker, permettendo così all'utente di eseguire i comandi Docker senza dover utilizzare sudo ogni volta. </p>
<p> -aG sta per "append to group" (aggiungi al gruppo), e docker è il nome del gruppo. ${USER} è una variabile d'ambiente che rappresenta il nome dell'utente corrente.  </p>
<pre><code>
sudo usermod -aG docker ${USER}
</code></pre>
<p>
Per verificare se le modifiche sono state eseguite con successo mi disconnetto e riconnetto nella seguente istanza.
</p>
<p>
Procedo con l’assegnazione del ruolo manager con questo codice:
</p>
<pre><code>
docker swarm init --advertise-addr 172.31.92.118
</code></pre>
<p>
ottenendo come output una conferma che questa istanza ora è diventata manager e fornendomi un codice per assegnare alle altre istanze il ruolo di utente.
</p>
<pre><code>
docker swarm join --token SWMTKN-1-2ca4tuegeusncn42i02l8lw4yc8t8vzpj5ovw1ewm8i98h6tmp-eqouyv9esuom2moygvjgrltj8 172.31.92.118:2377
</code></pre>
<p>
Questo codice devo andarlo ad inserire ad ogni istanza utente che ho creato in modo da poter creare uno sciame.
</p>
<p>
Ritorno al nodo manager ed utilizzo il seguente comando per osservare tutti i nodi con i rispettivi ruoli:
</p>
<pre><code>
docker node ls
</code></pre>

<br></br>

<h2>Distribuzione dell’applicazione.</h2>
<p>
Prima di creare un servizio nello sciame, ho deciso di distribuire l’applicazione attraverso un metodo particolare, ossia:
</p>

<p> Clono il codice sorgente di un'applicazione Streamlit che è stata preparata per essere eseguita come un container Docker dalla mia repository di github. </p>
<pre><code>
git clone https://github.com/Imkun-on/Streamlit-app-Docker.git
</code></pre>
<p> Elenco i file e le directory nel percorso corrente, anche per verificare che la clonazione sia andata a buon fine e per visualizzare i contenuti della directory di lavoro corrente. </p>
<pre><code>
ls
</code></pre>
<p> Cambio la directory corrente alla directory appena clonata Streamlit-app-Docker, che contiene il Dockerfile e i file sorgente dell'applicazione. </p>
<pre><code>
cd Streamlit-app-Docker/
</code></pre>
<p> Nuovamente, elenco i file e le directory nella directory corrente, ora all'interno di Streamlit-app-Docker, per mostrare il contenuto della directory dell'applicazione. </p>
<pre><code>
ls
</code></pre>
<p> Creo un'immagine Docker per l'applicazione Streamlit, utilizzando il Dockerfile presente nella directory corrente. L'immagine viene taggata con il nome. </p> 
<pre><code>
docker build -t imkun/nome-app-streamlit .
</code></pre>
<p> Elenco tutte le immagini Docker disponibili sul sistema, permettendomi di vedere l'immagine appena creata e altre immagini che potrebbero essere presenti. </p>
<pre><code>
docker images -a
</code></pre>
<p> Avvio un container Docker in modalità "detached" (in background) utilizzando l'immagine imkun/nome-app-streamlit, mappando la porta 8501 del container sulla porta 8501 dell'host. </p>
<p> Questo mi permette di accedere all'applicazione Streamlit tramite il browser all'indirizzo dell'host sulla porta 8501. </p>
<pre><code>
docker run -d -p 8501:8501 imkun/nome-app-streamlit
</code></pre>
<p> Elenco tutti i container Docker attualmente in esecuzione, permettendomi di verificare che il container dell'applicazione sia avviato correttamente. </p>
<pre><code>
docker ps
</code></pre>
<p> Fermo un container Docker in esecuzione, specificando l'ID o il nome del container come argomento. </p>
<pre><code>
docker stop &lt;nome_container o id&gt;
</code></pre>
<p> Rimuovo tutti i container Docker fermati, pulendo il sistema dai container non più necessari. docker ps -a -q elenca gli ID di tutti i container, e docker rm li rimuove. </p>
<pre><code>
docker rm $(docker ps -a -q)
</code></pre>

<br></br>

<h2>Creazione di servizi.</h2>
<p>
Creo un servizio Docker nel contesto di un cluster Docker Swarm dal nodo manager, avviando l'applicazione come un servizio distribuito con 4 repliche (istanze) del container, rendendo l'applicazione altamente disponibile e scalabile.
</p>
<pre><code>
docker service create --name nome-app-streamlit --replicas 3 -p 8501:8501 imkun/nome-app-streamlit:latest (da inserire al codice sopra)
</code></pre>
<p>Applico la stessa procedura per i servizi Postgree,Apache e Redis, specificando il numero di repliche e versione del servizio (per vedere la versione del servizio sono andato su Docker Hub): </p>
<pre><code>
docker service create --name redis --replicas 4 redis:latest
</code></pre>
<pre><code>
docker service create --name apache --replicas 4 httpd
</code></pre>
<pre><code>
docker service create --name postgres --replicas 1 \
  -e POSTGRES_PASSWORD=Databas3 \
  postgres
</code></pre>
<p>Il motivo per cui ho selezionato questi servizi è per il fatto che:</p>
<ul>
  <li><strong>Apache</strong>: può fungere da reverse proxy, indirizzando le richieste dal web alla mia applicazione Streamlit. Questo mi permette di esporre la tua app su Internet in modo sicuro e gestire meglio il traffico in ingresso.
inoltre se l'applicazione cresce in popolarità, Apache può aiutare a distribuire il carico tra più istanze dell'applicazione, migliorando le prestazioni e la disponibilità.</li>
  <li><strong>Redis</strong>: per le operazioni asincrone o di lunga durata, come l'importazione di grandi set di dati o l'esecuzione di analisi complesse, Redis può gestire le code di lavori, migliorando l'efficienza dell'applicazione.</li>
  <li><strong>PostgreSQL</strong>: può servire come database principale per memorizzare i dati di Yu-Gi-Oh!, inclusi mazzi, carte, statistiche di gioco, e altro ancora.</li>
</ul>
<p>
Dopo aver creato questi servizi, verifico se sono presenti tutti quanti: </p>
<pre><code>
docker service ls
</code></pre>
<p>Poi seleziono una qualsiasi istanza che fa parte dello sciame, eseguo la connessione, copio l’indirizzo Ip pubblico, lo incollo nel browser e inserisco il numero della porta 8501, ed ecco che la mia app si può vedere. </p>

<br></br>

<h2> Creazione di uno Stack Docker in modo che nessuno stack venga eseguito sul nodo Manager.</h2>
<p> Poichè abbiamo molti servizi vado ad utilizzare Stack Docker che mi consente di distribuire e raggruppare logicamente più servizi, che sono contenitori distribuiti in uno sciame. Quindi rimuovo tutti i servizi che ho creato.</p>
<pre><code>
docker service rm $(docker service ls -q)
</code></pre>
<p> Poi vado a creare un file con estensione yml specificando tutti i servizi che devo utilizzare nella mia streamlit e distribuisco lo stack utilizzando questo comando:</p>
<pre><code>
docker stack deploy --compose-file docker-compose.yml mio_stack
</code></pre>
<p> Infine vado a guardare sia i servizi nel mio stack ed anche se non sono in esecuzione sul nodo di gestione attraverso i seguenti codici: </p>
<pre><code>
docker stack ls
</code></pre>pre>
<pre><code>
docker stack ps mio_stack
</code></pre>
<p> </p>
<br></br>

<h2>Archiviazione dell’immagine Docker su Docker Hub.</h2>
<p>
Prima di procedere con il successivo comando, sono andato a creare un profilo su Docker Hub, in modo da archiviare l’app.
</p>
<p> Effettuo il login al Docker Hub, permettendomi di caricare (push) o scaricare (pull) immagini Docker. </p>
<pre><code>
docker login
</code></pre>
<p> Carico l'immagine taggata “latest” dell'applicazione al Docker Hub sotto il nome imkun/nome-app-streamlit. </p>
<pre><code>
docker push imkun/nome-app-streamlit:latest
</code></pre>
<p> Rimuovo l'immagine Docker specificata dal sistema locale. </p>
<pre><code>
docker rmi imkun/nome-app-streamlit:latest
</code></pre>
<p> Scarico l'immagine Docker imkun/nome-app-streamlit da Docker Hub. </p>
<pre><code>
docker pull imkun/nome-app-streamlit
</code></pre>
<p> Come ho fatto in precedenza avvio un container Docker in background utilizzando l'immagine specificata e mappando le porte come indicato. </p>
<pre><code>
docker run -d -p 8501:8501 imkun/nome-app-streamlit
</code></pre>


<h2> NOTA </h2> 
<p> Dato che nella streamlit mancano alcune analisi da aggiungere e nel caso decidessi di apportare modifiche, prima di procedere con il deployment, vado a testare le modifiche localmente per assicurarmi che l'applicazione funzioni come previsto. </p>
<p>Ciò lo faccio eseguendo l'applicazione Streamlit localmente </p>
<pre><code>
streamlit run app.py
</code></pre>

<p>Dopo aver confermato che le modifiche funzionano come previsto, vado ad aggiornare l'immagine Docker. </p> 
<p>Questo implica la creazione di una nuova immagine Docker che incorpora le modifiche apportate.</p> 
<p>Utilizzo il Dockerfile per costruire l'immagine, esattamente come ho fatto in precedenza: </p>
<pre><code>
docker build -t username/nome-app-streamlit:latest .
</code></pre>
<p> Una volta creata l'immagine aggiornata, la carico su Docker Hub per renderla accessibile ai nodi Docker Swarm </p>
<pre><code>
docker push username/nome-app-streamlit:latest
</code></pre>
<p>Infine, dico a Docker Swarm di utilizzare l'immagine aggiornata per il servizio che sta eseguendo l’applicazione Streamlit. </p>
<p>Se il servizio è già in esecuzione, posso aggiornarlo per usare la nuova immagine con il comando </p>
<pre><code>
docker service update --image username/nome-app-streamlit:latest nome-del-servizio
</code></pre>

<h2> AVVISO IMPORTANTE</h2>
<p>Se siete interessati a esplorare l'analisi dei dati che ho realizzato, vi invito a visitare il mio sito. A differenza di questo progetto, per l'analisi non ho utilizzato Streamlit. Potete trovare il sito al seguente indirizzo: <a href="https://www.kaggle.com/code/nezarec/eda-yu-gi-oh-cards" target="_blank">Analisi dei dati Yu-Gi-Oh su Kaggle 📊</a></p>

</body>
</html>
