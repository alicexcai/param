from random import random

from bokeh.layouts import column
from bokeh.models import Button
from bokeh.plotting import figure, curdoc

# create a plot and style its properties
p = figure()
# add a text renderer to our plot (no data yet)
r = p.text(x=[0, 100], y=[0, 100], text=['start', 'end'])
# store a link to the plot data
ds = r.data_source

# create a callback that will add a number in a random location


def callback():
    new_data = {}
    new_data['x'] = ds.data['x'] + [random()*70 + 15]
    new_data['y'] = ds.data['y'] + [random()*70 + 15]
    new_data['text'] = ds.data['text'] + [f"{random():.2f}"]
    ds.data = new_data
    
def upload_data():
    file_upload
    ds.data = new_data


# add a button widget and configure with the call back
button = Button(label="Press Me")
upload_button = Button(label="Upload data")
button.on_click(callback)
upload_button.on_click(upload_data)

# put the button and plot in a layout and add to the document
curdoc().add_root(column(button, p))
