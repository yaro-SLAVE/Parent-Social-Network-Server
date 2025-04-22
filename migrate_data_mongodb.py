from pymongo import MongoClient
from sqlalchemy import create_engine
import pandas as pd
import datetime

DATABASES = {
    'default':{
        'ENGINE':'mssql',                    
        'NAME':'Parent Social Network',                       
        'HOST':'DESKTOP-G9L5RFP\MSSQLSERVER01', 
        'OPTIONS': {
            'driver': 'ODBC Driver 17 for SQL Server',
        },
    }
}

MONGO_CLIENT = MongoClient('mongodb://localhost:27017/')
MONGO_DB = MONGO_CLIENT['social_network']

sql_engine = create_engine(
    f"mssql+pyodbc://@"
    f"{DATABASES['default']['HOST']}/{DATABASES['default']['NAME']}?"
    f"driver={DATABASES['default']['OPTIONS']['driver']}"
)

# Подключение к MongoDB
mongo_client = MONGO_CLIENT
mongo_db = MONGO_DB



# Пример миграции для модели User
def transform_users():
    profiles_df = pd.read_sql_table('social_network_userprofile', sql_engine)
    users_df = pd.read_sql_table('auth_user', sql_engine)

    users = []

    for _, profile in profiles_df.iterrows():
        user = users_df[users_df['id'] == profile['user_id']].to_dict('records')

        user = user[0]

        user_doc ={
            "_id": profile["id"],
            "logo": profile["logo"],
            "birth_date": str(profile["birth_date"]),
            "user": {
                'user_id': user['id'],
                'username': user['username'],
                'password': user['password'],
                'email': user['email'],
                'first_name': user['first_name'],
                'last_name': user['last_name'],
                'is_active': user['is_active'],
                'is_superuser': user['is_superuser'],
                'is_staff': user['is_staff'],
                'date_joined': str(user['date_joined']),
                'last_login': str(user['last_login'])
            }
        }

        users.append(user_doc)

    mongo_db.users.insert_many(users)

def transform_basements():
    basements_df = pd.read_sql_table('social_network_basement', sql_engine)
    users_df = pd.read_sql_table('auth_user', sql_engine)
    userbasements_df = pd.read_sql_table('social_network_userbasement', sql_engine)
    childs_df = pd.read_sql_table('social_network_child', sql_engine)
    profiles_df = pd.read_sql_table('social_network_userprofile', sql_engine)

    basements = []

    for _, basement in basements_df.iterrows():
        userbasements = userbasements_df[userbasements_df['basement_id'] == basement['id']].to_dict('records')

        users = []
        for userbasement in userbasements:
            user = users_df[users_df['id'] == userbasement['user_id']].to_dict('records')
            user = user[0]
            profile = profiles_df[profiles_df['user_id'] == user['id']].to_dict('records')

            if len(profile) > 0:
                profile = profile[0]
                users.append({
                    "user_id": profile["id"],
                    "username": user["username"],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"]
                })
        
        childs = childs_df[childs_df['basement_id'] == basement['id']].to_dict('records')
        childs_list = []
        for child in childs:
            childs_list.append({
                "first_name": child['first_name'],
                "birth_date": str(child['birth_date']),
                "gender": child['gender']
            })

        basement_doc = {
            "_id": basement["id"],
            "address": basement["address"],
            "capacity": basement["capacity"],
            "users": users,
            "childs": childs_list
        }

        basements.append(basement_doc)

    mongo_db.basements.insert_many(basements)

