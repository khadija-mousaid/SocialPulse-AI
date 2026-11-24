import pandas as pd

#charger les donnees
df=pd.read_csv("data/topic_results.csv")


#conserver tous les commentaires
needs_df=df.copy()

print("nombre total de commentaires :", len(needs_df))

print(needs_df[["comment_id", "comment_text", "sentiment"]].head(10))



need_keywords = {

    "menu_request": [
        "plus de plats",
        "plats marocains",
        "plus de choix",
        "plus de variété",
        "more meals",
        "more dishes",
        "more dishes",
        "plus de choix de sauces",
        "ajoutez-le définitivement au menu",
        "add it to the menu"
    ],

    "dietary_preference": [
        "vegan",
        "végétarien",
        "végétarienne",
        "sans gluten",
        "gluten free",
        "sans lactose"
    ],

    "feature_request": [
        "noter chaque plat",
        "évaluer chaque plat",
        "rate each dish",
        "note chaque plat"
    ],

    "delivery_request": [
        "étendre la zone de livraison",
        "élargir la zone de livraison",
        "livrer à",
        "plus de quartiers",
        "expand delivery",
        "delivery area"
    ],

    "notification_request": [
        "notification quand le livreur",
        "notification de départ",
        "notifier quand",
        "notification when the driver"
    ],

    "subscription_request": [
        "formule abonnement",
        "abonnement pour la semaine",
        "weekly subscription",
        "meal subscription"
    ],

    "packaging_preference": [
        "moins de plastique",
        "emballage écologique",
        "emballage recyclable",
        "eco-friendly packaging"
    ],

    "portion_preference": [
        "petite et une grande taille",
        "small and large size",
        "different portion sizes",
        "deux tailles"
    ],

    "language_request": [
        "menu disponible en anglais",
        "menu en anglais",
        "available in english",
        "english menu"
    ],

    "payment_request": [
        "plusieurs moyens de paiement",
        "autres moyens de paiement",
        "more payment options",
        "payment methods"
    ]
}





test_comments = [
    "Please add more vegan meals.",
    "J'aimerais voir une formule abonnement pour la semaine.",
    "Please make the menu available in English too.",
    "Je voudrais pouvoir noter chaque plat séparément."
]

for comment in test_comments:
    print("\nComment :", comment)





def detect_needs(comment):

    comment = str(comment).lower()

    detected_needs = []

    for need, keywords in need_keywords.items():

        for keyword in keywords:

            if keyword in comment:
                detected_needs.append(need)
                break

    if len(detected_needs) == 0:
        return ["no_need_detected"]

    return detected_needs







print(
    "Keyword présent :",
    "ajoutez-le définitivement au menu" in need_keywords["menu_request"]
)

print(
    "Test C142 :",
    detect_needs("J'ai aimé le bowl végétarien, ajoutez-le définitivement au menu !")
)





print("\n--- CUSTOMER NEEDS TESTS ---")

for comment in test_comments:

    print("\nComment :", comment)
    print("Detected needs :", detect_needs(comment))







# Appliquer la détection à tous les commentaires
needs_df["detected_needs"] = needs_df["comment_text"].apply(
    detect_needs
)

# Afficher les commentaires qui expriment un besoin
print("\n--- DETECTED CUSTOMER NEEDS ---")

for _, row in needs_df.iterrows():

    if row["detected_needs"] != ["no_need_detected"]:

        print("\nID :", row["comment_id"])
        print("Comment :", row["comment_text"])
        print("Sentiment :", row["sentiment"])
        print("Detected needs :", row["detected_needs"])


# Calculer la fréquence des besoins
needs_exploded = needs_df.explode("detected_needs")

print("\n--- CUSTOMER NEEDS SUMMARY ---")

print(
    needs_exploded[
        needs_exploded["detected_needs"] != "no_need_detected"
    ]["detected_needs"].value_counts()
)


# Compter les commentaires sans besoin détecté
no_need_df = needs_df[
    needs_df["detected_needs"].apply(
        lambda needs: needs == ["no_need_detected"]
    )
]

print("\nComments without detected needs :", len(no_need_df))


# Sauvegarder les résultats
needs_df.to_csv(
    "data/customer_needs_results.csv",
    index=False,
    encoding="utf-8-sig"
)

print("\nFichier customer_needs_results.csv créé !")







