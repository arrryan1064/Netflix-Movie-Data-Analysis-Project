import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv("mymoviedb.csv", lineterminator= '\n')

df['Release_Date'] = pd.to_datetime(df['Release_Date'])
print(df['Release_Date'].dtype) #
df['Release_Date'] = df['Release_Date'].dt.year
print(df['Release_Date'].dtype) #
# print(df.head())


# droppping the columns
cols = ['Overview', 'Original_Language','Poster_Url' ]
print(df.drop (cols , axis=1,inplace= True) )
print(df.columns)
print(df.head())

# catogorized Vote_average colummns
def categorize_col(df, col, labels):
    edges = [
        df[col].describe()['min'],
        df[col].describe()['25%'],
        df[col].describe()['50%'],
        df[col].describe()['75%'],
        df[col].describe()['max']
    ]
    
    
    labels = ["not_popular", "below_average", "average", "popular"]

    df[col] = pd.cut(df[col], edges, labels=labels, duplicates='drop')
    return df

df = categorize_col(df, 'Vote_Average', None)
print(df[['Title', 'Vote_Average']].head(10))
print(df["Vote_Average"].value_counts ())
df.dropna(inplace=True)
print(df.isnull().sum()) 


# split genres into a list and removing the spacce betn the genres  
df['Genre'] = df['Genre'].apply(lambda x: x.split(', '))
df = df.explode ('Genre') . reset_index(drop=True)
print(df['Genre'])
# casting the genres into category
df['Genre']= df['Genre'].astype('category')
print(df['Genre'].dtype)
print(df.nunique())


# DATA VISUALIZATION 
import seaborn as sns #
sns.set_style('whitegrid')
# we get to solve some question 
# Q1 What is the most frequent genre of movies realised on netflix ?
sns.catplot(y = 'Genre',data = df, kind = 'count',
            order= df['Genre'].value_counts().index ,
            color = "#9642f5" )

plt.title('Genre columns distribution')
plt.show() 

# Q2 which has highest votes in vote column
sns.catplot ( y = 'Vote_Average',data=df,kind='count' ,
             order=df['Vote_Average'] .value_counts().index,
             color="#f54242") 

plt.title("Vote_Average Distribution")
plt.show()

# Q3 What movies got the highest popularities ? what is its genre

max_popularity = df['Popularity'].max()

most_popular_movies = df[df['Popularity'] == max_popularity]

print("Max_popular_movies")

print(most_popular_movies[['Popularity', 'Genre' ]])

# Q4: Which movies got the lowest popularity? What is its genre?

lowest_popularity = df['Popularity'].min()

lowest_popular_movies = df[df['Popularity'] == lowest_popularity]

print("Lowest Popular Movie")

print(lowest_popular_movies[['Title', 'Popularity', 'Genre']])

# Q5 Which year has the most filmed movies
filmed = df['Release_Date'].hist()
plt.title("Release Date Column Distribution")
plt.show()