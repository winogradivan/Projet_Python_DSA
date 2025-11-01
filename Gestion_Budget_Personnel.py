import streamlit as st
import pandas as pd
from pathlib import Path
from datetime import date
# --- Configuration de la Persistance des Données ---
CSV_FILE = 'data.csv'

def charger_dataframe():
    """
    Charge le DataFrame à partir du fichier CSV ou le crée s'il n'existe pas.
    """
    # Utilise Path pour vérifier si le fichier existe
    if Path(CSV_FILE).exists():
        df = pd.read_csv(CSV_FILE)
        # S'assurer que 'Date' est au format datetime pour la manipulation

        df['Date'] = pd.to_datetime(df['Date'], errors='coerce', format='mixed')
        return df
    else:
        # Crée un DataFrame vide si le fichier n'existe pas
        donne_budget = ({
            'Date':[],
            'Type':[],
            'Montant': [],
            'Catégorie':[]
        })
        df = pd.DataFrame(donne_budget)
        # Sauvegarde le fichier vide pour qu'il existe sur le disque
        df.to_csv(CSV_FILE, index=False)
        return df

# ----------------------------
# Mot de passe pour sécuriser
# ----------------------------
PASSWORD = "Hola"  # change ce mot de passe

# Créer une variable dans session_state pour savoir si l'utilisateur est connecté
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False

# Bloc d'authentification : affiche le formulaire de mot de passe et bloque le reste si non connecté
if not st.session_state.authenticated:
    mdp_saisi = st.text_input("Entrez le mot de passe pour accéder à l'application", type="password")
    if st.button("Valider"):
        if mdp_saisi == PASSWORD:
            st.session_state.authenticated = True
            st.success("Mot de passe correct !")
        else:
            st.error("Mot de passe incorrect !")
    st.stop()  # empêche l'affichage du reste de l'application si non connecté

# --- Initialisation du DataFrame avec le CSV ---
# Charge le DataFrame une seule fois depuis le CSV (ou crée-le) et le stocke dans session_state
if 'df_transactions' not in st.session_state:
    st.session_state.df_transactions = charger_dataframe()

# Alias pour le DataFrame de la session pour un code plus lisible
df = st.session_state.df_transactions

st.title("Suivi du budget personnel")
st.markdown("Saisissez vos revenus et vos dépenses ici pour suivre vos comptes")

st.write("Tableau du Budget")
st.dataframe(df, width='stretch')

# --- Partie 2: Formulaire d'Ajout de Transaction dans la Sidebar ---

with st.sidebar:

    # Définir les catégories de dépenses et de revenus
    categories_depenses = [
        "Alimentation", "Transport", "Logement", "Loisirs",
        "Santé", "Vêtements", "Télécommunications", "Éducation", "Divers"
    ]
    categories_revenus = ["Salaire", "Investissements", "Autre"]

    # Champs du formulaire
    type_saisi = st.selectbox("Type de transaction", ["Revenu", "Dépense"])

    # Afficher les catégories appropriées selon le type de transaction
    if type_saisi == "Dépense":
        categorie_saisie = st.selectbox("Catégorie", options=categories_depenses)
    else:
        categorie_saisie = st.selectbox("Catégorie", options=categories_revenus)

    date_saisie = st.date_input("Date de transaction")
    montant_saisi = st.number_input("Montant", min_value=0.01, step=1.00)

    # 🔹 Enregistrement uniquement quand on clique sur le bouton
    if st.button("Enregistrer la transaction"):
        # CORRECTION DE L'ERREUR: Convierte el objeto datetime.date a una cadena de texto (string)
        # Esto evita el ValueError al intentar guardar un objeto date directamente en el CSV
        date_formattee = date_saisie.strftime('%Y-%m-%d')

        # Création du DataFrame pour la nouvelle ligne
        df_nouvelle_ligne = pd.DataFrame([{
            'Date': date_formattee, # Usamos la fecha formateada como string
            'Type': type_saisi,
            'Montant': montant_saisi,
            'Catégorie': categorie_saisie
        }])

        # Concatène et met à jour le DataFrame de la session
        st.session_state.df_transactions = pd.concat(
            [st.session_state.df_transactions, df_nouvelle_ligne],
            ignore_index=True
        )

        # Sauvegarde immédiate du DataFrame mis à jour dans le CSV
        st.session_state.df_transactions.to_csv(CSV_FILE, index=False)

        st.success("Transaction enregistrée !")
        st.rerun() # Force l'actualisation de la page

