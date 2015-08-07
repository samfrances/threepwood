import tweepy, os, guybrush
from secretconf import CONSUMER_KEY, CONSUMER_SECRET, ACCESS_KEY, ACCESS_SECRET

auth = tweepy.OAuthHandler(CONSUMER_KEY, CONSUMER_SECRET)
auth.set_access_token(ACCESS_KEY, ACCESS_SECRET)
api = tweepy.API(auth)

# Check if there is a last tweet id saved, and get since_id from it if it does
this_module_directory = os.path.dirname(os.path.realpath(__file__))
since_id_file = os.path.join(this_module_directory, "since_id.txt")
if os.path.isfile(since_id_file):
    with open(since_id_file, 'r') as f:
        since_id = f.read().strip()
else:
    since_id = None

# Make the appropriate cursor, depending on whether we have a since_id or not
if since_id:
    curs = tweepy.Cursor(api.mentions_timeline, since_id=since_id)
else:
    curs = tweepy.Cursor(api.mentions_timeline, since_id=since_id)

# reply to mentions, and note latest id]
first = True
for mention in curs.items():
    # get latest since_id
    if first:
        since_id = mention.id
        first = False
    user = mention.user.screen_name
    incoming_insult = mention.text
    print incoming_insult
    retort = guybrush.insult(incoming_insult)
    reply = "@{0} {1}".format(user, retort)
    api.update_status(status=reply, in_reply_to_status_id=mention.id)

#record last id
with open(since_id_file, 'w+') as f:
    f.write(str(since_id))