import pandas as pd

df = pd.read_csv("data/sentiment_results.csv")

#selet 10 comments from each predicted sentiment
sample=(df.groupby("sentiment", group_keys=False)
        .sample(n=10, random_state=42)
        .reset_index(drop=True))


#keep only the information needed for human evaluation
validation=sample[["comment_id","comment_text"]].copy()

#Add columns for human annotation
validation["human_sentiment"]=""
validation["notes"]=""

#Export the validation sample
validation.to_csv("data/validation_sample.csv",
                  index=False,
                  encoding="utf-8-sig")


print("Validation sample created successfully!")
print("Number of comments:", len(validation))
print(validation.head())