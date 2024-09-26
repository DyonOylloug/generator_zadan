from importlib.metadata import version
__version__ = version("generator_zadan")

from .zespolone import rownanie_liniowe
from .zespolone import rownanie_kwadratowe
from .zespolone import pierwiastek_zespolony
from .zespolone import rownanie_ze_sprzezeniem
from .zespolone import obszar_zespolony
from .uklady_rownan_liniowych import uklad_rownan_nieoznaczony
from .uklady_rownan_liniowych import uklad_Cramera
from .macierze import wyznacznik_parametr
from .macierze import macierz_odwrotna_parametr  #strasznie wolne - 14s na jeden 3x3, ale było też 85s!!!
from .macierze import rownanie_macierzowe
from .macierze import wartosci_wlasne
from .macierze import diagonalizacja_macierzy
from .macierze import rzad_macierzy
from .macierze import diagonalizacja_macierzy_z_wielokrotnym_wartosciami_wlasnymi
from .geometria_analityczna import rownanie_prostej
from .geometria_analityczna import rownanie_plaszczyzny
from .geometria_analityczna import odleglosc_prostych_skosnych
from .geometria_analityczna import punkt_symetryczny_do_plaszczyzny
from .geometria_analityczna import punkt_symetryczny_do_prostej
from .geometria_analityczna import katy_w_trojkacie
from .geometria_analityczna import pole_trojkata
from .geometria_analityczna import plaszczyzna_styczna
from .granice import granica_ciagu
from .granice import granica_funkcji
from .monotonicznosc import monotonicznosc
from .monotonicznosc import styczna_normalna
from .calki_nieoznaczone import calka_nieoznaczona
from .calki_nieoznaczone import calka_wymierna
from .calki_oznaczone import pole_obszaru
from .szeregi_Fouriera import szereg_Fouriera
from .calki_podwojne import calka_podwojna
from .generuj_zestaw import generuj_LaTeX
from .generuj_zestaw import dodaj_zadanie
