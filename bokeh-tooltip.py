# -*- coding: utf-8 -*-
"""
Created on Mon Mar 19 17:35:18 2018

@author: U6033615
"""

from collections import OrderedDict
from bokeh.plotting import figure
from bokeh.models import ColumnDataSource, HoverTool, Circle


fig = figure(
    title='DDS Help Tree',
    tools= 'box_zoom,box_select,reset' # Note no hover
)
names = ["Gavin Gray", "Ewan Klein", "Francisco Vargas", "S3", "S1", "S2", "S4"]
info = ["TA", "Lectuer", "TA", "Student", "Student", "Student", "Student"]

fig.line(x=[1,3,5],y=[1,2,1])
fig.line(x=[0,1,2],y=[0,1,0])
fig.line(x=[4,5,6],y=[0,1,0])

source = ColumnDataSource(
    data=dict(
        xname=[1, 3, 5,6,0,2,4],
        yname=[1, 2, 1,0,0,0,0],
        name = names,
        info = info
    )
)
fig.annulus(x='xname', y='yname', inner_radius=0.29, outer_radius=0.295,source=source)

circle = Circle(x='xname', y='yname', radius=0.29, fill_color='#e9f1f8')
circle_renderer = fig.add_glyph(source, circle)

x1, y1 = (-0.1, -0.04)
fig.text(x=[-0.1, x1 + 2, x1 + 4, x1+6] , y=[y1, y1, y1 , y1] , text=["S1", "S2", "S3", "S4"])
fig.text(x=[x1 + 0.9, x1 + 5] , y=[y1 +1 , y1 +1] , text=["GG", "FV"])
fig.text(x=[x1 + 3] , y=[y1 +2] , text=["EK"])

tooltips = OrderedDict([
    ('name', '@name'),
    ('info', '@info'),
])
fig.add_tools( HoverTool(tooltips=tooltips, renderers=[circle_renderer]))
show(fig)