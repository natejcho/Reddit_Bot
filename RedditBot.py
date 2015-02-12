import praw
#for incripted credentials, use voussoir's github, otherwise empty quotes
#import bot
#managing usernames for no endless replies
import sqlite3
import time

#assign important configuarable information into a variable, main body is same that way
#called a final variable never want to change at any moment, in all caps so you can immediately know what it is
USERAGENT = "/u/poopyshowerers python reddit tutorial replybot"
USERNAME = "nchovies"
PASSWORD = "qwerty"
SUBREDDIT = "test"
MAXPOSTS = 10

#list b/c want to give same response for many different phrases
SETPHRASES = ["python", "bots"]
SETRESPONSE = "I am a python bot"

#if its a small subreddit you don't need to check too often, this limits it
WAIT = 20

print("Opening database")
sql = sqlite3.connect('sql.db')
cur = sql.cursor()
cur.execute("CREATE TABLE IF NOT EXISTS oldposts(ID TEXT)")
sql.commit()

#So program not silent, only displays once while fxn keeps running
print("Logging in to reddit")
#user agent, ALWAYS include username and describe what doing
r = praw.Reddit(USERAGENT)
#left username, right pswd
r.login(USERNAME, PASSWORD)

def replybot():
    print('Fethcing subreddit ' + SUBREDDIT)
    #which subreddit, no /r/
    subreddit = r.get_subreddit(SUBREDDIT)
    print('Fetching coments')
    #praw can get 100 items at a time, max at 1000, reddit rule 1 call/2sec, small number controls sample size
    comments = subreddit.get_comments(limit=MAXPOSTS)
    #goes through most recent in order
    for comment in comments:
        #? is database sanitization, prevents attack on sql database, preqautionary
        cur.execute('SELECT * FROM oldposts WHERE ID=?', [comment.id])
        if not cur.fetchone():
            try:
                cauthor = comment.author.name
                if cauthor != USERNAME.lower():
                    cbody = comment.body.lower()
                    if any(key.lower() in cbody for key in SETPHRASES):
                        print("Replying to " + cauthor)
                        comment.reply(SETRESPONSE)
                else:
                    #already in database right now though
                    print("Will not reply to self")
            except AttributeError:
                pass

            cur.execute('INSERT INTO oldposts VALUES(?)', [comment.id])
            sql.commit()

while True:
    replybot()
    print("Waiting " + str(WAIT) + " seconds")
    time.sleeping(WAIT)
