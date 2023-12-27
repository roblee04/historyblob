
# csv format
# csv/moz_places.csv
# id,url,title,rev_host,visit_count,
# hidden,typed,frecency,last_visit_date,guid,
# foreign_count,url_hash,description,preview_image_url,site_name,origin_id,
# recalc_frecency,alt_frecency,recalc_alt_frecency

import pandas as pd
import time
from bertopic import BERTopic
from wordcloud import WordCloud
import matplotlib.pyplot as plt
from sklearn.feature_extraction.text import CountVectorizer

file = 'csv/moz_places.csv'
# Read the CSV file into a DataFrame
df = pd.read_csv(file)

columns_to_check = ['title', 'last_visit_date']
df = df.dropna(subset=columns_to_check)


# PREPROCESSING
# remove all mentions of DUO and SCU
df = df[df["title"].str.contains("Duo Security| Santa Clara University") == False]

# remove google-search ending
df['title'] = df['title'].str.replace(r'- Google Search$', '')

# only capture the last 7 days. 
time_in_week = 604800
curr_time = int(time.time()) # dont need to be too precise, cast into int
time_in_ms = (curr_time - time_in_week) * 1000000
past_week_df = df[df.last_visit_date >= time_in_ms]

# Select specific columns, 
# id | url | title | last_visit_date (unix time)
selected_columns = past_week_df[['id', 'title', 'last_visit_date']]

output_file_path = 'data.csv'
# # Save the selected columns to a new CSV file
selected_columns.to_csv(output_file_path, index=False)

# PROCESSING

# convert dataframe to list
docs = past_week_df['title'].tolist()

# remove frequent stopwords  
vectorizer_model = CountVectorizer(stop_words="english")

# bertopic
topic_model = BERTopic(vectorizer_model=vectorizer_model)
topics, probs = topic_model.fit_transform(docs)
topic_model.reduce_topics(docs, nr_topics=10)

# wordcloud and colors

colors = ['#33a02c', '#ff7f00', '#6a3d9a', '#e31a1c', '#fdbf6f', '#a6cee3', '#b2df8a', '#fb9a99', '#cab2d6']
def custom_color_func(word, font_size, position, orientation, random_state=None, **kwargs):
    topic, s = topic_model.find_topics(word, top_n = 1)
    topic = topic[0]
    if topic == -1:
        return '#1f78b4'
    else:
        return colors[topic]


def create_wordcloud(topic_model, topics, save_path=None):
    text = {}
    for i in range(-1, topics - 2):
        for word, value in topic_model.get_topic(i):
            text[word] = value
            
    # text = {word: value for word, value in topic_model.get_topic(i)}
    wc = WordCloud(color_func=custom_color_func, width=1600, height=800, background_color="white", max_words=100)
    wc.generate_from_frequencies(text)
    
    plt.figure( figsize=(10,5))
    plt.imshow(wc, interpolation="bilinear")
    plt.tight_layout(pad=0)
    plt.axis("off")
        

    if save_path:
        plt.savefig(save_path)
    else:
        plt.show()

# Show and save word cloud
save_path = "wordcloud.png"  # Change the filename as needed
# create_wordcloud(topic_model, save_path=save_path)
create_wordcloud(topic_model, topics=10, save_path=save_path)

print(topic_model.get_topic_info())

