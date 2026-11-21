
import pandas as pd
from transformers import pipeline

# Charger les commentaires nettoyés
df = pd.read_csv("data/processed_comments.csv")

# Charger le modèle multilingue
model_name = "cardiffnlp/twitter-xlm-roberta-base-sentiment"

sentiment_model = pipeline(
    "sentiment-analysis",
    model=model_name,
    tokenizer=model_name
)

# Analyser tous les commentaires
results = sentiment_model(
    df["cleaned_text"].fillna("").tolist(),
    batch_size=8,
    truncation=True
)

# Ajouter les résultats au DataFrame
df["sentiment"] = [result["label"] for result in results]
df["confidence"] = [round(result["score"], 3) for result in results]

# Afficher quelques résultats
print("\n--- Résultats de l'analyse ---")
print(df[["comment_text", "sentiment", "confidence"]].head(10))

# Répartition des sentiments
print("\n--- Répartition des sentiments ---")
print(df["sentiment"].value_counts())

# Sauvegarder les résultats
df.to_csv(
    "data/sentiment_results.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nFichier sentiment_results.csv créé avec succès !")
