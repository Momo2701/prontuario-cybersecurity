#!/usr/bin/env python3
"""
PRONTUARIO #11: PCAP Traffic Analysis & Flag Extractor
-------------------------------------------------------
Modulo: Network Security / Traffic Analysis
Descrizione: Estrazione di flussi di traffico in chiaro e ricerca di flag
            o credenziali all'interno di file di cattura .pcap tramite Scapy.
"""

from scapy.all import rdpcap, TCP, Raw

# ==================== INPUT DATI D'ESAME ====================
PCAP_FILE = "capture.pcap"  # Percorso del file pcap fornito dalla traccia
SEARCH_KEYWORD = "flag{"    # Pattern o stringa da cercare nel payload
# ============================================================


def main():
    print(f"[*] Lettura del file di cattura: {PCAP_FILE}")
    try:
        packets = rdpcap(PCAP_FILE)
        print(f"[*] Totale pacchetti letti: {len(packets)}\n")
        
        found = False
        for i, pkt in enumerate(packets):
            # Verifica se il pacchetto contiene un layer TCP con payload applicativo (Raw)
            if pkt.haslayer(TCP) and pkt.haslayer(Raw):
                payload = pkt[Raw].load
                try:
                    decoded_payload = payload.decode('utf-8', errors='ignore')
                    # Cerca la keyword o la flag nel payload del pacchetto
                    if SEARCH_KEYWORD in decoded_payload:
                        print(f"[+] Trovato match nel pacchetto #{i}:")
                        print(f"    Payload: {decoded_payload.strip()}\n")
                        found = True
                except Exception:
                    pass
                    
        if not found:
            print("[-] Nessun match trovato con la keyword specificata.")
            
    except Exception as e:
        print(f"[!] Errore durante l'analisi del file pcap: {e}")


if __name__ == "__main__":
    main()
