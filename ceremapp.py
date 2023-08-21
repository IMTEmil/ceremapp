import streamlit as st
import plotly.express as px
import pandas as pd
import plotly.graph_objects as go
import copy
import numpy as np

csv_separator = ";"

css = """
<style>
div {
    color: #292574;
}
</style>
"""

title_css = """
<style>
.custom-title {
    color: #ef7757;
    font-size: 24px;
    font-weight: bold;
    margin-bottom: 20px;
}
</style>
"""

class Csvfile:
    def __init__(self, uploaded_file) :

        self.uploadedfile = uploaded_file

        self.df = pd.read_csv(uploaded_file, sep = csv_separator)

        self.step = self.df["step"].iloc[0]
        self.xmin = self.df["xmin"].iloc[0]
        self.ymin = self.df["ymin"].iloc[0]
        
        self.df.drop(['step', 'xmin', 'ymin'], axis = "columns", inplace = True)

        self.name = uploaded_file.name[:-4]

        self.set_graphs()

    def get_maxv(self) -> float:
        return self.df.values.max()

    def get_minv(self) -> float:
        return self.df.values.min()
    
    def get_x_coordinates(self) :
        return [self.xmin + i * self.step for i in range(self.df.shape[1])]
    
    def get_y_coordinates(self) :
        return [self.ymin + i * self.step for i in range(self.df.shape[0])]
    
    def get_filename(self) -> str :
        return self.name
    
    def get_graph_y(self) :
         return self.graph_y  
      
    def get_graph_x(self) :
         return self.graph_x
    
    def set_graphs(self) :
        self.graph_y = [self.df.iloc[:, i] for i in range(self.df.shape[0])]
        self.graph_x = [self.df.iloc[i] for i in range(self.df.shape[0])]

    def get_inv(self) :
        inv_csv = copy.copy(self)

        inv_csv.df = inv_csv.df * -1

        inv_csv.set_graphs()

        return inv_csv


def display_graph(csvfile : Csvfile, axis):

    if axis == 1 : caxis = "x"
    else : caxis = "y"

    type_affichage = st.radio("Afficher :", ("Toutes les courbes selon l'axe " + caxis, "Vue par profil selon l'axe " + caxis))

    checkbox_inv = st.checkbox("Inverser les courbes selon l'axe " + caxis, value = False)

    if checkbox_inv == True : csvfile__ = csvfile.get_inv()
    else : csvfile__ = csvfile

    if type_affichage == "Vue par profil selon l'axe " + caxis :

        slider_x = st.slider("Profil à afficher", min_value = 1, max_value = csvfile__.df.shape[axis - 1], value = 1)

        if axis == 1 :
            figure_x = px.line(x = csvfile__.get_x_coordinates(), y = csvfile__.df.iloc[slider_x - 1])
        else : 
            figure_x = px.line(x = csvfile__.get_y_coordinates(), y = csvfile__.df.iloc[:, slider_x - 1])

        figure_x = go.Figure(figure_x, layout_yaxis_range = [csvfile__.get_minv(), csvfile__.get_maxv()])

        figure_x.update_layout(title = "Vue par profils selon l'axe " + caxis)

    else :

        if axis == 1 :
            figure_x = px.line(x = csvfile__.get_x_coordinates(), y = csvfile__.get_graph_x())
        else :
            figure_x = px.line(x = csvfile__.get_y_coordinates(), y = csvfile__.get_graph_y())

        figure_x = go.Figure(figure_x, layout_yaxis_range = [csvfile__.get_minv(), csvfile__.get_maxv()])

        figure_x.update_layout(title = "Tous les profils selon l'axe " + caxis)

        figure_x.update_traces(line=dict(color="grey", width = 0.5))
        
    figure_x.update_layout(autosize = True,
                           showlegend = False, 
                           yaxis_title = csvfile.get_filename(), 
                           margin = dict(l=20, r=20, t=40, b=20), 
                           height = 600,
                           title_font = dict(size=20))

    st.plotly_chart(figure_x, use_container_width=True) 


def display3D_figure(csvfile : Csvfile):
    
    x = np.array(csvfile.get_x_coordinates())
    
    y = np.array(csvfile.get_y_coordinates())

    X, Y = np.meshgrid(x, y)

    Z = csvfile.df.to_numpy()

    fig = go.Figure(data=[go.Surface(z = Z, x = x, y = y, colorscale="Plasma")])

    fig.update_layout(title = 'Vue 3D de ' + csvfile.name, height = 1000, margin = dict(l=300, r=300, t=40, b=20))
    st.plotly_chart(fig, autosize = True, use_container_width = True)    
        

st.set_page_config(page_title = "CEREM-APP", page_icon = "https://raw.githubusercontent.com/IMTEmil/ceremapp/main/cerema_icon2.ico", layout = "wide")

st.image("https://raw.githubusercontent.com/IMTEmil/ceremapp/main/LogosRF%2BCerema_horizontal.png", output_format="PNG", width=500)

st.markdown(css, unsafe_allow_html=True)

with open( "style.css" ) as css:
    st.markdown( f'<style>{css.read()}</style>' , unsafe_allow_html= True)

st.markdown("<p style='color: #ef7757; text-align: center;font-size: 50px; font-weight: bold;margin-bottom: 20px;'>Bienvenue sur l'outil de visualisation de MELBA</h1>", unsafe_allow_html=True)

file = st.file_uploader("Veuillez charger le fichier CSV à visualiser ci-dessous.", type = ["csv"], accept_multiple_files=False)

if file:

    csvfile = Csvfile(file)

    display_graph(csvfile, 1)

    display_graph(csvfile, 2)

    display3D_figure(csvfile)
