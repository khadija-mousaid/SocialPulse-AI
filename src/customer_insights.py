import pandas as pd
import ast

#1 charger les resultats precedents
df=pd.read_csv("data/topic_results.csv")

#2 transformer les themes en listes python
def parse_topics(value):
    try:
        return ast.literal_eval(value)
    except (ValueError, SyntaxError):
        return []


df["topics"]=df["topics"].apply(parse_topics)

#3 garder les commentaires negatifs
negative_df=df[df["sentiment"]=="negative"].copy()

#4 separer les themes
negative_topics= negative_df.explode("topics")

#supprimer les lignes sans theme
negative_topics=negative_topics.dropna(subset=["topics"])

#5 compter les commentaires negatifs par theme
insights = (negative_topics.groupby("topics").agg(
    negative_count = ("comment_id", "count"),
    evidence=("comment_text", lambda x: list(x.head(3)))
)
.reset_index()
)

#6 trier les themes
insights = insights.sort_values(
    by="negative_count",
    ascending=False
)


# 7. Afficher les résultats
print("\n--- CUSTOMER INSIGHTS ---")

for _, row in insights.iterrows():

    print("\nThème :", row["topics"])

    print(
        "Nombre de commentaires négatifs :",
        row["negative_count"]
    )

    print("Exemples de commentaires :")

    for comment in row["evidence"]:
        print("-", comment)



#8 sauvegarder les resultats
insights.to_csv(
    "data/customer_insights.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nFichier customer_insights.csv cree !")