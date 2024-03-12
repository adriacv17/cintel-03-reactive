import plotly.express as px
from shiny.express import input, ui
from shiny import render
from shinywidgets import render_plotly
import pandas as pd
import seaborn as sns
import palmerpenguins  # This package provides the Palmer Penguins dataset

# Use the built-in function to load the Palmer Penguins dataset
penguins_df = palmerpenguins.load_penguins()

# added title to main page
ui.page_opts(title="Adrian's Penguin Data", fillable=True)

# Use ui.input_selectize() to create a dropdown input to choose a column
with ui.sidebar(open="open"):
    ui.h2("Sidebar")
    ui.input_selectize(
        "selected_attribute",
        "select attribute",
        ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"],
    )

    # Use ui.input_numeric() to create a numeric input for the number of Plotly histogram bins
    ui.input_numeric("plotly_bin_count", "plotly bin count", 40)

    # Use ui.input_slider() to create a slider input for the number of Seaborn bins
    ui.input_slider("seaborn_bin_count", "seaborn bin count", 1, 40, 20)

    # Use ui.input_checkbox_group() to create a checkbox group input to filter the species
    ui.input_checkbox_group(
        "selected_species_list",
        "select species",
        ["Adelie", "Gentoo", "Chinstrap"],
        selected=["Gentoo", "Chinstrap"],
        inline=True,
    )

    # Use ui.hr() to add a horizontal rule to the sidebar
    ui.hr()

    # Use ui.a() to add a hyperlink to the sidebar
    ui.a(
        "Adrian's GitHub Repo",
        href="https://github.com/adriacv17/cintel-02-data/blob/main/app.py",
        target="_blank",
    )

# create a layout to include 2 cards with a data table and data grid
with ui.layout_columns():
    with ui.card(full_screen=True):  # full_screen option to view expanded table/grid
        ui.h2("Penguin Data Table")

        @render.data_frame
        def penguins_datatable():
            return render.DataTable(penguins_df)

    with ui.card(full_screen=True):  # full_screen option to view expanded table/grid
        ui.h2("Penguin Data Grid")

        @render.data_frame
        def penguins_datagrid():
            return render.DataGrid(penguins_df)


# added a horizontal rule
ui.hr()

# create a layout to include 3 cards with different plots
with ui.layout_columns():
    with ui.card(full_screen=True):
        ui.h2("Species Plotly Histogram")

        @render_plotly
        def plotly_histogram():
            return px.histogram(
                penguins_df,
                x=input.selected_attribute(),
                nbins=input.plotly_bin_count(),
                color="species",
            )

    with ui.card(full_screen=True):
        ui.h2("Seaborn Histogram")

        @render.plot(alt="Species Seaborn Histogram")
        def seaborn_histogram():
            seaborn_plot = sns.histplot(
                data=penguins_df,
                x=input.selected_attribute(),
                bins=input.seaborn_bin_count(),
                multiple="dodge",
                hue="species",
            )
            seaborn_plot.set_title("Species Seaborn Histogram")
            seaborn_plot.set_ylabel("Measurement")

    with ui.card(full_screen=True):
        ui.h2("Species Plotly Scatterplot")

        @render_plotly
        def plotly_scatterplot():
            return px.scatter(
                penguins_df,
                title="Plotly Scatterplot",
                x="body_mass_g",
                y="bill_length_mm",
                color="species",
                symbol="species",
            )
