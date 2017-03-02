import bisect

class Ring:
    def __init__(self, hashFn, replicas):
        self.hashFn = hashFn
        self.replicas = replicas

        self.sortedHashedBucketKeys = []
        self.bucketKeyMapping = {}

    def addBucket(self, bucketKey):
        hashedBucketKey = self.hashFn(bucketKey)
        self.bucketKeyMapping[hashedBucketKey] = bucketKey
        insertPosition = bisect.bisect_left(self.sortedHashedBucketKeys, hashedBucketKey)
        self.sortedHashedBucketKeys.insert(insertPosition, hashedBucketKey)

    def findBucketsForKey(self, key):
        possibleBuckets = []
        for i in xrange(self.replicas):
            replicatedHashedKey = self.hashFn(key + i)
            nearestPos = bisect.bisect_left(self.sortedHashedBucketKeys, replicatedHashedKey)
            if nearestPos != len(self.sortedHashedBucketKeys):
                possibleBuckets.append(self.bucketKeyMapping[self.sortedHashedBucketKeys[nearestPos]])
            else:
                possibleBuckets.append(self.bucketKeyMapping[self.sortedHashedBucketKeys[-1]])
        return possibleBuckets
