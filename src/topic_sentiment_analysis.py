import pandas as pd
from collections import defaultdict

# Charger directement les résultats
df = pd.read_csv("data/topic_results.csv")

print("Colonnes disponibles :", df.columns.tolist())

#4 convertir la colonne topics en listes python
df["topics"]=df["topics"].apply(lambda x: eval(x) if isinstance(x, str) and x.startswith("[") else [])


#5 compter les sentiments par theme
results=[]

for _, row in df.iterrows():
    for topic in row["topics"]:
        results.append({
            "topic": topic, 
            "sentiment": row["sentiment"]
        })


analysis_df=pd.DataFrame(results)

summary=(
    analysis_df
    .groupby(["topic","sentiment"])
    .size()
    .reset_index(name="count")
)


print("\n--- ANALYSE THEME + SENTIMENT ---")
print(summary.to_string(index=False))


#6 enregistrer le resultat
summary.to_csv(
    "data/topic_sentiment_summary.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nFichier topic_sentiment_summary.csv créé !")