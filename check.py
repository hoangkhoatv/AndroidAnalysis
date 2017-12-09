import os, time
path_to_watch = "."
before = dict ([(f, None) for f in os.listdir (path_to_watch)])
i = 10
for x in range(0,i):
    time.sleep (10)
    after = dict ([(f, None) for f in os.listdir (path_to_watch)])
    added = [f for f in after if not f in before]
    removed = [f for f in before if not f in after]
    if added: 
        print added
        print "Added: ", ", ".join (added)
        i = i + 1
    if removed: print "Removed: ", ", ".join (removed)
    before = after
