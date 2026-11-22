import re
import pandas as pd

#1 charger les commentaires
df=pd.read_csv("data/sentiment_results.csv")

#2 definir les mots cles de chaque theme
topics={
    "delivery":["livraison","livreur","retard","delivery","deliver","التوصيل"],

    "food_quality": ["goût", "frais", "fraîcheur","délicieux", "salé", "sec", "food","bowl", "poulet", "quinoa", "saumon","bon", "bonne", "délicieux", "délicieuse","frais", "fraîche", "fraîcheur","goût", "salé", "sec"],

    "price_payment": ["prix", "cher", "paiement","payer", "carte", "réduction", "frais de livraison"],

    "portions": ["portion", "quantité", "grammes","taille", "généreux","portion", "portions", "quantité","gramme", "grammes", "taille", "tailles","généreux", "généreuse"],

    "menu_diversity": ["menu", "végétarien", "vegan","plats", "choix", "diversité","menu", "végétarien", "végétarienne","végétariennes", "vegan", "plats","choix", "diversité"],

    "nutrition_allergens": ["calories", "protéines", "gluten","allergènes", "allergique", "lactose"],

    "ordering_platform": ["site", "application", "compte","commander", "commande", "formulaire"],

    "customer_service": ["service client", "remboursement","réponse", "contacter", "réclamation"],

    "packaging": ["packaging", "emballage", "plastique","recyclable", "contenant"]

}

def detect_topics(comment):
    detected_topics=[]
    comment=str(comment).lower()
    for topic, keywords in topics.items():
        for keyword in keywords:
            #chercher le mot ou l'expression complete
            pattern=r"(?<!\w)"+re.escape(keyword)+r"(?!\w)"

            if re.search(pattern, comment):
                detected_topics.append(topic)
                break

    return detected_topics




#tester sur quelques commentaires
test_comments=[
    "Le prix est élevé et les portions sont petites.",
    "La livraison était rapide et le repas délicieux.",
    "Votre emballage contient trop de plastique."
]

for comment in test_comments:
    print("\nCommentaire :", comment)
    print("Themes :", detect_topics(comment))



#appliquer l'analyse a tous les commentaires
df["topics"]=df["comment_text"].apply(detect_topics)

#enregistrer les resultats
df.to_csv("data/topic_results.csv", index=False, encoding="utf-8-sig")

print("\n--- Analyse des themes terminee ---")
print("Nombre de commentaires :",len(df))


#afficher les premiers resultats
print(df[["comment_id","comment_text","topics"]].head(10))


print("\nFichier topic_results.csv cree !")




from collections import Counter

# Compter les occurrences de chaque thème
topic_counts = Counter()

for comment_topics in df["topics"]:
    for topic in comment_topics:
        topic_counts[topic] += 1

# Créer un tableau de fréquences
topic_summary = pd.DataFrame(
    topic_counts.items(),
    columns=["topic", "count"]
)

topic_summary = topic_summary.sort_values(
    by="count",
    ascending=False
)

print("\n--- FREQUENCE DES THEMES ---")
print(topic_summary.to_string(index=False))

# Enregistrer les fréquences
topic_summary.to_csv(
    "data/topic_summary.csv",
    index=False,
    encoding="utf-8-sig"
)
