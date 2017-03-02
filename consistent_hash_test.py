import hashlib
import consistent_hash as ch

def testHashRing():
    hashFn = lambda x: x
    ring = ch.Ring(hashFn=hashFn, replicas=5)
    buckets = [1, 13, 21]
    for bucket in buckets:
      ring.addBucket(bucket)

    for i in xrange(-10, -2):
        assert ring.findBucketsForKey(i) == [1, 1, 1, 1, 1]
    assert ring.findBucketsForKey(-2) == [1, 1, 1, 1, 13]
    assert ring.findBucketsForKey(0) == [1, 1, 13, 13, 13]
    for i in xrange(2, 10):
        assert ring.findBucketsForKey(i) == [13, 13, 13, 13, 13]
    assert ring.findBucketsForKey(10) == [13, 13, 13, 13, 21]
    for i in xrange(14, 18):
        assert ring.findBucketsForKey(i) == [21, 21, 21, 21, 21]
    assert ring.findBucketsForKey(19) == [21, 21, 21, 21, 21]

if __name__ == '__main__':
    testHashRing()
