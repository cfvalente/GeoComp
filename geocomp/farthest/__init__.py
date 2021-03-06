#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""Algoritmos para o problema do Par Mais Distante:

Dado um conjunto de pontos S, determinar dois cuja distancia entre eles 
maxima

Algoritmos disponveis:
- Fora bruta
- Diametro
"""
import diameter
import brute

children = [
	[ 'diameter', 'Diameter', 'Diametro' ],
	[ 'brute', 'Brute', 'Forca Bruta' ]
]

__all__ = map (lambda a: a[0], children)
