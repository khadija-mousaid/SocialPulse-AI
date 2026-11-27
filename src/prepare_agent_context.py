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



# analyser les problemes detectes
issues_df["issues"]=issues_df["issues"].apply(
    ast.literal_eval
)

print("\n--- ISSUE EXAMPLES ---")

print(
    issues_df[["comment_id","issues"]].head(10)
)

#separer les problemes multiples
issues_exploded= issues_df.explode("issues")

#compter chaque type de probleme
issues_counts=issues_exploded["issues"].value_counts()
print("\n--- ISSUE DISTRIBUTION ---")
print(issues_counts)

#analyser les besoins des clients
needs_df["detected_needs"]= needs_df["detected_needs"].apply(
    ast.literal_eval
)

print("\n--- CUSTOMER NEEDS EXAMPLES ---")
print(
    needs_df[["comment_id","detected_needs"]].head(10)
)

#separer les besoins multiples
needs_exploded=needs_df.explode("detected_needs")

#exclure les commentaires sans besoin detecte
needs_exploded=needs_exploded[needs_exploded["detected_needs"] != "no_need_detected"]

#compter chaque type de besoin
needs_counts = needs_exploded["detected_needs"].value_counts()
print("\n--- CUSTOMER NEEDS DISTRIBUTION ---")
print(needs_counts)


#construire le contexte de l'agent
agent_context = {
    "metadata":{
        "project": "SocialPulse AI",
        "dataset_type": "synthetic",
        "total_comments": int(total_comments)
    },
    "sentiment_overview": sentiment_distribution,

    "topic_overview": {
        str(topic): int(count)
        for topic, count in topic_counts.items()
    },

    "issue_overview":{
        str(issue): int(count)
        for issue, count in issues_counts.items()
    },

    "customer_needs_overview":{
        str(need): int(count)
        for need, count in needs_counts.items()
    }

}

print("\n--- AGENT CONTEXT ---")
print(agent_context)


#ajouter des preuves pour chaque probleme
issue_evidence={}

for _, row in issues_df.iterrows():
    detected_issues = row["issues"]
    for issue in detected_issues:
        if issue not in issue_evidence:
            issue_evidence[issue]=[]

        issue_evidence[issue].append({
            "comment_id": row["comment_id"],
            "comment_text": row["comment_text"]
        })



agent_context["issue_evidence"]=issue_evidence
print("\n--- ISSUE EVIDENCE EXAMPLES ---")
for issue, examples in list(issue_evidence.items())[:3]:
    print("\nProbleme :",issue)

    for example in examples:
        print(example)




#ajouter des preuves pour chaque besoin client
need_evidence={}
for _, row in needs_df.iterrows():
    detected_needs = row["detected_needs"]
    for need in detected_needs:
        if need == "no_need_detected":
            continue
        if need not in need_evidence:
            need_evidence[need]=[]

        need_evidence[need].append({
            "comment_id": row["comment_id"],
            "comment_text": row["comment_text"]
        })

agent_context["customer_needs_evidence"]=need_evidence
print("\n--- CUSTOMER NEEDS EVIDENCE EXAMPLES ---")

print("\n--- DEBUG NEEDS DATA ---")

print(
    needs_df[
        needs_df["detected_needs"].apply(
            lambda x: x != ["no_need_detected"]
        )
    ][["comment_id", "comment_text", "detected_needs"]]
)

for need, examples in list(need_evidence.items())[:3]:

    print("\nBesoin :", need)

    for example in examples:
        print(example)              