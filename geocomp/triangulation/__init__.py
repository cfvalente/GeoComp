#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Algoritmos para o problema de triangulacao:

Dado um poligono encontra uma triangulacao

Algoritmos disponveis:
- Força Bruta -- Remoção de orelhas
- Triangulação de Y Monótono
- Lee e Preparata

"""

import plotpolygon
import brute
import leepreparata
import monotone

children = [
	[ 'plotpolygon', 'PlotPolygon', 'Desenha o polígono' ],
	[ 'brute', 'Brute', 'Remoção de orelhas' ],
	[ 'monotone', 'Monotone', 'Triangulação de Y Monótono' ],
	[ 'leepreparata', 'LeePreparata', 'Lee e Preparata' ]

]

__all__ = map (lambda a: a[0], children)
