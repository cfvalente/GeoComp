"""Algoritmos para o problema de triangulacao:

Dado um poligono encontra uma triangulacao

Algoritmos disponveis:
- Triangulacao de Y Monotono
- Lee e Preparata
- Forca Bruta
"""
import brute
import leepreparata
import monotone

children = [
	[ 'monotone', 'Monotone', 'Triangulacao de Y Monotono' ],
	[ 'leepreparata', 'LeePreparata', 'Lee e Preparata' ],
	[ 'brute', 'Brute', 'Forca Bruta' ]
]

__all__ = map (lambda a: a[0], children)
