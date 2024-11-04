import plotly.express as px
import plotly.graph_objects as go
from shiny.express import input, ui, output, render
from shinywidgets import render_plotly
import palmerpenguins
import seaborn as sns
import matplotlib.pyplot as plt


# Familiarize myself with the data

# Column names
# - species: penguin species
# - island: island name
# - bill_length_mm: length of the bill in millimeters
# - bill_depth_mm: depth of the bill in millimeters
# - flipper_length_mm: length of the flipper in millimeters
# - body_mass_g: body mass in grams
# - sex: MALE or FEMALE

# Load data in with built in function
penguins_df = palmerpenguins.load_penguins()

with ui.layout_columns():
    # Create Data Table
    with ui.card():
        "Penguins Data Table"
        @render.data_frame
        def penguinstable_df():
                return render.DataTable(penguins_df, filters=False,selection_mode='row')

    # Create Data Grid
    with ui.card():
        "Penguins Data Grid"
        @render.data_frame
        def penguinsgrid_df():
            return render.DataGrid(penguins_df, filters=False, selection_mode="row")


#-----------------------
# Define User Interface
#------------------------   

with ui.sidebar(open="open"): 
        
        # Add 2nd level header to sidebar
        ui.h2("Sidebar")
    
        # Create input selectize to create a dropdown input to choose a column
        ui.input_selectize(
            'selected_attribute',
            'Select an attribute',
            ["bill_length_mm", "bill_depth_mm", "flipper_length_mm", "body_mass_g"])

        # Create input numeric for a numeric input for Plotly bins
        ui.input_numeric(
            "plotly_bin_count",
            'Plotly Bin Count',
            20)

        # Create input slider input for number of seaborn bins
        ui.input_slider(
            "seaborn_bin_count",
            "Seaborn Bin Count",
            1, 20, 10)

        # Create checkbox group input to filter the species
        ui.input_checkbox_group(
            "selected_species_list",
            "Filter by Species",
            ["Adelie", "Gentoo", "Chinstrap"],
            selected= ["Adelie", "Gentoo", "Chinstrap"],
            inline= False)
       
        # Add a horizontal rule to the sidebar
        ui.hr()

        # Add a hyperlink to the sidebar
        ui.a(
            "GitHub",
            href= "https://github.com/ClaytonSeabaughGH/cintel-02-data",
            target= "_blank")


#----------------------------------------
# Create Main layout for displaying plots
#----------------------------------------

    
ui.page_opts(title="Clayton's Penguin Data", fillable=True)

# Create interactive plotly plot
with ui.layout_columns():
    @render_plotly
    def plotly_plot():
        filtered_df = penguins_df[
                penguins_df["species"].isin(input.selected_species_list())]
        selected_attribute = input.selected_attribute()
        bin_count = input.plotly_bin_count()
        fig = px.histogram(
            filtered_df,
            x=selected_attribute,
            nbins=bin_count,
            title="Plotly Histogram",
            color="species", 
        )
        fig.update_traces(marker_line_color="black", marker_line_width=2)
        return fig
        
# Create interactive seaborn plot
with ui.layout_columns():
    with ui.card():
        @render.plot(alt="Seaborn Histogram")
        def seaborn_plot():
            filtered_df = penguins_df[
                penguins_df["species"].isin(input.selected_species_list())]
            selected_attribute = input.selected_attribute()
            ax=sns.histplot(data=filtered_df,x=selected_attribute,bins=input.seaborn_bin_count(),hue="species", multiple="stack")
            ax.set_title("Seaborn Histogram")
            ax.set_xlabel(selected_attribute)
            ax.set_ylabel("Count")
            return ax

# Create plotly scatter plot
with ui.card(full_screen=True):
    ui.card_header("Plotly Scatterplot: Species")
    @render_plotly
    def plotly_scatterplot():
        filtered_df = penguins_df[
                penguins_df["species"].isin(input.selected_species_list())]
        fig = px.scatter(
                filtered_df,
                x="body_mass_g",
                y="flipper_length_mm",
                color="species",
                title="Penguins Scatterplot: Body Mass vs. Flipper Length",
                labels={
                    "body_mass_g": "Body Mass (g)",
                    "flipper_length_mm": "Flipper Length (mm)",},)
        return fig

# Create a violin plot showing distribution of mass
with ui.card(full_screen=True):
    ui.card_header("Plotly Violinplot: Species")
    @render_plotly
    def line_plot():
        selected_attribute = input.selected_attribute()
        fig = px.violin(
            penguins_df,
            y=selected_attribute,
            x="species",
            box=True,                
            points="all",           
            title="Attriubte Distribution by Species",
            color="species")
        return fig
