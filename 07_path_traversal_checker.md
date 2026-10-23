# SCHEDA OPERATIVA #07: Path Traversal Tester & Validator

### 1. Identificazione Rapida (Quando usarlo in sede d'esame)
* **Contesto:** La sfida presenta un'applicazione web con un endpoint HTTP GET che gestisce file o risorse tramite parametri espliciti nella query string (es. `?file=document.pdf`, `?page=about.html`, `?doc=view`).
* **Obiettivo:** Verificare la presenza di vulnerabilità di tipo **Path Traversal / Arbitrary File Read** ed eseguire il bypass di filtri di sanificazione deboli (es. filtri basati su rimozione singola non ricorsiva o assenza di encoding).

### 2. Parametri da Modificare in Sede d'Esame
Prima di eseguire lo script nel terminale, verifica e modifica unicamente le seguenti righe nella sezione `INPUT DATI D'ESAME`:
1. **`TARGET_URL`**: Sostituisci l'URL di esempio con quello fornito dalla traccia d'esame (es. `http://<IP_TARGET>/download`).
2. **`PARAM_NAME`**: Modifica il nome del parametro stringa intercettato nell'URL (es. se la richiesta originale è `/view?page=home`, imposta `PARAM_NAME = "page"`).
3. **`TRAVERSAL_PAYLOADS`**: Personalizza o estendi la lista dei payload se il sistema implementa filtri specifici (es. aggiungendo codifiche URL multiple o sequenze di escape alternative).

### 3. Guida Sintattica essenziale ("Zero Python")
* **`requests.get(url, params=dizionario)`**: Invia una richiesta HTTP di tipo GET al server web accodando automaticamente i parametri specificati nel dizionario all'URL sotto forma di query string (es. `?file=../../../../etc/passwd`).
* **`response.status_code`**: Restituisce il codice numerico della risposta HTTP (es. `200` per successo, `404` per risorsa non trovata).
* **`response.text`**: Estrae il contenuto testuale o HTML restituito dal server, utilizzato nello script per ricercare la presenza di firme di sistema (`root:x:`) o del formato della flag (`flag{...}`).

### 4. Schema di Write-Up Associato
In sede di stesura del Write-up d'esame, utilizza questa struttura sintetica basata sull'esecuzione dello script:
* **1. Vulnerabilità e Meccanismo:** 
  L'applicazione non effettua una corretta validazione e canonicalizzazione dei percorsi passati in input, consentendo l'utilizzo di sequenze di escape (`../`) per uscire dalla directory radice autorizzata e leggere file arbitrari del sistema operativo. Eventuali filtri basati su sostituzioni non ricorsive (single-pass) vengono aggirati tramite payload di padding (`....//`).
* **2. Metodologia d'Attacco & Script:** 
  Utilizzo dello script automatizzato `07_path_traversal_checker.py` per testare iterativamente una serie di payload di Path Traversal e bypass di codifica sull'endpoint target tramite richieste HTTP GET.
* **3. Risultato:** 
  Individuazione del payload vincente ed estrazione corretta del file di sistema o della stringa della flag dal corpo della risposta HTTP del server.
