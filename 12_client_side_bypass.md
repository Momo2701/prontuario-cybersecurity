Modulo 12: Client-Side Controls & JavaScript Inspection (Client-Side Bypass)
​Parole chiave e indizi espliciti nella traccia:
​Riferimenti a pulsanti disabilitati (disabled), campi nascosti del modulo (<input type="hidden">), restrizioni di accesso gestite da script di validazione eseguiti direttamente nel browser.
​Anomalie strutturali o nel codice sorgente:
​Controlli di sicurezza o restrizioni di ruolo delegati interamente alla logica JavaScript lato client, senza alcuna validazione speculare o verifica di autorizzazione eseguita dal server.
​Motivo logico di applicazione:
​Si applica quando l'interfaccia grafica blocca un'azione o un inserimento tramite vincoli del browser, permettendo di bypassare la grafica e inviare direttamente i parametri desiderati al server tramite richieste HTTP personalizzate.

​3. GUIDA ALL'ADATTAMENTO (COSA MODIFICARE)
​In sede d'esame, procedi modificando i seguenti parametri:
​TARGET_URL: Inserisci l'URL dell'azione del form (attributo action del tag <form> nell'HTML).
​FORM_DATA: Modifica le chiavi e i valori inserendo i nomi dei campi nascosti (<input type="hidden" name="...">) o modificando i permessi (es. trasformando is_admin=0 in is_admin=1).
​4. WRITE-UP TEORICO CONCISO & REMEDIATION
​Vulnerabilità & Meccanismo: L'applicazione riponeva la propria sicurezza su controlli di validazione e restrizioni implementati esclusivamente lato client (tramite JavaScript o attributi HTML come disabled/hidden). Ciò ha permesso di aggirare i controlli interfaccia e inviare parametri arbitrari direttamente al server.
​Identificazione & Metodo: Mediante l'ispezione del codice sorgente HTML/JS della pagina sono stati individuati i campi nascosti e le logiche di restrizione, replicati e manipolati programmaticamente tramite lo script Python 12_client_side_bypass.py.
​Remediation & Hardening: Implementare rigorosamente la validazione lato server (Server-Side Validation) per qualsiasi input o parametro ricevuto, trattando ogni dato proveniente dal client come potenzialmente manipolato o malevolo.
