#!/usr/bin/env python
# -*- coding: utf-8 -*-

from geocomp.common.polygon import *

def PlotPolygon(p):
	polygon = Polygon(p)
	polygon.plot ('white')
