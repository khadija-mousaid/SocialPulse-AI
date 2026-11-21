import pandas as pd
import re

df=pd.read_csv("data/socialpulse_comments_synthetic.csv")

def clean_text(text):
    text=text.lower()
    text=text.strip()
    text=re.sub(r"\s+", " ",text)
    return text

df["cleaned_text"]=df["comment_text"].apply(clean_text)

print(df[["comment_text", "cleaned_text"]].head(10))

df.to_csv("data/processed_comments.csv",
          index=False,
          encoding="utf-8-sig")


print("\nFichier processed_comments.csv cree avec succes!")