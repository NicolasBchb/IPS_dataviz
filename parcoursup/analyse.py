# %%
import pandas as pd
import dtale
import plotly.express as px

df = pd.read_csv("fr-esr-parcoursup.csv", sep=";")

dtale.show(df)


# %%
cols = {
    "g_ea_lib_vx": "etablissement",
    "dep": "departement",
    "dep_lib": "departement_num",
    "region_etab_aff": "region",
    "acad_mies": "academie",
    "ville_etab": "ville",
    "fili": "formation",
    "form_lib_voe_acc": "filiere",
    "fil_lib_voe_acc": "specialite",
    "contrat_etab": "contrat",
    "g_olocalisation_des_formations": "coordonnees",
    "capa_fin": "capacite",
    "voe_tot": "voeux",
    "voe_tot_f": "voeux_f",
    "nb_voe_pp": "voeux_pp",
    "nb_voe_pp_bg": "voeux_pp_general",
    "nb_voe_pp_bg_brs": "voeux_pp_general_boursiers",
    "nb_voe_pp_bt": "voeux_pp_technologique",
    "nb_voe_pp_bt_brs": "voeux_pp_technologique_boursiers",
    "nb_voe_pp_bp": "voeux_pp_pro",
    "nb_voe_pp_bp_brs": "voeux_pp_pro_boursiers",
    "nb_voe_pp_at": "voeux_pp_autres",
    "acc_tot": "admis",
    "acc_tot_f": "admis_f",
    "acc_brs": "admis_boursiers",
    "acc_neobac": "admis_neobac",
    "acc_bg": "admis_general",
    "acc_bt": "admis_technologique",
    "acc_bp": "admis_pro",
    "acc_at": "admis_autres",
    "acc_mention_nonrenseignee": "admis_mention_nan",
    "acc_sansmention": "admis_sansmention",
    "acc_ab": "admis_ab",
    "acc_b": "admis_b",
    "acc_tb": "admis_tb",
    "acc_tbf": "admis_tbf",
    "acc_term": "admis_term",
    "acc_term_f": "admis_term_f",
    # 'acc_aca_orig':"admis_aca_orig",
    "acc_aca_orig_idf": "admis_aca_orig",
    "taux_adm_psup": "taux_admission",
    "taux_adm_psup_gen": "taux_admission_general",
    "taux_adm_psup_techno": "taux_admission_technologique",
    "taux_adm_psup_pro": "taux_admission_pro",
    "pct_f": "pourcentage_f",
    "pct_aca_orig_idf": "pourcentage_aca_orig",
    "pct_bours": "pourcentage_boursiers",
}

df_clean = df[cols.keys()].rename(columns=cols)

dtale.show(df_clean)

# %%
df_clean["pourcentage_voeux_f"] = (df_clean["voeux_f"] / df_clean["voeux"]) * 100


# %%
colonne = "etablissement"

for formation in df_clean["formation"].unique():

    df_filtre = (
        df_clean.query("formation == @formation")
        .groupby(colonne)
        .mean()
        .reset_index()
    )


    genre = px.bar(
        df_filtre,
        y=colonne,
        x="pourcentage_f",
        # histfunc="avg",
        height=1000,
        color="pourcentage_voeux_f",
        color_continuous_scale=px.colors.diverging.balance_r,
        template="plotly_dark",
        hover_data=[colonne, "pourcentage_f", "pourcentage_voeux_f", "voeux", "admis"],
        range_color=[0, 100],

    )

    genre.update_layout(
        yaxis={"categoryorder": "total ascending"},
    )

    # add a segment at 50%
    genre.add_shape(
        type="line",
        x0=50,
        x1=50,
        y0=0,
        y1=len(df_filtre[colonne].unique()),
        line=dict(
            color="Red",
            width=1,
            dash="dashdot",
        ),
    )


    genre.show()

    genre.write_html(f"genre_{colonne}_{formation}.html")


# %%
variable = "departement"

contrat = px.bar(
    df_clean.groupby(variable).mean().reset_index(),
    y=variable,
    x="pourcentage_f",
    color="pourcentage_voeux_f",
    color_continuous_scale=px.colors.diverging.balance_r,
    template="plotly_dark",
    hover_data=[variable, "pourcentage_f", "pourcentage_voeux_f", "voeux", "admis"],
    range_color=[0, 100],
    height=1000,
)

contrat.add_shape(
    type="line",
    x0=50,
    x1=50,
    y0=0,
    y1=len(df_clean[variable].unique()),
    line=dict(
        color="Red",
        width=1,
        dash="dashdot",
    ),
)

contrat.update_layout(
    yaxis={"categoryorder": "total ascending"},
)

contrat.show()

contrat.write_html(f"genre_{variable}.html")
# %%
