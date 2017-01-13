def testHashRing():
    hashFn = lambda x: x
    ring = Ring(hashFn=hashFn, replicas=5)
    keys = [1, 13, 21]
    for key in keys:
        ring.addKey(key)

    for i in xrange(-10, 1):
        assert ring.findKeyGTE(i) == 1
    for i in xrange(1, 6):
        assert ring.findKeyGTE(i) == 1
    for i in xrange(6, 18):
        assert ring.findKeyGTE(i) == 13
    for i in xrange(18, 26):
        assert ring.findKeyGTE(i) == 21
    for i in xrange(26, 31):
        assert ring.findKeyGTE(i) == 21
