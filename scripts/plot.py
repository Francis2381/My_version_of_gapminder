import pandas as pd
import numpy as np

from bokeh.io import curdoc

from bokeh.plotting import figure

from bokeh.models import HoverTool, ColumnDataSource
from bokeh.models.widgets import CheckboxGroup, Slider, Button

from bokeh.layouts import column, row


def modify_doc(df1):
    
    #Creating Column Data Source
    def make_dataset(df1):
        return ColumnDataSource(df1)
    
    # A function to style the plot
    def style(p):
        # Title 
        p.title.align = 'center'
        p.title.text_font_size = '20pt'

        # Axis titles
        p.xaxis.axis_label_text_font_size = '15pt'
        p.xaxis.axis_label_text_font_style = 'bold'
        p.yaxis.axis_label_text_font_size = '15pt'
        p.yaxis.axis_label_text_font_style = 'bold'

        # Tick labels
        p.xaxis.major_label_text_font_size = '12pt'
        p.yaxis.major_label_text_font_size = '12pt'

        return p

    # A function to create the plot
    def make_plot(src):
        # Blank plot with correct labels
        p = figure(plot_width = 1000, plot_height = 600, title = 'Life Expectancy vs Birth Rate',
                  x_axis_label = 'Birth Rate', y_axis_label = 'Life Expectancy')
        
        value = list(df1['region'].unique())
        
        p.circle('birth_rate', 'life_expect', source=src, fill_alpha=0.7, size='population_scaled',
                hover_fill_color = 'purple', hover_fill_alpha = 0.7, color='color', legend = 'region')

        # Adding a hover tool to the plot
        hover = HoverTool(tooltips=[('Country', '@country'),
                                   ('Income Range', '@income'),
                                   ('Population', '@population_str'),
                                   ('GDP/cap', '@gdp_percap')], point_policy='follow_mouse')
        p.add_tools(hover)
        
        p.legend.click_policy = 'hide'

        # Styling
        p = style(p)

        return p
  
    # Callback function
    def update(attr, old, new):
        # the list of active as in ticked regions in the selecction panel
        region_to_plot = [region_selection.labels[i] for i in 
                            region_selection.active]
        # Subsetting and selecting the right values based on selection
        df = df1.set_index(['region'])
        df = df.loc[region_to_plot]
        df = df[df['year']== year_lider.value]
        # Make a new dataset based on the selected regions, using the 'make_dataset' function defined earlier
        new_src = make_dataset(df)
        # Update the source data
        src.data.update(new_src.data)
        
    def animate_update():
        year = year_lider.value + 1
        if year > 2015:
            year = 1990
        year_lider.value = year

    # Animate function to animate the plot using the slider
    def animate():
        global callback_id
        if button.label == 'Static':
            button.label = 'Animate'
            callback_id = curdoc().add_periodic_callback(animate_update, 200)
        else:
            button.label = 'Static'
            curdoc().remove_periodic_callback(callback_id)
            
            
    callback_id = None
    
    button = Button(label='Static', width=60)
    button.on_click(animate)
    
    value = list(df1['region'].value_counts().index)
    
    region_selection = CheckboxGroup(labels=value, active = [0, 1])
    region_selection.on_change('active', update)
    
    year_lider = Slider(start = 1990, end = 2015, 
                         step = 1, value = 1990,
                         title = 'Year of Plot')
    year_lider.on_change('value', update)
    
    # Creating data for the initial plot to be displayed
    initial = [region_selection.labels[i] for i in region_selection.active]
    df = df1.set_index(['region'])
    df = df.loc[initial]
    df = df[df['year']== year_lider.value]
    src = make_dataset(df)
    
    # Organising the layout of the plot
    controls = row(region_selection, year_lider, button)    
    
    p = make_plot(src)
    layout = column([controls, p])
    
    return layout
    