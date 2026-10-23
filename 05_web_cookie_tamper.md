# 📖 Scheda Operativa: 05_web_cookie_tamper

## 1. QUANDO USARE QUESTO SCRIPT (30 Secondi)
* **Scenario:** Challenge di Web Security in cui l'autenticazione o il ruolo dell'utente (`role`, `is_admin`, `user`) sono memorizzati direttamente in un cookie lato client.
* **Criterio:** Il cookie non impiega firme crittografiche (HMAC, JWT) né un Session ID opaco gestito lato server; utilizza testo in chiaro o semplice encoding (Base64, URL-encoding).
* **Input Noto:** Il cookie assegnato dal server (es. `dXNlcj1ndWVzdDtyb2xlPWd1ZXN0`) e la struttura dei parametri d'autorizzazione.

---

## 2. VARIABILI DA MODIFICARE IN SEDE D'ESAME
1. `ORIGINAL_COOKIE = "..."`: Incolla il cookie ricevuto dal server via DevTools o risposta HTTP.
2. `RAW_PAYLOAD = "user=admin;role=admin"`: Modificare la stringa impostando i parametri con i privilegi elevati richiesti.
3. `USE_BASE64 = True`: Impostare su `True` se il cookie è codificato in Base64, oppure `False` se in chiaro.

---

## 3. WRITE-UP TEORICO MODELLO (Da personalizzare)

### 1. Vulnerabilità e Modello Teorico
L'applicazione web è affetta da una vulnerabilità di **Broken Access Control** dovuta ad una gestione insicura dello stato lato client (*Insecure Client-Side State Management*).

La falla si articola su tre livelli:
1. **Trust Boundary Violation:** Il server delega il controllo dell'autorizzazione al client, fidandosi ciecamente dei parametri d'accesso (`role=guest`) inviati nel cookie HTTP senza validazione lato backend.
2. **Assenza di Integrità e Firma Crittografica:** Il cookie non include un Message Authentication Code (HMAC) o una firma digitale che consenta al server di rilevare alterazioni non autorizzate dei dati.
3. **Equivoco tra Encoding e Cifratura:** L'impiego della codifica Base64 offre esclusivamente una rappresentazione alfanumerica dei dati, priva di qualsiasi garanzia di riservatezza o inalterabilità.

Questa debolezza permette un attacco di **Privilege Escalation Verticale**, consentendo a un utente non privilegiato di forgiarsi credenziali amministrative e scavalcare i controlli d'accesso.

### 2. Approccio e Payload/Script
Per la risoluzione è stato utilizzato lo script di prontuario `05_web_cookie_tamper.py`.

Procedura operativa applicata:
1. Intercettato ed analizzato il cookie di sessione originale (es. `auth_token = dXNlcj1ndWVzdDtyb2xlPWd1ZXN0`).
2. Decodificata la stringa Base64 identificando la struttura interna dello stato: `user=guest;role=guest`.
3. Alterata la struttura dati sostituendo i valori con le credenziali amministrative target: `user=admin;role=admin`.
4. Ricodificata la stringa alterata in formato Base64 ottenendo il token forgiato (`dXNlcj1hZG1pbjtyb2xlPWFkbWlu`) ed inviata la richiesta HTTP con l'header `Cookie:` aggiornato.

### 3. Remediation / Hardening
Per mettere in sicurezza la gestione delle sessioni e dell'autorizzazione:
- **Server-Side Session Management:** Spostare interamente lo stato dell'utente lato server (es. database o memoria volatile Redis). Il client deve conservare unicamente un Session ID opaco, generato tramite un generatore casuale crittograficamente sicuro (CSPRNG).
- **Cryptographic State Integrity:** Se si necessita di uno stato *stateless* lato client, adottare standard sicuri come i JSON Web Token (JWT) o cookie firmati tramite HMAC con chiave segreta ad alta entropia custodita esclusivamente sul server.
- **Cookie Security Flags:** Impostare i flag di sicurezza `HttpOnly` (per prevenire accessi via JavaScript/XSS), `Secure` (per forzare il transito su cifratura TLS/HTTPS) e `SameSite=Strict` (per prevenire attacchi CSRF).
