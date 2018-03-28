# -*- coding: utf-8 -*-
"""
https://dev.socrata.com/blog/2014/11/04/data-visualization-with-python.html
"""
import numpy as np
import pandas as pd
import datetime
import urllib
 
from bokeh.plotting import ColumnDataSource, figure, output_file
from bokeh.models import HoverTool, Circle
from collections import OrderedDict

###########################################
# Query/Read data source in JSON format
###########################################
query = ("https://data.lacity.org/resource/mgue-vbsx.json?"
    "$group=date"
    "&call_type_code=507P"
    "&$select=date_trunc_ymd(dispatch_date)%20AS%20date%2C%20count(*)"
    "&$order=date")
#Notice that the key in the JSON dict has to be "date", and format has to match definition of a date timestamp.
# Otherwise, pandas won't recognize it, and parseing will be wrong.
raw_data = pd.read_json(query)
assert( "date" in raw_data.columns )

# Augment the data frame with the day of the week and the start of the week that it's in.
# This will make more sense soon...
raw_data['day_of_week'] = [date.dayofweek for date in raw_data["date"]]
raw_data['week'] = [(date - datetime.timedelta(days=date.dayofweek)).strftime("%Y-%m-%d") for date in raw_data["date"]]
 
# Pivot our data to get the matrix we need
data = raw_data.pivot(index='week', columns='day_of_week', values='count')
data = data.fillna(value=0)
 
# Get our "weeks" and "days"
weeks = list(data.index)
days = ["Mon", "Tues", "Wed", "Thurs", "Fri", "Sat", "Sun"]

# Set up the data for plotting. We will need to have values for every
# pair of year/month names. Map the rate to a color.
max_count = raw_data["count"].max()
day_of_week, week, color, parties = [], [], [], []

##################################
# Core plotting logic! Arrays.
##################################
for w in weeks:
    for idx, day in enumerate(days):
        day_of_week.append(day)
        week.append(w)
        count = data.loc[w][idx]
        parties.append(count)
        color.append("#%02x%02x%02x" % (255, np.int64(255 - (count / max_count) * 255.0), np.int64(255 - (count / max_count) * 255.0)))

# For convinience of plotting. Not necessary. 
source = ColumnDataSource(
    data=dict(
        day_of_week=day_of_week,
        week=week,
        color=color,
        parties=parties,
    )
)    

# Configure the region of plot
output_file('all-las-parties.html')
TOOLS = 'box_zoom,box_select,reset,hover'
fig=figure( title='\"Party\" Disturbance Calls in LA', x_range=weeks, y_range=list(reversed(days)), tools=TOOLS)
fig.plot_width, fig.plot_height=900, 400
fig.toolbar_location='right'

# For tooltips [TODO]
#fig.annulus(x='day_of_week', y='week', inner_radius=0.29, outer_radius=0.295,source=source)
#circle = Circle(x='day_of_week', y='week', radius=0.29, fill_color='#e9f1f8')
#circle_renderer = fig.add_glyph(source, circle)    

###############################
# Main ploting function!
###############################
fig.rect(raw_data["week"], raw_data["day_of_week"], width=1, height=1,color=color, line_color=None)

fig.grid.grid_line_color = None
fig.axis.axis_line_color = None
fig.axis.major_tick_line_color = None
fig.axis.major_label_text_font_size = "8pt"
fig.axis.major_label_standoff = 0
fig.xaxis.major_label_orientation = np.pi/3

#hover = fig.select(dict(type=HoverTool))
#hover.tooltips = OrderedDict([
#    ('parties', '@parties'),
#])

tooltips = OrderedDict([
    ('parties', '@parties'),
])
#fig.add_tools( HoverTool(tooltips=tooltips, renderers=[circle_renderer]))
    
show(fig) # show the plot
