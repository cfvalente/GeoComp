#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Algoritmos para o problema de triangulacao:

Dado um poligono encontra uma triangulacao

Algoritmos disponveis:
- Triangulação de Y Monótono
- Lee e Preparata
- Força Bruta
"""

import plotpolygon
import brute
import leepreparata
import monotone

children = [
	[ 'plotpolygon', 'PlotPolygon', 'Desenha o polígono' ],
	[ 'monotone', 'Monotone', 'Triangulação de Y Monótono' ],
	[ 'leepreparata', 'LeePreparata', 'Lee e Preparata' ],
	[ 'brute', 'Brute', 'Força Bruta' ]
]

__all__ = map (lambda a: a[0], children)
