from pathlib import Path
import pandas as pd
import plotly.express as px
import streamlit as st

# 1. Configuration de la page (Doit être la toute première commande Streamlit)
st.set_page_config(
    page_title="App Club Sportif - Vue 360",
    page_icon="🏆",
    layout="wide",
    initial_sidebar_state="expanded",
)

# 2. Chargement et préparation des données
DATA_PATH = Path(__file__).parent / "adhesions_club.csv"


@st.cache_data
def load_data():
    df = pd.read_csv(DATA_PATH)
    df["Date_Inscription"] = pd.to_datetime(df["Date_Inscription"])
    df["Mois_Inscription"] = (
        df["Date_Inscription"].dt.to_period("M").astype(str)
    )
    return df


df = load_data()

# 3. Barre latérale : Le centre de contrôle
with st.sidebar:
    st.image("https://cdn-icons-png.flaticon.com/512/1256/1256650.png", width=80)
    st.title("⚙️ Centre de tri")
    st.markdown("---")

    villes_selection = st.multiselect(
        "📍 Villes", options=df["Ville"].unique(), default=df["Ville"].unique()
    )
    sections_selection = st.multiselect(
        "🏅 Sections",
        options=df["Section"].unique(),
        default=df["Section"].unique(),
    )
    statut_selection = st.multiselect(
        "💳 Statut Paiement",
        options=df["Statut"].unique(),
        default=df["Statut"].unique(),
    )

    st.markdown("---")
    st.info(
        "💡 **Astuce :** Modifiez ces filtres pour mettre à jour tous les"
        " graphiques instantanément."
    )

# Filtrage dynamique
df_filtered = df[
    (df["Ville"].isin(villes_selection))
    & (df["Section"].isin(sections_selection))
    & (df["Statut"].isin(statut_selection))
]

# 4. En-tête principal
st.title("🏆 Tableau de Bord Interactif - Saison 2026")
st.markdown("*Vision globale et temps réel de la santé de l'association.*")

# 5. Les Onglets de navigation
tab1, tab2, tab3 = st.tabs(
    ["📈 Vue Globale", "💸 Suivi Financier", "📇 Base de Données & Exports"]
)

# --- ONGLET 1 : VUE GLOBALE ---
with tab1:
    col1, col2, col3, col4 = st.columns(4)
    total_adherents = len(df_filtered)
    nouvelles_inscriptions = len(
        df_filtered[df_filtered["Date_Inscription"] >= "2026-08-01"]
    )

    col1.metric("👥 Total Adhérents", total_adherents)
    col2.metric(
        "🚀 Inscriptions (depuis Août)",
        nouvelles_inscriptions,
        "+ Rentrée active",
    )
    col3.metric(
        "🏅 Section N°1",
        (
            df_filtered["Section"].value_counts().idxmax()
            if not df_filtered.empty
            else "N/A"
        ),
    )
    col4.metric(
        "📍 Ville Principale",
        (
            df_filtered["Ville"].value_counts().idxmax()
            if not df_filtered.empty
            else "N/A"
        ),
    )

    st.markdown("<br>", unsafe_allow_html=True)

    g1, g2 = st.columns((2, 1))

    with g1:
        st.subheader("📅 Dynamique des Inscriptions (2026)")
        inscriptions_par_mois = (
            df_filtered.groupby("Mois_Inscription")
            .size()
            .reset_index(name="Nombre")
        )
        fig_timeline = px.area(
            inscriptions_par_mois,
            x="Mois_Inscription",
            y="Nombre",
            markers=True,
            color_discrete_sequence=["#3498db"],
        )
        fig_timeline.update_layout(
            xaxis_title="",
            yaxis_title="Nb Inscriptions",
            margin=dict(l=0, r=0, t=30, b=0),
        )
        st.plotly_chart(fig_timeline, use_container_width=True)

    with g2:
        st.subheader("🎯 Répartition par Section")
        fig_bar = px.bar(
            df_filtered["Section"].value_counts().reset_index(name="Nb"),
            x="Nb",
            y="Section",
            orientation="h",
            color="Section",
            text_auto=True,
        )
        fig_bar.update_layout(
            showlegend=False,
            xaxis_title="",
            yaxis_title="",
            margin=dict(l=0, r=0, t=30, b=0),
        )
        st.plotly_chart(fig_bar, use_container_width=True)

# --- ONGLET 2 : SUIVI FINANCIER ---
with tab2:
    f1, f2, f3 = st.columns(3)
    total_attendu = df_filtered["Tarif (€)"].sum()
    total_encaisse = df_filtered[df_filtered["Statut"] == "Payé"][
        "Tarif (€)"
    ].sum()
    reste_a_percevoir = total_attendu - total_encaisse
    taux = (total_encaisse / total_attendu * 100) if total_attendu > 0 else 0

    f1.metric("💰 Chiffre d'Affaires Attendu", f"{total_attendu:,.0f} €")
    f2.metric("✅ Total Encaissé", f"{total_encaisse:,.0f} €")
    f3.metric(
        "⚠️ Reste à Recouvrer",
        f"{reste_a_percevoir:,.0f} €",
        f"-{taux:.1f}% encaissé",
        delta_color="inverse",
    )

    st.markdown("---")

    c1, c2 = st.columns(2)
    with c1:
        st.subheader("🍕 État des Paiements")
        fig_pie = px.pie(
            df_filtered,
            names="Statut",
            color="Statut",
            hole=0.4,
            color_discrete_map={
                "Payé": "#2ecc71",
                "En attente": "#f1c40f",
                "Incomplet": "#e74c3c",
            },
        )
        fig_pie.update_traces(textposition="inside", textinfo="percent+label")
        st.plotly_chart(fig_pie, use_container_width=True)

    with c2:
        st.subheader("💎 Revenus par Ville")
        fig_rev = px.histogram(
            df_filtered,
            x="Ville",
            y="Tarif (€)",
            color="Statut",
            barmode="group",
            color_discrete_map={
                "Payé": "#2ecc71",
                "En attente": "#f1c40f",
                "Incomplet": "#e74c3c",
            },
        )
        st.plotly_chart(fig_rev, use_container_width=True)

# --- ONGLET 3 : BASE DE DONNÉES & EXPORT ---
with tab3:
    st.subheader("📇 Annuaire Filtré")

    st.dataframe(
        df_filtered,
        column_config={
            "ID_Adherent": st.column_config.TextColumn("ID", max_chars=10),
            "Tarif (€)": st.column_config.NumberColumn(
                "Cotisation", format="%d €"
            ),
            "Date_Inscription": st.column_config.DateColumn(
                "Date Inscription", format="DD/MM/YYYY"
            ),
        },
        use_container_width=True,
        hide_index=True,
    )

    csv = df_filtered.to_csv(index=False).encode("utf-8")
    st.download_button(
        label="📥 Exporter cette liste ciblée (CSV)",
        data=csv,
        file_name="adherents_filtres.csv",
        mime="text/csv",
    )