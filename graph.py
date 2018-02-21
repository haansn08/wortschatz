from intervaltree import IntervalTree
from itertools import *
import sys
import time
import matplotlib.pyplot as plt

sys.path.append("/usr/share/anki")

from anki import *
col = Collection("collection.anki2")

def cardIds():
    for i in col.findCards(""):
        yield i

now = int(time.time() * 1000)
def reviewSpans():
    for cid in cardIds():
        revs = col.db.all("select revlog.id,ease,nid from revlog inner join cards on cards.id = revlog.cid where revlog.cid=?",cid)
        a,b = tee(revs)
        if not next(b, None):
            continue
        for span in zip(a,b):
            yield span
        last = list(revs[-1])
        last[0] = now
        #yield revs[-1], last

correctCards = IntervalTree()
for start, end in reviewSpans():
    if end[1] is not 1: #review was correct
        startHour = start[0]
        endHour = end[0]
        correctCards[start[0]:end[0]] = end[2]


beginDate = now - (3*365*24*60*60*1000) #two years ago

dates = []
wordCount = []
for time in range(beginDate, now, 24*60*60*1000):
    dates.append(time)
    correctNodes = set()
    for span in correctCards[time]:
        correctNodes.add(span.data)
    wordCount.append(len(correctNodes))

plt.plot(dates, wordCount)
plt.show()
