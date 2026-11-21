import pandas as pd
df=pd.read_csv("data/socialpulse_comments_synthetic.csv")

print("\n--- Apercu des donnees ---")
print(df.head())
print("\n--- Dimensions ---")
print(df.shape)
print("\n --- Informations ---")
print(df.info())
print("\n--- Valeurs manquantes ---")
print(df.isnull().sum())
print("\n--- Nombre de doublons ---")
print(df.duplicated().sum())
print("\n--- Statistiques ---")
print(df.describe(include='all'))



# 1. Vérifier les commentaires vides
print("Commentaires vides :",
      df["comment_text"].isna().sum())

# 2. Supprimer les espaces inutiles
df["comment_text"] = df["comment_text"].str.strip()

# 3. Supprimer les commentaires vides
df = df[df["comment_text"] != ""]

# 4. Convertir la date en format datetime
df["comment_date"] = pd.to_datetime(df["comment_date"])

# 5. Vérifier les types après conversion
print("\n--- Nouveaux types ---")
print(df.dtypes)

# 6. Afficher les résultats
print("\n--- Dataset nettoyé ---")
print(df.head())