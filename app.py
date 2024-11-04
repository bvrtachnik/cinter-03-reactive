import plotly.express as px
from shiny.express import input, ui, render
from shinywidgets import render_plotly
from palmerpenguins import load_penguins
from shinywidgets import output_widget, render_widget, render_plotly
import seaborn as sns
from shiny import render
import palmerpenguins


penguins_df = load_penguins()

ui.page_opts(title="Brett's Penguin Data", fillable=True)

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
    with ui.card():
        "Penguins Data Table"
        @render.data_frame
        def penguinstables_df():
            return render.DataTable(penguins_df, filters=False,selection_mode="row")

    with ui.card():
        "Penguins Data Grid"
        @render.data_frame
        def penguintables_df():
            return render.DataGrid(penguins_df,filters=False,selection_mode="row")

with ui.layout_columns():
    
    # Plotly Histogram
    with ui.card():
        ui.card_header("Plotly Histogram")
        @render_plotly
        def plotlyhistogram():
            return px.histogram(
                penguins_df,
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
                data=penguins_df, 
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
                penguins_df,
                x="body_mass_g",
                y="bill_depth_mm",
                color="species",
                labels={"body_mass_g": "Body Mass (g)",
                "bill_depth_mm": "Bill Depth (mm)"}
                )
