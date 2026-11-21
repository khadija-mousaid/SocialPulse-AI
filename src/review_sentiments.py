import pandas as pd

df=pd.read_csv("data/sentiment_results.csv")

uncertain=df.sort_values(by="confidence",
                         ascending=True)

print("\n--- 15 predictions a verifier ---")

for _, row in uncertain.head(15).iterrows():
    print("\nCommentaire :", row["comment_text"])
    print("Sentiment :", row["sentiment"])
    print("Confiance :", row["confidence"])
    print("-"*40)