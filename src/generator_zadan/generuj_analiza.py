# noinspection PyUnresolvedReferences
import codecs  # dla kodowania utf-8
import datetime  # do pobierania daty
import multiprocessing
from inputimeout import inputimeout
import os
# noinspection PyUnresolvedReferences
import random
import sys  # do wysyłania komunikatów w czerwonym kolorze
import textwrap
import time
from pathlib import Path  # do obsługi plików

import babel.dates  # do ładnego generowania daty

import generatory


# Todo: zmienić arg na zadanie: str, licznik: int zamiast art[0] i arg[1]
def zadanie(arg):  # Śmieszne to przekazywanie funkcji jako stringa. eval nie działa wewnątrz pool (zasięg zmiennych)
    start = time.time()
    # print('Początek', arg)
    kolor = (((arg[1] % 13) // 7) * 10 + ((arg[1] % 13) % 7))
    # R, G, B = random.randint(0, 255), random.randint(0, 255), random.randint(0, 255)
    # k = f"38;2;{R};{G};{B}"
    print(
        ' |' * (kolor if kolor < 7 else kolor - 3),
        f'\33[{31 + kolor}m{arg[1]} - Start:  '
        # f'\33[{k}m{arg[1]} - Start:  '
        + f'{arg[0]}'.replace('generatory.', '') + '\033[0m')
    wynik = eval(
        arg[0])  # bez tego eval funkcja się kopiuje a nie uruchamia. I początek i koniec wyświetlają się razem.
    # print(wynik)
    # print('Koniec', arg[0])
    dlugosc_polecenia = len(
        f'zadanie nr {arg[1]} - {arg[0]}'.replace('generatory.', ''))
    # print(dlugosc_polecenia)
    print(
        ' |' * (kolor if kolor < 7 else kolor - 3),
        f'\33[{31 + kolor}m{arg[1]} - Koniec: '
        # f'\33[{k}m{arg[1]} - Koniec: '
        + f'{arg[0]}'.replace('generatory.', '')
        + '-' * (100 - dlugosc_polecenia) + '--' * (12 - (kolor if kolor < 7 else kolor - 3))
        + f': {(time.time() - start):.3f} sekund' + '\033[0m')
    return wynik


def tekst(arg):  # może wystarczy print w pool.map_async? Ale tu można ewentualnie modyfikować wszystkie.
    # print(arg)
    return (arg)


def dodaj_zadanie(plik, zadanie, warstwa):
    polecenie, rozwiazanie = zadanie
    polecenie = '\\tcbitem ' + polecenie + '\n'
    polecenie = textwrap.indent(polecenie, prefix='\t\t')
    rozwiazanie = f'\\zOdpowiedziami{{\\kolorodpowiedzi}}{{ocg{warstwa}}}\n\t{{{rozwiazanie}}}\n\n'
    rozwiazanie = textwrap.indent(rozwiazanie, prefix='\t\t\t')
    plik.write(polecenie + rozwiazanie)


def generuj_analiza(nazwa_pliku: str = 'Analiza',
                    ile_zadan: int = 10,
                    kolor_odpowiedzi: str = 'red',  # 'red' - ukryte, odsłaniane po klinięciu.
                    gotowiec: bool = True,  # True, gdy chcesz przyspieszyć generowanie!!!
                    Fourier_bez_wykresu: bool = False):  # True, gdy chcesz przyspieszyć generowanie do testów!!!
    # poniżej max(100,...) bo dla ile_zadan=1 brakuje miejsca
    # nie może być ile_zadan=1 bo gryzie sie z wpisaywaniem do pliku
    wyniki = list(range(ile_zadan * 50))  # tu jest duży zapas - dopracować - 50 oznacza ile mogłoby być typów zadań
    # print('\33[31m' + f'Używamy {multiprocessing.cpu_count() - 1} wątków' + '\33[0m')
    n = iter(wyniki)
    licznik = 1

    pool = multiprocessing.Pool(nr_of_threads)
    wyniki[next(n)] = pool.map_async(tekst, ['\n\t\\section{Granice}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Granice ciągów}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [('generatory.granica_ciagu(typ=0) ', licznik + i) for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [('generatory.granica_ciagu(typ=1) ', licznik + i) for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [('generatory.granica_ciagu(typ=2) ', licznik + i) for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [('generatory.granica_ciagu(typ=3) ', licznik + i) for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [('generatory.granica_ciagu(typ=4) ', licznik + i) for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Granice funkcji}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [('generatory.granica_funkcji(typ=random.choice([i for i in range(11)])) ',
                                       licznik + i) for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])

    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Asymptoty funkcji}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [('generatory.asymptoty(typ=random.choice(range(1,11))) ', licznik + i) for i in
                                      range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])

    wyniki[next(n)] = pool.map_async(tekst, ['\n\t\\section{Styczna i normalna}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(zadanie, [('generatory.styczna_normalna(typ=1) ', licznik + i) for i in
                                               range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(zadanie, [('generatory.styczna_normalna(typ=2) ', licznik + i) for i in
                                               range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])

    wyniki[next(n)] = pool.map_async(tekst, ['\n\t\\section{Monotoniczność}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [('generatory.monotonicznosc(typ=1) ', licznik + i) for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [(f'generatory.monotonicznosc(typ=2, gotowiec={gotowiec}) ', licznik + i) for i in
                                      range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [(f'generatory.monotonicznosc(typ=3, gotowiec={gotowiec}) ', licznik + i) for i in
                                      range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])

    wyniki[next(n)] = pool.map_async(tekst, ['\n\t\\section{Całka nieoznaczona}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Całkowanie przez części}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(zadanie, [('generatory.calka_nieoznaczona(typ=1) ', licznik + i) for i in
                                               range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])

    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Całkowanie przez podstawianie}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [(f'generatory.calka_nieoznaczona(typ=3, gotowiec={gotowce}) ', licznik + i) for i
                                      in
                                      range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Całkowanie ułamków prostych 1-go rodzaju}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(zadanie, [('generatory.calka_nieoznaczona(typ=4) ', licznik + i) for i in
                                               range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])

    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Całkowanie ułamków prostych 2-go rodzaju}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(zadanie, [('generatory.calka_nieoznaczona(typ=2) ', licznik + i) for i in
                                               range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])

    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Całkowanie funkcji wymiernych}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(zadanie, [('generatory.calka_wymierna(wlasciwy=True) ', licznik + i) for i in
                                               range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(zadanie, [('generatory.calka_wymierna(wlasciwy=False) ', licznik + i) for i in
                                               range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])

    wyniki[next(n)] = pool.map_async(tekst, ['\n\t\\section{Całka oznaczona}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Pole obszaru}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [('generatory.pole_obszaru(typ=1) ', licznik + i) for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [('generatory.pole_obszaru(typ=2) ', licznik + i) for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [(f'generatory.pole_obszaru(typ=3, gotowiec={gotowiec}) ', licznik + i) for i in
                                      range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [(f'generatory.pole_obszaru(typ=4, gotowiec={gotowiec}) ', licznik + i) for i in
                                      range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [('generatory.pole_obszaru(typ=5) ', licznik + i) for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])

    wyniki[next(n)] = pool.map_async(tekst, ['\n\t\\section{Szeregi Fouriera}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Szeregi Fouriera}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [(f'generatory.szereg_Fouriera(typ_l=0, typ_p=0,'
                                       f' bez_wykresu={Fourier_bez_wykresu},'
                                       f' nr_zadania={licznik + i})',
                                       licznik + i) for i in range(0, ile_zadan // 2)])
    licznik += ile_zadan // 2
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [(f'generatory.szereg_Fouriera(typ_l=random.randint(0,1),'
                                       f' typ_p=random.randint(0,1),'
                                       f' bez_wykresu={Fourier_bez_wykresu},'
                                       f' nr_zadania={licznik + i})',
                                       licznik + i) for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [(f'generatory.szereg_Fouriera(typ_l=random.randint(0,4),'
                                       f' typ_p=random.randint(0,4),'
                                       f' bez_wykresu={Fourier_bez_wykresu},'
                                       f' nr_zadania={licznik + i})',
                                       licznik + i) for i in range(0, ile_zadan)])
    licznik += ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])

    wyniki[next(n)] = pool.map_async(tekst, ['\n\t\\section{Funkcje dwóch zmiennych}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Płaszczyzna styczna}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [(f'generatory.plaszczyzna_styczna()',
                                       licznik + i) for i in range(0, ile_zadan)])
    licznik += ile_zadan

    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])

    wyniki[next(n)] = pool.map_async(tekst, ['\t\\subsection{Całki podwójne po obszarze trójkątnym}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [(f'generatory.calka_podwojna(typ=1, nr_zadania={licznik + i})', licznik + i) for i
                                      in
                                      range(0, 2 * ile_zadan)])
    licznik += 2 * ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])

    wyniki[next(n)] = pool.map_async(tekst,
                                     ['\t\\subsection{Całki podwójne po obszarze ograniczonym wykresami krzywych}\n', ])
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\begin{tcbitemize}[zadanie]\n', ])
    wyniki[next(n)] = pool.map_async(zadanie,
                                     [(f'generatory.calka_podwojna(typ=2, nr_zadania={licznik + i})', licznik + i) for i
                                      in
                                      range(0, 2 * ile_zadan)])
    licznik += 2 * ile_zadan
    wyniki[next(n)] = pool.map_async(tekst, ['\t\\end{tcbitemize}\n', ])

    print(f'Zadań wyszło: {licznik - 1}')
    pool.close()
    pool.join()

    if not os.path.exists('wygenerowane'):
        os.makedirs('wygenerowane')
        print(" ! Tworzę katalog wygenerowane ", file=sys.stderr)
    plik = Path(
        'wygenerowane//' + nazwa_pliku + '.tex')
    plik.touch(exist_ok=True)
    plik = codecs.open(plik, "w", "utf8")
    plik.write(('% !TeX spellcheck = pl_PL-Polish\n'
                '\\documentclass[a4paper,10pt]{article}\n'  # można zmieniać rozmiar czcionki
                '\\linespread{1.3} %odstepy miedzy liniami\n'
                '\\usepackage[a4paper, lmargin=2cm, rmargin=2cm, tmargin=2cm, bmargin=2cm]{geometry}\n'
                '\\usepackage{amsfonts}\n'
                '\\usepackage{amsmath}\n'
                '\\usepackage{animate}\n'
                '\\usepackage{color}\n'
                '\\usepackage{enumitem}\n'
                '\\usepackage{fancyhdr}\n'
                '\\usepackage{float}\n'
                '\\usepackage{graphicx}\n'  # do pdf
                '\\usepackage[colorlinks=true,linkcolor=blue]{hyperref}\n'
                '\\usepackage{ifthen}\n'
                '\\usepackage[utf8]{inputenc}\n'
                '\\usepackage{lmodern}\n'
                # '\\def\\pdftexversion{120}'  # eliminacja problemów przy kompilowaniu - niepotrzebne przy pdf-ach
                '\\usepackage{ocgx}\n'
                # '\\usepackage{pgf}\n'  # niepotrzebne gdy importujemy pdf-y
                '\\usepackage{polski}\n\n'
                '\\usepackage{bookmark}\n\n'
                '\\usepackage{tcolorbox}\n'
                '\\tcbuselibrary{most}\n'
                '\\tcbuselibrary{skins}\n'
                '\\tcbuselibrary{raster}\n'
                '% brak - bez odpowiedzi i bez miejsca, white - bez odpowiedzi z miejscem, red = odpowiedzi ukryte ale dostepne\n'
                f'\\newcommand{{\\kolorodpowiedzi}}{{{kolor_odpowiedzi}}}\n\n'
                '\\renewcommand{\\footrulewidth}{0.4pt}% linia pozioma na końcu strony - default is 0pt\n'
                '\\DeclareFontShape{OMX}{cmex}{m}{n}\n'
                '    {<-7.5> cmex7\n'
                '    <7.5-8.5> cmex8\n'
                '    <8.5-9.5> cmex9\n'
                '    <9.5-> cmex10}{}\n'
                '\\DeclareSymbolFont{largesymbols}{OMX}{cmex}{m}{n}\n\n'
                '\n'
                '\\newcommand{\\ukryte}{1}  % domyślnie odpowiedzi są do pokazywania po kliknięciu\n'
                '\\ifthenelse{\\equal{\\kolorodpowiedzi}{red}}  % ukrywamy od pokazywania gdy kolor jest red\n'
                '\t{\\renewcommand{\\ukryte}{0}}{}\n\n'
                '\\newcommand{\\zOdpowiedziami}[3]{\n'
                '\t\\ifthenelse{\\equal{#1}{brak}}{}{\n'
                '\t\t\\ifthenelse{\\equal{#1}{white}}{\\vphantom{#3}}{\\tcbox[rozwiazanie]{\n'
                '\t\t\t\\switchocg{#2}{\\textcolor{\\kolorodpowiedzi}{Rozwiązanie: }}\n'
                '\t\t\t\t\\begin{ocg}{Odp. \\thesubsection.\\thetcbrasternum}{#2}{\\ukryte}\n'  # warstwy nazywane numerem
                '\t\t\t\t\t\\textcolor{\\kolorodpowiedzi}{#3}\n'
                '\t\t\t\t\\end{ocg}}}}}\n\n'
                '\\tcbset{\n'
                '\tzadanie/.style={size=small,\n'
                '\t\traster columns=1,\n'
                '\t\tcolframe=green!50!black,\n'
                '\t\tcolback=green!2!white,\n'
                '\t\tcolbacktitle=green!40!black,\n'
                '\ttitle={Zadanie \\thesubsection.\\thetcbrasternum}}\n}\n'
                '\\tcbset{\n'
                '\trozwiazanie/.style={size=small, capture=minipage}\n}\n'
                '\\graphicspath{{../pics}}\n'

                '\\begin{document}\n'
                '    \\author{\\tcbox[colframe=blue!50!black,colback=blue!2!white,colbacktitle=blue!40!black]\n'
                '        {\\Large Adam Bohonos \\thanks{\href{https://github.com/DyonOylloug/generator_zadan}{GitHub}}}}\n'
                '    \\title{\\tcbox[colframe=green!50!black,colback=green!2!white,colbacktitle=green!40!black]\n'
                '        {\\Huge Analiza - zadania uzupełniające}}\n'
                '    \\date{\\tcbox[colframe=green!50!black,colback=green!2!white,colbacktitle=green!40!black]\n'
                '        {\\small ' +
                babel.dates.format_datetime(datetime.datetime.now(), "d MMMM yyyy", locale='pl_PL') + '}}\n'
                                                                                                      '    \\maketitle\n'
                                                                                                      '    \\pagestyle{fancy}\n'
                                                                                                      '    \\setlength{\\headheight}{27.29453pt}\n'
                                                                                                      '    \\fancyfoot[R]{\\tiny\\textbf{ ' +
                babel.dates.format_datetime(datetime.datetime.now(), "d MMMM yyyy, HH:mm", locale='pl_PL') + '}}\n' +
                # '    \\hspace{1cm}' + '\n\n'
                '    \\tableofcontents'
                ))

    warstwa = 0
    for i in range(len(wyniki)):  # wynik to lista stringów i krotek
        try:
            # print(len(wyniki[i].get()))
            if len(wyniki[i].get()) == 1:
                plik.write(wyniki[i].get()[0])
            else:
                for k in wyniki[i].get():
                    dodaj_zadanie(plik, k, warstwa)
                    warstwa += 1
        except Exception:
            pass

    plik.write('\n\\end{document}')
    plik.close()

    puste = 0  # to do szacowania rozmiaru listy wyników
    for i in range(len(wyniki)):  # wynik to lista stringów i krotek
        try:
            wyniki[i].get()
        except Exception:
            puste += 1
    print('Puste miejsca w wynikach: ', puste)
    print("--- %s seconds ---" % (time.time() - start_time))


