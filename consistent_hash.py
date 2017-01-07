from collections import namedtuple
CacheEntry = namedtuple('CacheEntry', 'cacheReference hashedCacheReference')

class CacheEntryIndex:
    def __init__(self):
        # TODO use list for now
        self.cacheEntryList = []

    def addEntry(self, entry):
        self.cacheEntryList.append(entry)

    def findNearestCacheEntry(self, hashedCacheObject):
        distances = [(cacheEntry.hashedCacheReference-hashedKey, cacheEntry) for cacheEntry in self.cacheEntryList]
        distances.sort(key=lambda x: x[0])
        return distances[0][1]

class Ring:
    # TODO does not handle virtual nodes/replicas
    # TODO cacheCount should be abstracted better
    def __init__(self, hashFunction, cacheCount, ringCapacity):
        self.ringCapacity = ringCapacity
        self.hashFunction = hashFunction

        self.cacheEntryIndex = CacheEntryIndex()
        for _ in xrange(cacheCount):
            newCache = dict()
            # TODO what happens on a hash collision?
            self.cacheEntryIndex.addEntry(CacheEntry(newCache, self.hashFunction(newCache)%self.ringCapacity))

    def getHashForObjectKey(self, objectKey):
        return self.hashFunction(objectKey) % self.ringCapacity

    def put(self, objectKey, objectValue):
        hashedKey = self.getHashForObjectKey(objectKey)
        nearestCache = self.cacheEntryIndex.findNearestCacheEntry(hashedKey).cacheReference
        nearestCache[objectKey] = objectValue

    def get(self, objectKey):
        hashedKey = self.getHashForObjectKey(objectKey)
        nearestCache = self.cacheEntryIndex.findNearestCacheEntry(hashedKey).cacheReference
        return nearestCache[objectKey]


if __name__ == '__main__':
    hashFunction = lambda x: hash(x)
    ring = Ring(hashFunction, 5, 100)

    testKeys = [i for i in xrange(201)]

    for testKey in testKeys:
        ring.put(testKey, None)
