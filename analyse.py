# %%
import json
import pandas as pd
import dtale
from tqdm import tqdm
import plotly.express as px
import plotly.graph_objects as go


# %%
df = pd.read_csv("fr-en-ips_ecoles.csv", sep=";")

dtale.show(df)

# %%
df_public = df[df["Secteur"] == "public"].groupby("Nom de la commune").mean().reset_index()
df_prive = df[df["Secteur"] == "privé sous contrat"].groupby("Nom de la commune").mean().reset_index()

fig = go.Figure()
fig.add_trace(go.Histogram(y=df_public['IPS'].to_list(), x=df_public['Nom de la commune'].to_list(), name="Public", histfunc="avg"))
fig.add_trace(go.Histogram(y=df_prive['IPS'].to_list(), x=df_prive['Nom de la commune'].to_list(), name="Privé", histfunc="avg"))

fig.update_layout(title_text='IPS par Nom de la commune', template="plotly_dark")

# sort bars
fig.update_layout(barmode='group', xaxis={'categoryorder':'total descending'})

fig.show()

fig.write_html("histogram.html")

# %%
df_paris = df[df["Nom de la commune"].str.contains('PARIS')]
df_paris = df_paris[df_paris["Nom de la commune"].str.contains('ARRONDISSEMENT')]

df_paris_public = df_paris[df_paris["Secteur"] == "public"].groupby("Nom de la commune").mean().reset_index()
df_paris_prive = df_paris[df_paris["Secteur"] == "privé sous contrat"].groupby("Nom de la commune").mean().reset_index()

paris  = go.Figure()
paris.add_trace(go.Histogram(y=df_paris_public['IPS'].to_list(), x=df_paris_public['Nom de la commune'].to_list(), name="Public", histfunc="avg"))
paris.add_trace(go.Histogram(y=df_paris_prive['IPS'].to_list(), x=df_paris_prive['Nom de la commune'].to_list(), name="Privé", histfunc="avg"))

paris.update_layout(title_text='IPS par arrondissement de Paris', template="plotly_dark", barmode='group', xaxis={'categoryorder':'total descending'})

paris.show()

paris.write_html("paris.html")

# %%
camembert = px.pie(df, names='Secteur', title='Répartition des écoles par secteur', template="plotly_dark")

camembert.show()

camembert.write_html("camembert.html")

# %%
with open('departements.geojson') as f:
    dept = json.load(f)

df["departement"] = df['Code du département'].map(lambda x: x[1:] if x.startswith('0') else x)

fig = px.choropleth_mapbox(df.groupby("departement").mean().reset_index(),
                           geojson=dept, locations='departement', color='IPS',
                           color_continuous_scale="jet",
                           range_color=(85, 125),
                           mapbox_style="carto-positron",
                           featureidkey="properties.code",
                           zoom=3, center = {"lat": 47.081012, "lon": 2.398782},
                           opacity=0.5,
                           labels={'unemp':'unemployment rate'}
                          )

fig.update_layout(margin={"r":0,"t":0,"l":0,"b":0})

fig.show()


# %%
