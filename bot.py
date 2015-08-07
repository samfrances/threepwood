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

# if there are no new twitter mentions, report this and exit
mentions = list(curs.items())
if len(mentions) == 0:
    print "-----------"
    print "No new twitter mentions"
    print "-----------"
    exit()

# Reverse mentions list so that oldest is first
mentions.reverse()

# reply to mentions, and note latest id
for mention in mentions:
    # record last twitter mention dealt with
    since_id = mention.id
    # formulate reply
    user = mention.user.screen_name
    incoming_insult = mention.text
    retort = guybrush.insult(incoming_insult)
    reply = u"@{0} {1}".format(user, retort)
    # reply to twitter mention
    try:
        api.update_status(status=reply, in_reply_to_status_id=mention.id)
    except tweepy.error.TweepError as e:
        print e
        print mention.id
        #record last id and exit
        with open(since_id_file, 'w+') as f:
            f.write(str(mention.id))
        exit()
    else:
        print "-----------"
        print mention.id
        print incoming_insult.encode('utf-8', errors="replace")
        print reply.encode('utf-8', errors="replace")
        print "-----------"
    
#record last id
with open(since_id_file, 'w+') as f:
    f.write(str(since_id))
