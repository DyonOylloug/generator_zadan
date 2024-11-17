import codecs  # dla kodowania utf-8
import datetime  # do pobierania daty
import os  # do tworzenia katalogów
import random
import sys  # do wysyłania komunikatów w czerwonym kolorze
import textwrap
from pathlib import Path  # do obsługi plików

import babel.dates  # do ładnego generowania daty
import matplotlib.pyplot as plt
import sympy as sp
from tqdm import trange

import generatory

plt.rcParams.update({
    "text.usetex": True,
})

kierunek = 'generuj'  # domyślnie zestaw_sekcje
semestr = ''  # w stylu 'semestr 1'
przedmiot = 'Test_zadania'
kolokwium = ''  # w stylu 'kolokwium 1'
# grupa = 1
data = ''  # w stylu: 01 grudnia 2022 - będzie w nagłówku wydruku
# ile_zestawow = 1  # niepotrzebne
kolor_odpowiedzi = 'blue'


def dodaj_zadanie(plik, zadanie, warstwa):
    polecenie, rozwiazanie = zadanie
    polecenie = '\\tcbitem ' + polecenie + '\n'
    polecenie = textwrap.indent(polecenie, prefix='\t\t')
    rozwiazanie = f'\\zOdpowiedziami{{\\kolorodpowiedzi}}{{ocg{warstwa}}}\n\t{{{rozwiazanie}}}\n\n'
    rozwiazanie = textwrap.indent(rozwiazanie, prefix='\t\t\t')
    plik.write(polecenie + rozwiazanie)
    global nr_warstwy
    nr_warstwy += 1


if not os.path.exists('wygenerowane'):
    os.makedirs('wygenerowane')
    print(" ! Tworzę katalog wygenerowane ", file=sys.stderr)
plik = Path(
    'wygenerowane//' + kierunek + '-' + przedmiot + semestr + kolokwium + '.tex')
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

ile_zadan = 10
nr_warstwy = 0  # do ukrywania odpowiedzi - w każdej funkcji musi być o jeden większy
Fourier_bez_wykresu = True


