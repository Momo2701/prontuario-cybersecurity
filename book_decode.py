#!/usr/bin/env python3
"""
PRONTUARIO #09: Paragraph-Line-Word Book Cipher Solver
------------------------------------------------------
Modulo: Crittografia / Cifrari a Libro (Paragraph, Line, Word)
Descrizione: Estrazione automatizzata di parole basata su coordinate a tre livelli:
            (Numero Paragrafo, Numero Riga nel Paragrafo, Numero Parola nella Riga).
"""

# ==================== INPUT DATI D'ESAME ====================
TEXT_FILE = "book.txt"

# Coordinate nel formato: (Paragrafo, Riga, Parola) - indicizzate da 1
BOOK_COORDINATES = [
    (1, 9, 4), 
    (4, 2, 8), 
    (4, 8, 3), 
    (7, 1, 5), 
    (8, 10, 1)
]
# ============================================================

def parse_paragraphs(filename: str):
    """Divide il file di testo in paragrafi basandosi sulle righe vuote."""
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Dividiamo il testo in blocchi separati da linee vuote (paragrafi)
    raw_paragraphs = content.split('\n\n')
    paragraphs = []
    
    for p in raw_paragraphs:
        # Per ogni paragrafo, filtriamo le righe effettive escludendo le stringhe vuote
        lines = [line.strip() for line in p.split('\n') if line.strip()]
        if lines:
            paragraphs.append(lines)
            
    return paragraphs

def solve_paragraph_book_cipher(filename: str, coords: list):
    try:
        paragraphs = parse_paragraphs(filename)
        print(f"[*] File caricato con successo. Trovati {len(paragraphs)} paragrafi.\n")
        
        extracted_words = []
        for idx, (p_idx, l_idx, w_idx) in enumerate(coords, 1):
            # Conversione indici da 1 (umani) a 0 (Python)
            paragraph = paragraphs[p_idx - 1]
            line = paragraph[l_idx - 1]
            words = line.split()
            word = words[w_idx - 1]
            
            extracted_words.append(word)
            print(f"[*] Punto {idx} -> Paragrafo {p_idx}, Riga {l_idx}, Parola {w_idx}: '{word}'")
            
        flag_sentence = " ".join(extracted_words)
        print("\n=== BOOK CIPHER (PARAGRAPH) RISOLTO! ===")
        print(f" Risultato Finale: {flag_sentence}")
        print("=========================================\n")
        
    except IndexError as e:
        print(f"[!] Errore di indice: Una coordinata (Paragrafo/Riga/Parola) non esiste nel testo. Dettagli: {e}")
    except FileNotFoundError:
        print(f"[!] Errore: Il file '{filename}' non è stato trovato nella directory.")

if __name__ == "__main__":
    solve_paragraph_book_cipher(TEXT_FILE, BOOK_COORDINATES)