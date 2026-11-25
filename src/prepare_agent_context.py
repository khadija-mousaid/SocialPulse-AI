import pandas as pd
import json
import ast
from pathlib import Path


#1 charger les fichiers csv
data_path = Path("data")
comments_df = pd.read_csv(data_path/"topic_results.csv")
insights_df = pd.read_csv(data_path/"customer_insights.csv")
issues_df = pd.read_csv(data_path/"issue_results.csv")
needs_df = pd.read_csv(data_path/"customer_needs_results.csv")


total_comments = len(comments_df)
sentiment_counts = comments_df["sentiment"].value_counts()
print("\n--- SENTIMENT DISTRIBUTION ---")
print(sentiment_counts)


sentiment_distribution={}

for sentiment, count in sentiment_counts.items():

    percentage = round((count / total_comments) * 100, 2)

    sentiment_distribution[sentiment] = {
        "count": int(count),
        "percentage": percentage
    }

print("\n--- SENTIMENT OVERVIEW ---")

print(sentiment_distribution)





#analyser les themes
comments_df["topics"]= comments_df["topics"].apply(
    ast.literal_eval
)
print("\n--- TOPIC EXAMPLES ---")

print(comments_df[["comment_id", "topics"]].head(10))













#transformer chaque theme en ligne
topics_exploded = comments_df.explode("topics")

#compter les occurrences de chaque theme
topic_counts = topics_exploded["topics"].value_counts()

print("\n--- TOPIC DISTRIBUTION ---")

print(topic_counts)












#2 verifier le chargement
print("Donnees chargees avec succes !")

print("commentaires :", len(comments_df))
print("Insights :",len(insights_df))
print("Problemes :", len(issues_df))
print("Besoin :", len(needs_df))