# def asymptoty(typ: int = 1):
#     x = sp.Symbol('x', real=True)
#     if typ == 1:
#         while True:
#             a, b, c, d, e = [random.choice([-2, -1, 0, 1, 2, 3]) for _ in range(5)]
#             if (a ** 2 + b ** 2 != 0
#                     and d ** 2 != 0
#                     and sp.solve(d * x + e, x)[0] not in sp.solve(a * x ** 2 + b * x + c, x)):
#                 break
#         funkcja = (a * x ** 2 + b * x + c) / (d * x + e)
#         a_2 = sp.limit(funkcja / x, x, sp.oo)
#         b_2 = sp.limit(sp.factor(funkcja - a_2 * x), x, sp.oo)
#         x_0 = sp.solve(d * x + e, x)[0]
#         return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
#                 f'\t\\[\n'
#                 f'\t\tf(x)= {sp.latex(funkcja)}.\n'
#                 f'\t\\]\n',
#                 f'$D_f\\colon \\mathbb{{R}}\\setminus \\left\\{{{sp.latex(x_0)}\\right\\}}.$' + '\\\\' +
#                 f'{"Asymptota pionowa dwustronna w $x_0=" + str(sp.latex(x_0)) + ".$ "}' + '\\\\' +
#                 f'{("Asymptota ukośna w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
#                 f'{("Asymptota pozioma w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}')
#     if typ == 2:
#         while True:
#             a, b, c, d, e = [random.choice([-2, -1, 0, 1, 2, 3]) for _ in range(5)]
#             if (a != 0
#                     and d ** 2 != 0
#                     and sp.solve(d * x + e, x)[0] in sp.solve(a * x ** 2 + b * x + c, x)):
#                 break
#         funkcja = (a * x ** 2 + b * x + c) / (d * x + e)
#         a_2 = sp.limit(funkcja / x, x, sp.oo)
#         b_2 = sp.limit(sp.factor(funkcja - a_2 * x), x, sp.oo)
#         x_0 = sp.solve(d * x + e, x)[0]
#         return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
#                 f'\t\\[\n'
#                 f'\t\tf(x)= {sp.latex(funkcja)}.\n'
#                 f'\t\\]\n',
#                 f'$D_f\\colon \\mathbb{{R}}\\setminus \\left\\{{{sp.latex(x_0)}\\right\\}}.$' + '\\\\' +
#                 f'{("Asymptota ukośna w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
#                 f'{("Asymptota pozioma w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}')
#     if typ == 3:
#         while True:
#             a, b, c, d, e, f = [random.choice([-2, -1, 0, 1, 2, 3]) for _ in range(6)]
#             x_licznik = sp.solve(a * x ** 2 + b * x + c)
#             x_mianownik = sp.solve(d * x ** 2 + e * x + f)
#             # print(x_licznik, x_mianownik)
#             # print(type(x_mianownik[0]), type(x_mianownik[1]))
#             if (a != 0 and d ** 2 != 0
#                     and all(int(i * 6) == i * 6 for i in x_mianownik)
#                     and set(x_mianownik).isdisjoint(set(x_licznik))):
#                 break
#         funkcja = (a * x ** 2 + b * x + c) / (d * x ** 2 + e * x + f)
#         a_2 = sp.limit(funkcja / x, x, sp.oo)
#         b_2 = sp.limit(sp.factor(funkcja - a_2 * x), x, sp.oo)
#         if len(x_mianownik) == 0:
#             return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
#                     f'\t\\[\n'
#                     f'\t\tf(x)= {sp.latex(funkcja)}.\n'
#                     f'\t\\]\n',
#                     f'$D_f\\colon \\mathbb{{R}}.$' + '\\\\' +
#                     f'{("Asymptota ukośna w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
#                     f'{("Asymptota pozioma w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}')
#         if len(x_mianownik) == 1:
#             return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
#                     f'\t\\[\n'
#                     f'\t\tf(x)= {sp.latex(funkcja)}.\n'
#                     f'\t\\]\n',
#                     f'$D_f\\colon \\mathbb{{R}}\\setminus \\left\\{{{sp.latex(x_mianownik[0])}\\right\\}}.$' + '\\\\' +
#                     f'{"Asymptota pionowa dwustronna w $x_0=" + str(sp.latex(x_mianownik[0])) + ".$ "}' + '\\\\' +
#                     f'{("Asymptota ukośna w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
#                     f'{("Asymptota pozioma w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}')
#         if len(x_mianownik) == 2:
#             return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
#                     f'\t\\[\n'
#                     f'\t\tf(x)= {sp.latex(funkcja)}.\n'
#                     f'\t\\]\n',
#                     f'$D_f\\colon \\mathbb{{R}}\\setminus {sp.latex(set(x_mianownik))}.$' + '\\\\' +
#                     f'{"Asymptota pionowa dwustronna w $x_1=" + str(sp.latex(x_mianownik[0])) + ".$ "}' + '\\\\' +
#                     f'{"Asymptota pionowa dwustronna w $x_2=" + str(sp.latex(x_mianownik[1])) + ".$ "}' + '\\\\' +
#                     f'{("Asymptota ukośna w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
#                     f'{("Asymptota pozioma w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}')
#     if typ == 4:
#         while True:
#             a, b, c, d, e, f = [random.choice([-2, -1, 0, 1, 2, 3]) for _ in range(6)]
#             x_mianownik = sp.solve(d * x ** 2 + e * x + f)
#             x_licznik = sp.solve(a * x ** 2 + b * x + c)
#
#             if (a != 0 and d ** 2 != 0
#                     and all(int(i * 6) == i * 6 for i in x_mianownik)
#                     and len(x_mianownik) == 2
#                     and len(x_licznik) == 2
#                     and e != 0
#                     and f != 0
#                     and len(set(x_mianownik).union(set(x_licznik))) == len(x_mianownik) + len(x_licznik) - 1):
#                 break
#         funkcja = (a * x ** 2 + b * x + c) / (d * x ** 2 + e * x + f)
#         a_2 = sp.limit(funkcja / x, x, sp.oo)
#         b_2 = sp.limit(sp.factor(funkcja - a_2 * x), x, sp.oo)
#         return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
#                 f'\t\\[\n'
#                 f'\t\tf(x)= {sp.latex(funkcja)}.\n'
#                 f'\t\\]\n',
#                 f'$D_f\\colon \\mathbb{{R}}\\setminus {sp.latex(set(x_mianownik))}.$' + '\\\\' +
#                 f'{("Asymptota pionowa dwustronna w $x_1=" + str(sp.latex(x_mianownik[0])) + ".$ " + chr(92) + chr(92)) if not sp.limit(funkcja, x, x_mianownik[0]).is_real else ""}' +
#                 f'{("Asymptota pionowa dwustronna w $x_2=" + str(sp.latex(x_mianownik[1])) + ".$ " + chr(92) + chr(92)) if not sp.limit(funkcja, x, x_mianownik[1]).is_real else ""}' +
#                 f'{("Asymptota ukośna w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
#                 f'{("Asymptota pozioma w plus i minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}')
#     if typ == 5:
#         a, b = [random.choice([-2, -1, 1, 2, 3]) for _ in range(2)]
#         c = random.choice([-2, -1, 0, 1, 2, 3])
#         funkcja = a * sp.exp(random.choice([-1, 1]) * x) + b * x + c
#         a_1 = sp.limit(funkcja / x, x, -sp.oo)
#         b_1 = sp.limit(sp.factor(funkcja - a_1 * x), x, -sp.oo) if a_1.is_real else None
#         a_2 = sp.limit(funkcja / x, x, sp.oo)
#         b_2 = sp.limit(sp.factor(funkcja - a_2 * x), x, sp.oo) if a_2.is_real else None
#         return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
#                 f'\t\\[\n'
#                 f'\t\tf(x)= {sp.latex(funkcja)}.\n'
#                 f'\t\\]\n',
#                 f'$D_f\\colon \\mathbb{{R}}.$' + '\\\\' +
#                 f'{("Asymptota ukośna w minus nieskończoności o równaniu $y=" + str(sp.latex(a_1 * x + b_1)) + ".$ ") if a_1.is_real and b_1.is_real and a_1 != 0 else ""}' +
#                 f'{("Asymptota pozioma w minus nieskończoności o równaniu $y=" + str(sp.latex(a_1 * x + b_1)) + ".$ ") if a_1.is_real and b_1.is_real and a_1 == 0 else ""}' +
#                 f'{("Asymptota ukośna w plus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
#                 f'{("Asymptota pozioma w plus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}'
#                 )
#     if typ == 6:
#         a, e = [random.choice([-1, 1, 2]) for _ in range(2)]
#         b, c, d, f = [random.choice([-1, 0, 0, 0, 1, 2]) for _ in range(4)]
#         funkcja = (a * sp.exp(random.choice([-1, 1]) * x) + b * x ** 2 + c * x + d) / (e * x + f)
#         a_1 = sp.limit(funkcja / x, x, -sp.oo)
#         b_1 = sp.limit(sp.factor(funkcja - a_1 * x), x, -sp.oo) if a_1.is_real else None
#         a_2 = sp.limit(funkcja / x, x, sp.oo)
#         b_2 = sp.limit(sp.factor(funkcja - a_2 * x), x, sp.oo) if a_2.is_real else None
#         x_0 = sp.solve(e * x + f)[0]
#         # print(a_1, b_1, a_2, b_2)
#         return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
#                 f'\t\\[\n'
#                 f'\t\tf(x)= {sp.latex(funkcja)}.\n'
#                 f'\t\\]\n',
#                 f'$D_f\\colon \\mathbb{{R}}\\setminus {sp.latex(set(sp.solve(e * x + f)))}.$' + '\\\\' +
#                 f'{("Asymptota pionowa dwustronna w $x_0=" + str(sp.latex(x_0)) + ".$ " + chr(92) + chr(92)) if not sp.limit(funkcja, x, x_0).is_real else ""}' +
#                 f'{("Asymptota ukośna w minus nieskończoności o równaniu $y=" + str(sp.latex(a_1 * x + b_1)) + ".$ ") if a_1.is_real and b_1.is_real and a_1 != 0 else ""}' +
#                 f'{("Asymptota pozioma w minus nieskończoności o równaniu $y=" + str(sp.latex(a_1 * x + b_1)) + ".$ ") if a_1.is_real and b_1.is_real and a_1 == 0 else ""}' +
#                 f'{("Asymptota ukośna w plus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
#                 f'{("Asymptota pozioma w plus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}'
#                 )
#     if typ == 7:
#         a, b, d = [random.choice([-1, 1, 2]) for _ in range(3)]
#         c = random.choice([0, 1, -1])
#         funkcja = a * x + b + c * sp.atan(d * x)
#         a_1 = sp.limit(funkcja / x, x, -sp.oo)
#         b_1 = sp.limit(sp.factor(funkcja - a_1 * x), x, -sp.oo) if a_1.is_real else None
#         a_2 = sp.limit(funkcja / x, x, sp.oo)
#         b_2 = sp.limit(sp.factor(funkcja - a_2 * x), x, sp.oo) if a_2.is_real else None
#         return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
#                 f'\t\\[\n'
#                 f'\t\tf(x)= {sp.latex(funkcja)}.\n'
#                 f'\t\\]\n',
#                 f'$D_f\\colon \\mathbb{{R}}.$' + '\\\\' +
#                 f'{("Asymptota ukośna w minus nieskończoności o równaniu $y=" + str(sp.latex(a_1 * x + b_1)) + ".$ " + chr(92) + chr(92)) if a_1.is_real and b_1.is_real and a_1 != 0 else ""}' +
#                 f'{("Asymptota pozioma w minus nieskończoności o równaniu $y=" + str(sp.latex(a_1 * x + b_1)) + ".$ " + chr(92) + chr(92)) if a_1.is_real and b_1.is_real and a_1 == 0 else ""}' +
#                 f'{("Asymptota ukośna w plus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
#                 f'{("Asymptota pozioma w plus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}'
#                 )
#     if typ == 8:
#         a = random.choice([-1, 1, 2])
#         b = random.choice([0, 1, -1])
#         funkcja = (a * x + b)*sp.exp(random.choice([-1,1])*1/x)
#         a_1 = sp.limit(funkcja / x, x, -sp.oo)
#         b_1 = sp.limit(sp.factor(funkcja - a_1 * x), x, -sp.oo) if a_1.is_real else None
#         a_2 = sp.limit(funkcja / x, x, sp.oo)
#         b_2 = sp.limit(sp.factor(funkcja - a_2 * x), x, sp.oo) if a_2.is_real else None
#         return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
#                 f'\t\\[\n'
#                 f'\t\tf(x)= {sp.latex(funkcja)}.\n'
#                 f'\t\\]\n',
#                 f'$D_f\\colon \\mathbb{{R}} \\setminus {sp.latex({0})}.$' + '\\\\' +
#                 f'{("Asymptota pionowa lewostronna w $x_0=" + str(sp.latex(0)) + ".$ " + chr(92) + chr(92)) if not sp.limit(funkcja, x, 0,"-").is_real else ""}' +
#                 f'{("Asymptota pionowa prawostronna w $x_0=" + str(sp.latex(0)) + ".$ " + chr(92) + chr(92)) if not sp.limit(funkcja, x, 0).is_real else ""}' +
#                 f'{("Asymptota ukośna w plus minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
#                 f'{("Asymptota pozioma w plus minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}'
#                 )
#     if typ == 9:
#         a = random.choice([-1, 1, 2])
#         b = random.choice([0, 1, -1])
#         funkcja = (a * x + b) + random.choice([-1,1]) * sp.exp(random.choice([-1,1])*1/x)
#         a_1 = sp.limit(funkcja / x, x, -sp.oo)
#         b_1 = sp.limit(sp.factor(funkcja - a_1 * x), x, -sp.oo) if a_1.is_real else None
#         a_2 = sp.limit(funkcja / x, x, sp.oo)
#         b_2 = sp.limit(sp.factor(funkcja - a_2 * x), x, sp.oo) if a_2.is_real else None
#         return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
#                 f'\t\\[\n'
#                 f'\t\tf(x)= {sp.latex(funkcja)}.\n'
#                 f'\t\\]\n',
#                 f'$D_f\\colon \\mathbb{{R}} \\setminus {sp.latex({0})}.$' + '\\\\' +
#                 f'{("Asymptota pionowa lewostronna w $x_0=" + str(sp.latex(0)) + ".$ " + chr(92) + chr(92)) if not sp.limit(funkcja, x, 0,"-").is_real else ""}' +
#                 f'{("Asymptota pionowa prawostronna w $x_0=" + str(sp.latex(0)) + ".$ " + chr(92) + chr(92)) if not sp.limit(funkcja, x, 0).is_real else ""}' +
#                 f'{("Asymptota ukośna w plus minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
#                 f'{("Asymptota pozioma w plus minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}'
#                 )
#     if typ == 10:
#         a = random.choice([-1, 1, 2])
#         b = random.choice([0, 1, -1])
#         funkcja = (a * x + b) + random.choice([-1,1]) * sp.ln(x)/x
#         a_2 = sp.limit(funkcja / x, x, sp.oo)
#         b_2 = sp.limit(sp.factor(funkcja - a_2 * x), x, sp.oo) if a_2.is_real else None
#         return (f'Wyznaczyć wszystkie asymptoty funkcji\n'
#                 f'\t\\[\n'
#                 f'\t\tf(x)= {sp.latex(funkcja)}.\n'.replace('log','ln') +
#                 f'\t\\]\n',
#                 f'$D_f\\colon \\left(0, \\infty\\right).$' + '\\\\' +
#                 f'{("Asymptota pionowa prawostronna w $x_0=" + str(sp.latex(0)) + ".$ " + chr(92) + chr(92)) if not sp.limit(funkcja, x, 0).is_real else ""}' +
#                 f'{("Asymptota ukośna w plus minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 != 0 else ""}' +
#                 f'{("Asymptota pozioma w plus minus nieskończoności o równaniu $y=" + str(sp.latex(a_2 * x + b_2)) + ".$ ") if a_2.is_real and b_2.is_real and a_2 == 0 else ""}'
#                 )


plik.write('\t\\subsection{Regresja liniowa}\n')
plik.write(r'    \begin{tcbitemize}[zadanie] ' + '\n')
for _ in trange(ile_zadan, desc='Regresja'):
    dodaj_zadanie(plik, generatory.asymptoty(typ=random.choice(range(1,11))), nr_warstwy)
    # dodaj_zadanie(plik, generatory.pierwiastek_zespolony(stopien=4, nr_zadania=nr_warstwy), nr_warstwy)
    # dodaj_zadanie(plik, generatory.szereg_Fouriera(typ_l=random.randint(0,4), typ_p=random.randint(0,4), nr_zadania=nr_warstwy), nr_warstwy)
# dodaj_zadanie(plik, generatory.styczna_normalna(typ=1), nr_warstwy)
plik.write(r'    \end{tcbitemize}' + '\n')

plik.write(r'\end{document}' + '\n')
plik.close()

# \usepackage{animate}
# \graphicspath{{../pics}}
# \animategraphics[height=6cm,controls=true,autoplay,loop]{1}
# 	{szereg_Fouriera_1}{0}{10}