def transform_posts():
    users_df = pd.read_sql_table('auth_user', sql_engine)
    childs_df = pd.read_sql_table('social_network_child', sql_engine)
    profiles_df = pd.read_sql_table('social_network_userprofile', sql_engine)
    posts_df = pd.read_sql_table('social_network_post', sql_engine)
    comments_df =  pd.read_sql_table('social_network_comment', sql_engine)
    post_likes_df = pd.read_sql_table('social_network_postlike', sql_engine)
    post_photos_df = pd.read_sql_table('social_network_postphoto', sql_engine)
    child_photos_df = pd.read_sql_table('social_network_childphoto', sql_engine)
    post_reactions_df = pd.read_sql_table('social_network_postreaction', sql_engine)
    reactions_df = pd.read_sql_table('social_network_reaction', sql_engine)

    posts = []

    for _, post in posts_df.iterrows():
        user = users_df[users_df["id"] == post["user_id"]].to_dict('records')
        user = user[0]

        profile = profiles_df[profiles_df["user_id"] == user["id"]].to_dict('records')

        if len(profile) > 0:
            profile = profile[0]

            likes = post_likes_df[post_likes_df["post_id"] == post["id"]].to_dict('records')
            likes_doc = []
            for like in likes:
                likes_doc.append({
                    "user_id": like["user_id"],
                    "date": like["date"]
                })

            comments = comments_df[comments_df["post_id"] == post["id"]].to_dict('records')
            comments_doc = []
            for comment in comments:
                comments_doc.append(comment["id"])

            photos_doc = []

            photos = post_photos_df[post_photos_df["post_id"] == post["id"]].to_dict('records')
            for photo in photos:
                childs = child_photos_df[child_photos_df["photo_id"] == photo["id"]].to_dict('records')
                childs_doc = []

                for child_photo in childs:
                    child = childs_df[childs_df["id"] == child_photo["child_id"]].to_dict('records')
                    child = child[0]

                    childs_doc.append({
                        "first_name": child["first_name"],
                        "birth_date": str(child["birth_date"]),
                        "gender": child["gender"]
                    })
                
                photos_doc.append({
                    "photo": photo["photo"],
                    "childs": childs_doc
                })

            reactions = post_reactions_df[post_reactions_df["post_id"] == post["id"]].to_dict('records')
            reactions_doc = []

            for reaction in reactions:
                react = reactions_df[reactions_df["id"] == reaction["reaction_id"]].to_dict('records')
                react = react[0]

                reactions_doc.append({
                    "reaction": react["reaction"],
                    "date": str(reaction["date"]),
                    "user_id": reaction["user_id"]
                })

            post_doc = {
                "_id": post["id"],
                "title": post["title"],
                "body": post["body"],
                "date": str(post["create_time"]),
                "user": {
                    "user_id": profile["id"],
                    "username": user["username"],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"]
                },
                "likes": likes_doc,
                "comments": comments_doc,
                "photos": photos_doc,
                "reactions": reactions_doc
            }

            posts.append(post_doc)
    mongo_db.posts.insert_many(posts)
    
def transform_comments():
    users_df = pd.read_sql_table('auth_user', sql_engine)
    profiles_df = pd.read_sql_table('social_network_userprofile', sql_engine)
    comments_df =  pd.read_sql_table('social_network_comment', sql_engine)
    comment_likes_df =  pd.read_sql_table('social_network_commentlike', sql_engine)

    comments = []

    for _, comment in comments_df.iterrows():
        user = users_df[users_df["id"] == comment["user_id"]].to_dict('records')
        user = user[0]

        profile = profiles_df[profiles_df["user_id"] == user["id"]].to_dict('records')

        if len(profile) > 0:
            profile = profile[0]

            likes = comment_likes_df[comment_likes_df["comment_id"] == comment["id"]].to_dict('records')
            likes_doc = []

            for like in likes:
                likes_doc.append({
                    "user_id": like["user_id"],
                    "date": str(like["date"])
                })

            comment_doc = {
                "_id": comment["id"],
                "body": comment["body"],
                "date": str(comment["date"]),
                "user": {
                    "user_id": profile["id"],
                    "username": user["username"],
                    "first_name": user["first_name"],
                    "last_name": user["last_name"]
                },
                "likes": likes_doc
            }

            comments.append(comment_doc)
    
    mongo_db.comments.insert_many(comments)

def transform_reactions():
    reactions_df = pd.read_sql_table('social_network_reaction', sql_engine)

    reactions = []

    for _, reaction in reactions_df.iterrows():
        reactions.append({
            "_id": reaction["id"],
            "reaction_name": reaction["reaction_name"],
            "reaction": reaction["reaction"]
        })
    
    mongo_db.reactions.insert_many(reactions)
# Выполнение миграций
if __name__ == '__main__':
    #transform_users()
    #transform_basements()
    #transform_posts()
    #transform_comments()
    transform_reactions()