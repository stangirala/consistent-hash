from collections import namedtuple
import bisect

class Ring:
    def __init__(self, hashFn, replicas):
        self.hashFn = hashFn
        self.replicas = replicas

        self.keyList = []
        self.hashedKeyList = []

    def addKey(self, key):
        hashedKey = self.hashFn(key)
        for i in xrange(self.replicas):
            replicatedHashedKey = i + hashedKey
            insertPosition = bisect.bisect_left(self.keyList, replicatedHashedKey)
            self.hashedKeyList.insert(insertPosition, replicatedHashedKey)
            self.keyList.insert(insertPosition, key)

    def findKeyGTE(self, key):
        hashedKey = self.hashFn(key)
        nearestPos = bisect.bisect_left(self.hashedKeyList, hashedKey)
        if nearestPos != len(self.hashedKeyList):
            return self.keyList[nearestPos]
        return self.keyList[-1]
