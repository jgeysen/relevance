# import text_cleaning as tcf
# import sentence_splitting as ssf
# import feature_engineering as fef

# import pandas as pd
# import joblib

# def extract_relevance(best_model,df_articles,regex_dict,entity_list):
#     df = df_articles.copy()
#     # Create a seperate dataframe for the title, linking an article identifier to an article title.
#     df_titles = df_articles[['title','identifier']]
#     # Create a seperate dataframe for the article bodies, linking an article identifier to an article body.
#     df_article_bodies = df_articles[['article_body','identifier']]
#     # Clean the article bodies using the custom cleaning functions from the text_cleaning module.
#     df_article_bodies['article_body'] = [tcf.clean_reuters_article(x) for x in df_article_bodies.article_body]
#     # Split the article bodies using the custom sentence_splitting function from the sentence_splitting module.
#     df_sentences = ssf.sentence_splitting(df_article_bodies)
#     # append a title column to the dataframe containing sentences.
#     # The title column is required for feature engineering.
#     df_sentences = df_sentences.merge(df_titles,left_on="identifier",right_on="identifier")
#     # perform feature engineering.
#     # Here we also need an entity list and a regex_dict.
#     df_data,all_regex_dict,feature_list= fef.create_features(df_sentences,regex_dict,entity_list)
#     # perform predictions on the df_data.
#     df_data['prediction'] = best_model.predict(df_data[feature_list])

#     # return a dataframe containing article identifier, sentences for that article and the prediction for set specific sentence.
#     df_data = df_data[['identifier','sentences','prediction']]

#     return df_data.reset_index(drop=True)
