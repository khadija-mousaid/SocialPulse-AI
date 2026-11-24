import pandas as pd

#1 charger les commentaires
df=pd.read_csv("data/topic_results.csv")

#2 garder les commentaires negatifs
negative_df = df[df["sentiment"] == "negative"].copy()
#3 definir les mots-cles de chaque prebleme
issue_keywords = {
    "late_delivery": [
        "took too long",
        "livraison en retard",
        "reçue à",
        "arrivée après",
        "arrivé après",
        "après ma pause",
        "un peu long pour le déjeuner"
    ],

    "delivery_coverage": [
        "delivery unavailable",
        "livrez",
        "livraison disponible",
        "zone de livraison"
    ],

    "tracking_problem": [
        "notification de livraison",
        "livreur n'était pas encore arrivé",
        "suivi de livraison"
    ],

    "unexpected_delivery_fee": [
        "frais de livraison changent",
        "frais de livraison variable"
    ],

    "missing_item": [
        "il manquait un article",
        "article manquant",
        "boisson commandée était absente",
        "boisson absente",
        "commande est arrivée incomplète",
        "وصلني الطلب ناقص",
        "الطلب ناقص"
    ],

    "wrong_order": [
        "mauvaise commande",
        "ce n'est pas ce que j'avais choisi"
    ],

    "wrong_recipient": [
        "pas la bonne personne",
        "mauvaise personne"
    ],

    "delivery_address_problem": [
        "mauvaise adresse",
        "livrée à la mauvaise adresse"
    ],


    # Food quality
    "cold_food": [
        "repas froid",
        "repas était froid",
        "froid"
    ],

    "dry_food": [
        "poulet était un peu sec",
        "trop sec",
        "viande sèche"
    ],

    # Packaging
    "damaged_packaging": [
        "contenant s'est ouvert",
        "emballage ouvert",
        "difficiles à ouvrir"
    ],

    "contamination": [
        "morceau de plastique dans",
        "corps étranger"
    ],

    "spilled_food": [
        "sauce était renversée",
        "sauce renversée"
    ],

    # Website and application
    "website_problem": [
        "site ne marche pas",
        "page introuvable",
        "lien dans votre bio"
    ],

    "application_performance": [
        "application un peu lente",
        "application lente"
    ],

    "account_problem": [
        "créer un compte",
        "commande n'apparaît pas dans mon compte"
    ],

    # Payment
    "payment_problem": [
        "carte est refusée",
        "options de paiement",
        "confirmation après le paiement"
    ],

    "promo_code_problem": [
        "code promo",
        "offre expire trop vite"
    ],

    # Customer service
    "no_response": [
        "contacter par téléphone sans succès",
        "sans succès",
        "service client m'a demandé"
    ],

    # Menu and nutrition
    "limited_menu_choices": [
        "choix est limité",
        "pas assez de choix",
        "choix des boissons est vraiment limité"
    ],

    "missing_allergen_information": [
        "manque les allergènes",
        "vérifier les allergènes"
    ],


    # Price and portions
    "high_price": [
        "prix est un peu élevé",
        "prix élevé",
        "too expensive",
        "trop cher"
    ],

    "small_portion": [
       "portions sont petites",
       "petite portion",
       "bigger portion",
       "moins généreux",
       "moins généreuse",
       "quantité insuffisante",
       "pour la quantité",
       "petite quantité",
       "quantité faible",
       "pour le prix"
    ],

    # Food quality and presentation
    "presentation_mismatch": [
        "présentation ne ressemble pas à la photo",
        "ne ressemble pas à la photo",
        "différent de la photo"
    ],

    # Menu and nutrition
    "menu_variety": [
        "toujours les mêmes plats",
        "manque de variété",
        "menu change chaque semaine",
        "same dishes"
    ],

    "insufficient_protein": [
        "manque des protéines",
        "pas assez de protéines",
        "not enough protein"
    ],

    "missing_dietary_options": [
        "sans gluten",
        "gluten free",
        "plats végétariens",
        "plats vegan"
    ],

    # Packaging
    "excessive_plastic": [
        "beaucoup de plastique",
        "trop de plastique",
        "moins de plastique"
    ],

    "sustainable_packaging_preference": [
        "moins de plastique même si",
        "emballage moins écologique"
    ],

    # Delivery form
    "delivery_area_selection": [
        "sélectionner mon quartier",
        "choisir mon quartier",
        "quartier dans le formulaire"
    ],

    # Promotions
    "promo_expiration": [
        "expire trop vite",
        "expiration trop rapide",
        "expires too quickly"
    ],

    # General feedback
    "general_dissatisfaction": [
        "correct, sans plus",
        "je ne pense pas recommander",
        "not satisfied"
    ],

    # Feature requests
    "feature_request": [
        "noter chaque plat séparément",
        "évaluer chaque plat",
        "rate each dish separately"
    ],


    "taste_problem": [
        "manque d'assaisonnement",
        "assaisonnement",
        "manquait de goût",
        "trop salé",
        "trop sucré",
        "trop cuit",
        "ajouter des épices"
    ],


}


#4 detecter le probleme

def detect_issues(comment):

    comment = str(comment).lower()

    detected_issues = []

    for issue, keywords in issue_keywords.items():

        for keyword in keywords:

            if keyword in comment:
                detected_issues.append(issue)
                break
    # Distinguer une préférence écologique
    # d'une plainte concernant le plastique
    if "sustainable_packaging_preference" in detected_issues:
        if "excessive_plastic" in detected_issues:
            detected_issues.remove("excessive_plastic")

    if len(detected_issues) == 0:
        return ["unclassified"]

    return detected_issues









# Tests multi-label
test_comments = [
    "Le prix est élevé pour la quantité.",
    "Le repas était bon mais la sauce était renversée dans le sac.",
    "Le packaging contient beaucoup de plastique et il est difficile à ouvrir."
]

print("\n--- MULTI-LABEL TESTS ---")

for comment in test_comments:
    print("\nComment :", comment)
    print("Issues :", detect_issues(comment))







#5 appliquer la fonction
negative_df["issues"]= negative_df["comment_text"].apply(
    detect_issues
)

#6 afficher les resultats
print("\n--- issue detection ---")

for _, row in negative_df.iterrows():
    if row["issues"] != "unclassified":

        print("\nID :", row["comment_id"])
        print("comment :",row["comment_text"])
        print("detected issues :",row["issues"])


# Séparer les différentes issues
issues_exploded = negative_df.explode("issues")

print("\n--- MULTI-LABEL ISSUE SUMMARY ---")

print(issues_exploded["issues"].value_counts())






# Afficher les commentaires non classifiés
unclassified_df = negative_df[
    negative_df["issues"].apply(
        lambda issues: issues == ["unclassified"]
    )
]





#8 sauvegarder
negative_df.to_csv(
    "data/issue_results.csv", index=False, encoding="utf-8-sig"
)


print("\nFichier issue_results.csv cree !")