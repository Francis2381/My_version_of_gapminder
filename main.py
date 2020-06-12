# Pandas for data management
import pandas as pd
from os.path import dirname, join
from bokeh.io import curdoc

# Importing the function that was created in the plot.py
from scripts.plot import modify_doc

# Reading the data in using pandas
df1 = pd.read_csv(join(dirname(__file__), 'data/cool.csv'), index_col=0).dropna()

# Creating the plot
plot = modify_doc(df1)

#Adding the plot to the current bokeh document and adding a webpage title
curdoc().add_root(plot)
curdoc().title = 'World Data'