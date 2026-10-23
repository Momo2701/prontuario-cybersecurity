# 📖 Scheda Operativa: 06_sql_injection_bypass

## 1. QUANDO IDENTIFICARE QUESTA VULNERABILITÀ (30 Secondi)
* **Scenario:** Form di autenticazione (`/login`) o endpoint di ricerca che interagisce con un database relazionale (SQL).
* **Criterio:** Il backend costruisce la query SQL tramite concatenazione diretta di stringhe senza sanificazione o parametrizzazione.
* **Input Noto:** Form HTTP POST/GET con campi di input come `username` e `password`.

---

## 2. PARAMETRI E LOGICA DEI PAYLOAD
* **Target Form Fields:** Identificare gli attributi `name="..."` del form HTML (es. `username`, `password`).
* **Pattern Tautologici Classici:**
  * `' OR 1=1 --` (SQLite / PostgreSQL / MS SQL)
  * `' OR '1'='1` (Generico)
  * `admin' --` (Bypass immediato se l'utente principale è noto)
  * `' OR 1=1 #` (MySQL)

---

## 3. WRITE-UP TEORICO MODELLO (Da personalizzare)

### 1. Vulnerabilità e Modello Teorico

La vulnerabilità di **SQL Injection (SQLi) Authentication Bypass** si verifica quando un'applicazione web costruisce query SQL dinamiche concatenando direttamente l'input fornito dall'utente, senza preventiva sanitizzazione o parametrizzazione.

#### Meccanismo del Difetto Architetturale
Nelle applicazioni vulnerabili, la query di autenticazione assume una struttura simile alla seguente:

$$Q(u, p) = \text{"SELECT * FROM users WHERE username = '" } \mathbin{\Vert} u \mathbin{\Vert} \text{"' AND password = '" } \mathbin{\Vert} p \mathbin{\Vert} \text{"'"}$$

dove $u$ e $p$ rappresentano le stringhe inviate nei campi `username` e `password`.

Il difetto risiede nel mancato isolamento tra la sintassi dell'istruzione SQL (codice) e i dati forniti dall'utente (dati):

1. **Alterazione dell'Albero Sintattico:** L'introduzione di caratteri di controllo come il singolo apice (`'`) interrompe la costante letterale all'interno della clausola `WHERE`.
2. **Iniezione di Tautologie Booleane:** Inserendo un operatore logico `OR` seguito da una condizione sempre vera (es. `1=1` o `'a'='a'`), la valutazione logica dell'intera clausola `WHERE` restituisce incondizionatamente `TRUE`.
3. **Truncation del Flusso di Esecuzione:** L'uso di metacaratteri di commento specifici per il DBMS in uso (`--` per SQLite/PostgreSQL/SQL Server, `#` o `-- ` per MySQL) impone al parser del database di ignorare la restante porzione della query, annullando di fatto il controllo sulla password.

Di conseguenza, la query finale eseguita dal motore di database diventa:

```sql
SELECT * FROM users WHERE username = '' OR 1=1 --' AND password = '...'
```

Poiché la condizione `username = '' OR 1=1` valuta a vero per ogni record della tabella, il database restituisce la prima riga presente (tipicamente l'account amministrativo o principale), consentendo l'accesso senza conoscere la credenziale segreta.

---

### 2. Metodologia di Analisi e Testing

1. **Identificazione dei Punti di Inserimento:** Mappatura dei parametri HTTP (GET/POST) associati ai campi del modulo di login (es. `username`, `password`).
2. **Generazione dei Candidate Payload:** Selezione di pattern sintattici volti a testare le differenti modalità di delimitazione delle stringhe e dei commenti accettati dai principali DBMS (`'`, `"`, `--`, `#`).
3. **Valutazione della Risposta HTTP:** Invio delle richieste e analisi del codice di stato (HTTP 200/302) e del contenuto HTML (presenza di stringhe di benvenuto o token di sessione).

---

### 3. Remediation e Hardening

* **Query Parametrizzate (Prepared Statements):** Adottare tassativamente istruzioni pre-compilate in cui la struttura SQL è separata dai dati dell'utente:
  ```python
  cursor.execute(
      "SELECT id, username FROM users WHERE username = ? AND password = ?",
      (user_input, pass_input)
  )
  ```
* **Object-Relational Mapping (ORM):** Utilizzare framework ORM ben consolidati (es. SQLAlchemy, Django ORM) che gestiscono nativamente la parametrizzazione delle query.
* **Principio del Minimo Privilegio:** Limitare i permessi dell'account database utilizzato dall'applicazione web alle sole operazioni strettamente necessarie (`SELECT`, `INSERT`), inibendo permessi amministrativi DDL (`DROP`, `ALTER`).