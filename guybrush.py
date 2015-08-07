"""A module with a simple function that replies to monkey island insults,
knowledge of which it loads from insults.txt"""

import os.path, string, random

def _sanitise_insult(text):
    """Remove punctuation from an insult and render into lowercase."""
    exclude = set(string.punctuation)
    return ''.join(ch for ch in text if ch not in exclude).lower()

def _parse_insults(text):
    """Parse the contents of a file of insults.
    return dictionary of insults and responses """
    # Split up the insult pairs
    pairs_text = text.strip().split("\n\n")
    # Turn the insult pairs into a list of pairs, discarding any invalid
    # entries with more or less than two lines
    pairs = filter((lambda x: len(x) == 2),
                   (p.splitlines() for p in pairs_text))
    # sanitise insults so that punctuation and case can be ignored
    pairs = [(_sanitise_insult(x), y) for x, y in pairs]
    return dict(pairs)

def _load_insults():
    """Load insults from config file and parse,
    returning dict of insults and responses"""
    # Put together path to config file
    this_module_directory = os.path.dirname(os.path.realpath(__file__))
    configpath = os.path.join(this_module_directory, "insults.txt")
    # Load and parse the insults
    with open(configpath, 'r') as f:
        insults = _parse_insults(f.read())
    return insults

def insult(insult_text):
    """Respond to a Monkey Island insult"""
    insults = _load_insults()
    insult_text = _sanitise_insult(insult_text)
    # Check if the text contains an insult, and if so, return appropriate retort
    for i in insults:
        if i in insult_text:
            return insults[i]
    # If insult is unknown, return a random rubbish insult
    return random.choice(("You are rubber, I am glue!",
                          "Oh yeah?"))

def test():
    print "Hello.\n", insult("Hello.")
    print
    print "You smell bad.\n", insult("You smell bad.")
    print
    print "I once owned a dog that was smarter than you.\n", insult("I once owned a dog that was smarter than you.")
    print
    print "I once owned a dog that was smarter than you.5555\n", insult("I once owned a dog that was smarter than you.")

if __name__ == "__main__":
    test()
