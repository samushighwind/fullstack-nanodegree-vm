#
# Database access functions for the web forum.
# 

import time
import psycopg2
import bleach

## Database connection
db = psycopg2.connect("dbname=forum")
c = db.cursor()

## Get posts from database.
def GetAllPosts():
    '''Get all the posts from the database, sorted with the newest first.

    Returns:
      A list of dictionaries, where each dictionary has a 'content' key
      pointing to the post content, and 'time' key pointing to the time
      it was posted.
    '''
    c.execute('SELECT content, time FROM posts ORDER BY time DESC')
    return (dict(zip(["content", "time"],
      (str(bleach.clean(column)) for column in row)))
      for row in c.fetchall())

## Add a post to the database.
def AddPost(content):
    '''Add a new post to the database.

    Args:
      content: The text content of the new post.
    '''
    c.execute("INSERT INTO posts (content) VALUES (%s)",
      (str(bleach.clean(content)),))
    db.commit()
