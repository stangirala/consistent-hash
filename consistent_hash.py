from collections import namedtuple
import bisect

CacheEntry = namedtuple('hashedCacheReference', 'cacheReference')

class CacheEntryIndex:
    def __init__(self):
        self.hashedCacheReferenceList = []
        self.cacheReferenceList = []

    def addEntry(self, entry):
        insertPosition = bisect.bisect_left(self.hashedCacheReferenceList, entry.hashedCacheReference)
        self.hashedCacheReference.insert(insertPosition, entry.hashedCacheReference)
        self.cacheReferenceList.insert(insertPosition, entry.cacheReference)

    def findNearestCacheEntry(self, hashedCacheObject):
        nearestPosition = bisect.bisect_left(self.hashedCacheReferenceList, hashedCacheObject)
        if 0 <= i < len(self.hashedCacheReferenceList):
            return self.cacheReferenceList[i]
        else:
            return None

class Ring:
    # TODO does not handle virtual nodes/replicas
    # TODO cacheCount should be abstracted better
    # TODO add replicas
    def __init__(self, hashFunction, cacheCount, ringCapacity):
        self.ringCapacity = ringCapacity
        self.hashFunction = hashFunction

        self.cacheEntryIndex = CacheEntryIndex()
        for _ in xrange(cacheCount):
            newCache = dict()
            newCacheEntry = CacheEntry(newCache, self._getHashForObjectKey(newCache))
            self.cacheEntryIndex.addEntry(CacheEntry(newCacheEntry))

    def _getHashForObjectKey(self, objectKey):
        return self.hashFunction(objectKey) % self.ringCapacity

    def put(self, objectKey, objectValue):
        hashedKey = self._getHashForObjectKey(objectKey)
        nearestCache = self.cacheEntryIndex.findNearestCacheEntry(hashedKey)
        nearestCache[objectKey] = objectValue

    def get(self, objectKey):
        hashedKey = self._getHashForObjectKey(objectKey)
        nearestCache = self.cacheEntryIndex.findNearestCacheEntry(hashedKey)
        return nearestCache[objectKey]


if __name__ == '__main__':
    hashFunction = lambda x: hash(x)
    ring = Ring(hashFunction, 5, 100)

    testKeys = [i for i in xrange(201)]

    for testKey in testKeys:
        ring.put(testKey, None)