# Parte 4 - Dashboard Résumé (Calculs et Visualisation)
# On affiche le tableau de bord uniquement si le DataFrame n'est pas vide

if not df.empty:

    # 1. Filtrer et calculer les totaux (le « traitement simple » du projet)
    # Calcule la somme des montants lorsque le Type est 'Revenu'
    total_revenus = df[df['Type'] == 'Revenu']['Montant'].sum()
    # Calcule la somme des montants lorsque le Type est 'Dépense'
    total_depenses = df[df['Type'] == 'Dépense']['Montant'].sum()
    solde_actuel = total_revenus - total_depenses

    st.subheader("Dashboard Résumé")

    # Crée trois colonnes pour afficher les métriques
    col1, col2, col3 = st.columns(3)

    # metric() est une fonction Streamlit pour afficher une valeur clé (métrique)
    # f-string pour formater la valeur en texte avec le format numérique et l'euro
    col1.metric("Total Revenus", f"{total_revenus:,.2f} €")
    col2.metric("Total Dépenses", f"{total_depenses:,.2f} €")
    col3.metric("Solde Actuel", f"{solde_actuel:,.2f} €")

    # 3. Gráfico (Exigence: Afficher les résultats... graphique)
    st.markdown("---")  # Sépare visuellement le tableau de bord
    st.subheader("Visualisation du Budget (Dépenses vs. Revenus)")

    ## Création d'un petit DataFrame pour le graphique
    df_chart = pd.DataFrame({
        'Type de transaction': ['Revenus', 'Dépenses'],
        'Montant': [total_revenus, total_depenses]
    })

    ## Fonction Streamlit qui affiche un graphique en barres
    st.bar_chart(df_chart, x='Type de transaction', y='Montant', width='stretch')
else:
    ## Message s'il n'y a pas de données
    st.subheader("Dashboard Résumé")
    st.info("Veuillez ajouter votre première transaction dans la barre latérale pour voir le résumé.")

# ---------------------------------------------------------------------
# Partie 5: Visualisation de l'Historique des Transactions (Tableau)
# ---------------------------------------------------------------------

st.subheader("Historique des Transactions")

# Affiche le DataFrame mis a jour et persistant
st.dataframe(
    df,
    width='stretch',
    hide_index=True, # Masque l'index par défaut de Pandas
    column_order=('Date', 'Type', 'Montant', 'Catégorie')
)

# -------------------
# Suppression d'une transaction
# -------------------
st.subheader("Supprimer une transaction")

if not df.empty:
    # Crear una lista de descripciones (incluyendo el índice) para el selectbox
    # Aseguramos que la columna 'Date' esté en formato datetime antes de usar strftime
    df['Date'] = pd.to_datetime(df['Date'], errors='coerce', format='mixed')

    options_suppression = [
        # Formatage de la date en chaîne de caractères pour l'affichage
        f"{i} | {row['Date'].strftime('%Y-%m-%d')} | {row['Type']} | {row['Montant']} € | {row['Catégorie']}"
        for i, row in df.iterrows()
        # Filtrar solo si la fecha no es NaT, para evitar errores en strftime
        if not pd.isna(row['Date'])
    ]

    # Manejar el caso donde no hay opciones válidas después del filtrado
    if options_suppression:
        choix_suppression = st.selectbox("Sélectionnez la transaction à supprimer", options_suppression)

        if st.button("Supprimer la transaction"):
            # Récupérer l'index (la première partie de la chaîne de caractères sélectionnée)
            index_suppression = int(choix_suppression.split(" | ")[0])

            # Supprimer la ligne du DataFrame
            st.session_state.df_transactions = st.session_state.df_transactions.drop(index=index_suppression)

            # Réinitialiser l'index pour éviter les problèmes de suppression ultérieure
            st.session_state.df_transactions.reset_index(drop=True, inplace=True)

            # Sauvegarde immédiate du DataFrame mis à jour dans le CSV
            st.session_state.df_transactions.to_csv(CSV_FILE, index=False)

            st.success("Transaction supprimée !")
            st.rerun() # Force le rechargement de la page pour mettre à jour l'affichage
    else:
        st.info("Aucune transaction valide à supprimer (vérifiez le format des dates).")
else:
    st.info("Aucune transaction à supprimer.")