if __name__ == '__main__':  # średni czas generowania z dnia 30.01.2024:  139.43769199848174
    try:

        # Take timed input using inputimeout() function
        nr_of_threads = int(inputimeout(prompt=f'\33[32m' + f'Procesor jest {multiprocessing.cpu_count()} wątkowy'
                                                            f' - Ile użyć wątków?\n'
                                                            f'Masz 10 sekund na decyzję.\n'
                                                            f'Domyslnie będzie {max(multiprocessing.cpu_count() // 2, 1)}.\n'
                                               + '\33[0m', timeout=10))
        if not 1 <= nr_of_threads <= multiprocessing.cpu_count():
            nr_of_threads = max(multiprocessing.cpu_count() // 2, 1)
            print('(Domyślnie) ', end='')

    # Catch the timeout error
    except Exception:

        # Declare the timeout statement
        nr_of_threads = max(multiprocessing.cpu_count() // 2, 1)
        print('(Domyślnie) ', end='')

    # Print the statement on timeoutprint(time_over)

    print('Użyjemy:', nr_of_threads)

    czas = list()
    ile_petli = 1  # to tylko do testowania średniego czasu generowania
    gotowce = True

    for i in range(1, ile_petli + 1):
        print('Rozpoczynam pętlę nr: ', i)
        start_time = time.time()
        generuj_analiza(nazwa_pliku='Analiza',
                        ile_zadan=20,  # nie może byc ile_zadan=1, bo gryzie zie z wpisywaniem tekstu i zadań do pliku
                        kolor_odpowiedzi='red',
                        Fourier_bez_wykresu=True,  # True, gdy chcesz przyspieszyć generowanie - np. do testów!!!
                        gotowiec=gotowce)
        czas.append(time.time() - start_time)
    print(czas)
    print('Średni czas generowania: ', sum(czas) / len(czas))
