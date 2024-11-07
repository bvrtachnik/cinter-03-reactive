import plotly.express as px
from shiny.express import input, ui, render
from shinywidgets import render_plotly
from palmerpenguins import load_penguins
from shinywidgets import output_widget, render_widget, render_plotly
import seaborn as sns
from shiny import render
import palmerpenguins
from shiny import reactive


penguins_df = load_penguins()

# Set the Page Options with the title "Brett's Penguin Data"
ui.page_opts(title="Brett's Penguin Data", fillable=True)

# Sidebar for User Interaction
with ui.sidebar(open="open"):
        ui.h2("Sidebar")
        ui.input_selectize(
            "selected_attribute",
            "Select Attributes",
            ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
            )
        ui.input_numeric(
            "plotly_bin_count",
            "Plotly Number of Bins",
            10,
            min=1,
            max=20,
            )
        ui.input_slider(
            "seaborn_bin_count",
            "Seaborn Number of Bins",
            min= 5,
            max= 50,
            value= 25
            )
        ui.input_checkbox_group(
            "selected_species_list",
            "Choose Species",
            ["Adelie","Gentoo","Chinstrap"],
            selected=["Adelie","Gentoo","Chinstrap"],
            inline=False
            )
        ui.hr()
        ui.a(
            "Brett's GitHub",
            href="https://github.com/bvrtachnik/cintel-02-data/tree/main",
            target="_blank"
            )

with ui.layout_columns():

    # Data Table Using Filtered Data    
    with ui.card():
        "Penguins Data Table"
        @render.data_frame
        def data_table():
            return render.DataTable(filtered_data())

    # Data Grid Using Filtered Data    
    with ui.card():
        "Penguins Data Grid"
        @render.data_frame
        def data_grid():
            return render.DataGrid(filtered_data())

with ui.layout_columns():
    
    # Plotly Histogram    
    with ui.card():
        ui.card_header("Plotly Histogram")
        @render_plotly
        def plotlyhistogram():
            return px.histogram(
                filtered_data(),
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
                color="species"
            ).update_layout(
                xaxis_title="Bill length (mm)",
                yaxis_title="Counts"
            )
            
    # Seaborn Histogram    
    with ui.card():
        ui.card_header("Seaborn Histogram")
       
        @render.plot
        def plot2():
            ax=sns.histplot(
                data=filtered_data(), 
                x=input.selected_attribute(), 
                bins=input.seaborn_bin_count(),
               )
            ax.set_title("Palmer Penguins")
            ax.set_xlabel(input.selected_attribute())
            ax.set_ylabel("Number")
            return ax
           
    # Plotly Scatterplot
    with ui.card(full_screen=True):
        ui.card_header("Plotly Scatterplot: Species")
        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                filtered_data(),
                x="body_mass_g",
                y="bill_depth_mm",
                color="species",
                labels={"body_mass_g": "Body Mass (g)",
                "bill_depth_mm": "Bill Depth (mm)"}
                )

# --------------------------------------------------------
# Reactive calculations and effects
# --------------------------------------------------------

# Add a reactive calculation to filter the data
# By decorating the function with @reactive, we can use the function to filter the data
# The function will be called whenever an input functions used to generate that output changes.
# Any output that depends on the reactive function (e.g., filtered_data()) will be updated when the data changes.


@reactive.calc
def filtered_data():
    selected_species = input.selected_species_list()
    if selected_species:
        return penguins_df[penguins_df['species'].isin(selected_species)]
    return penguins_df
