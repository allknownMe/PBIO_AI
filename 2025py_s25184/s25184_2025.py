# s25184_2025.py
# Cel programu: Generowanie losowej sekwencji DNA zapisanej w formacie FASTA, wraz z analizą zawartości nukleotydów.
# Kontekst: Program do zastosowania edukacyjnego w bioinformatyce – poznanie formatu FASTA i analizy sekwencji DNA.

import random

# Funkcja generująca losową sekwencję DNA
def generate_dna_sequence(length, uppercase=True):
    nucleotides = ['A', 'C', 'G', 'T'] if uppercase else ['a', 'c', 'g', 't']
    return ''.join(random.choices(nucleotides, k=length))

# Funkcja obliczająca statystyki sekwencji (działa tylko dla dużych liter)
def calculate_stats(sequence):
    upper_seq = sequence.upper()
    total = len(upper_seq)
    stats = {nuc: upper_seq.count(nuc) / total * 100 for nuc in 'ACGT'}
    cg_content = (stats['C'] + stats['G'])
    at_content = (stats['A'] + stats['T'])
    cg_at_ratio = cg_content / at_content if at_content != 0 else 0
    return stats, cg_content, cg_at_ratio

# Funkcja dzieląca sekwencję na linie po 60 znaków
def wrap_sequence(sequence, width=60):
    return '\n'.join(sequence[i:i+width] for i in range(0, len(sequence), width))

# MODIFIED (pętla while pozwala na wielokrotne generowanie sekwencji bez restartu):
while True:
    # Pobieranie danych od użytkownika
    try:
        length = int(input("Podaj długość sekwencji: "))
        if length <= 0:
            print("Długość musi być liczbą dodatnią!")
            continue
    except ValueError:
        print("Niepoprawna wartość. Podaj liczbę całkowitą.")
        continue

    seq_id = input("Podaj ID sekwencji: ")
    description = input("Podaj opis sekwencji: ")
    name = input("Podaj imię: ")

    # MODIFIED (zapytanie czy sekwencja ma być wielkimi czy małymi literami)
    letter_case = input("Czy chcesz zapisać sekwencję wielkimi literami? (T/N): ").strip().upper()
    use_upper = True if letter_case == 'T' else False

    # GENEROWANIE SEKWENCJI
    sequence = generate_dna_sequence(length, uppercase=use_upper)
    insert_position = random.randint(0, len(sequence))
    sequence_with_name = sequence[:insert_position] + name + sequence[insert_position:]

    # ZAPIS DO PLIKU
    filename = f"{seq_id}.fasta"
    try:
        with open(filename, 'w') as f:
            f.write(f">{seq_id} {description}\n")
            # ORIGINAL:
            # f.write(sequence_with_name + "\n")
            # MODIFIED (wstawienie podziału na linie po 60 znaków – zgodnie z FASTA):
            f.write(wrap_sequence(sequence_with_name) + "\n")
    except IOError as e:
        print(f"Błąd zapisu pliku: {e}")
        continue

    # STATYSTYKI (bez imienia i bez zmiany wielkości liter)
    stats, cg_content, cg_at_ratio = calculate_stats(sequence)

    # WYŚWIETLENIE WYNIKÓW
    print(f"Sekwencja została zapisana do pliku {filename}")
    print("Statystyki sekwencji:")
    for nuc in 'ACGT':
        print(f"{nuc}: {stats[nuc]:.1f}%")
    print(f"%CG: {cg_content:.1f}")
    print(f"Stosunek CG/AT: {cg_at_ratio:.2f}")

    # MODIFIED (kontrola pętli – możliwość zakończenia działania programu):
    again = input("Czy chcesz wygenerować kolejną sekwencję? (T/N): ").strip().upper()
    if again != 'T':
        print("Zakończono działanie programu.")
        break
