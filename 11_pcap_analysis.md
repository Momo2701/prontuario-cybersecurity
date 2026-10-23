3. GUIDA ALL'ADATTAMENTO (COSA MODIFICARE)
​In sede d'esame, procedi modificando i seguenti parametri:
​PCAP_FILE: Inserisci il nome o il percorso esatto del file di cattura fornito nell'archivio della sfida (es. traffic.pcapng).
​SEARCH_KEYWORD: Modifica la stringa di ricerca se la traccia non cerca la stringa standard flag{, ma ad esempio un nome utente, una password o un'estensione di file specifica (es. password, POST, Authorization).
​4. WRITE-UP TEORICO CONCISO & REMEDIATION
​Vulnerabilità & Meccanismo: L'applicazione o il servizio di rete comunica utilizzando protocolli non cifrati (es. HTTP in chiaro), consentendo l'intercettazione passiva del traffico e la lettura dei dati sensibili trasmessi tramite l'analisi dei pacchetti (.pcap).
​Identificazione & Metodo: Attraverso l'ispezione programmatica dei segmenti TCP e dei payload applicativi con la libreria Scapy, è stato possibile identificare il flusso di comunicazione e isolare il pacchetto contenente la stringa ricercata.
​Remediation & Hardening: Forzare l'utilizzo di protocolli di trasporto sicuri basati su crittografia end-to-end (es. HTTPS anziché HTTP, SFTP anziché FTP, SSH anziché Telnet) per impedire l'ascolto passivo (sniffing) sulla rete.
