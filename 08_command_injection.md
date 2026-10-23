# 📖 Scheda Operativa: 08_command_injection_tester

## 1. QUANDO IDENTIFICARE QUESTA VULNERABILITÀ (30 Secondi)
* **Scenario:** Endpoint web che accetta parametri destinati all'esecuzione di comandi di sistema (es. utility di rete `/ping?host=...`, strumenti di conversione o manipolazione file).
* **Criterio:** Il backend concatena l'input dell'utente direttamente in una stringa di comando invocata tramite shell di sistema (es. `os.system()`, `os.popen()`, `subprocess.Popen(..., shell=True)`).
* **Input Noto:** Parametri HTTP GET/POST destinati a interagire con la linea di comando del server.

---

## 2. MECCANICA DELLA VULNERABILITÀ
* **Metacaratteri della Shell:** L'uso di separatori e operatori di controllo della shell (come `;`, `|`, `&`, o newlines `%0a`) interrompe il comando originale e consente l'esecuzione sequenziale o condizionale di comandi arbitrari.
* **Mancato Isolamento Codice/Dati:** Poiché l'input viene elaborato direttamente dall'interprete della shell (`/bin/sh` o `bash`), i metacaratteri non vengono trattati come semplici dati ma come istruzioni di controllo.

---

## 3. WRITE-UP TEORICO MODELLO (Da personalizzare)

### 1. Vulnerabilità e Modello Teorico

La vulnerabilità di **OS Command Injection** (o *Shell Injection*) si verifica quando un'applicazione web concatena dati forniti dall'utente all'interno di una stringa invocata da un interprete di comandi di sistema, senza sanificazione né isolamento sintattico.

#### Meccanismo del Difetto Architetturale
Nelle applicazioni vulnerabili, l'esecuzione del comando di sistema avviene tipicamente tramite una relazione di concatenazione:

$$C_{\text{eseguito}} = \text{"ping -c 1 "} \mathbin{\Vert} \text{input\_utente}$$

Il difetto risiede nel mancato isolamento tra la struttura del comando e i dati dell'utente (*Code/Data Mixing*):

1. **Interpretazione dei Metacaratteri:** Quando la stringa viene passata alla shell (es. `/bin/sh -c`), i metacaratteri di controllo (es. `;`, `|`, `&`, `%0a`) vengono interpretati come delimitatori di istruzione anziché come caratteri letterali.
2. **Esecuzione Arbitraria di Comandi (RCE):** L'inserimento di un separatore consente di concatenare comandi secondari arbitrari, eseguiti con i medesimi privilegi del processo dell'applicazione web.

---

### 2. Metodologia di Analisi

1. **Mappatura dei Punti di Ingresso:** Identificazione dei parametri HTTP destinati a interagire con funzionalità del sistema operativo.
2. **Analisi della Risposta HTTP:** Valutazione dell'output restituito dall'applicazione web per confermare l'esecuzione dei comandi di sistema nel backend.

---

### 3. Remediation e Hardening

* **Eliminazione dell'Interprete di Shell (`shell=False`):** Invocare i comandi di sistema tramite chiamate dirette all'eseguibile, passando i parametri sotto forma di lista distinta e disabilitando la shell:
  ```python
  import subprocess

  # Esecuzione sicura senza invocazione della shell (/bin/sh)
  result = subprocess.run(
      ["ping", "-c", "1", user_input],
      capture_output=True,
      text=True,
      shell=False
  )
  ```
* **Validazione tramite Allowlist:** Verificare che l'input dell'utente rispetti un formato rigoroso (es. espressioni regolari per soli indirizzi IP o stringhe alfanumeriche) prima dell'elaborazione.
* **Principio del Minimo Privilegio:** Eseguire il servizio web con un account di sistema a privilegi estremamente ridotti per limitare l'impatto in caso di compromissione.