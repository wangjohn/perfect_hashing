import math
import random

class PerfectHash:
    def __init__(self, n=20):
        self.n = n
        self.upper = [False for i in xrange(self.n)]
        self.lower = [[] for i in xrange(self.n)]
        self.top_level_hash = UniversalHash(self.n)
        self.lower_level_hashes = [UniversalHash(4) for i in xrange(self.n)]

    def reset_hashes(self):
        self.top_level_hash.reset_hash(self.n)
        self.lower_level_hashes = [UniversalHash() for i in xrange(self.n)]

    def rehash_top_level(self):
        self.n = self.n*2
        new_lower = [[] for i in xrange(self.n)]
        self.reset_hashes()
        for i in xrange(len(self.lower)):
           for j in xrange(len(self.lower[i])):
               item = self.lower[i]
               top_bucket = self.top_level_hash.get_hashed_value(item.key)
               self.upper[top_bucket] = True
               new_lower[top_bucket].append(item)

        self.lower = [[] for i in xrange(self.n)]
        for i in xrange(len(new_lower)):
            self.reconstruct_bottom_level(i, new_lower[i])

    def reconstruct_bottom_level(self, i, old_items=False):
        if not old_items:
            old_items = [item for item in self.lower[i] if item]
        secondary_hash = self.lower_level_hashes[i]
        previous_size = secondary_hash.n
        secondary_hash.reset_hash(4*previous_size**2)
        new_bucket = [False for i in xrange(4*previous_size**2)]
        for item in old_items:
            new_bucket[secondary_hash.get_hashed_value(item.key)] = item
        self.lower[i] = new_bucket

    def find(self, item):
        top_bucket = self.top_level_hash.get_hashed_value(item.key)
        return self.lower[top_bucket][self.lower_level_hashes.get_hashed_value(item.key)]

    def insert(self, item):
        top_bucket = self.top_level_hash.get_hashed_value(item.key)
        secondary_bucket = self.lower_level_hashes[top_bucket].get_hashed_value(item.key)
        old_item = self.lower[top_bucket][secondary_bucket]
        if old_item:
            self.lower[top_bucket].append(item)
            self.reconstruct_bottom_level(top_bucket)
        else:
            self.lower[top_bucket][secondary_bucket] = item
        
    def delete(self, item):
        top_bucket = self.top_level_hash.get_hashed_value(item.key)
        self.lower[top_bucket][self.lower_level_hashes.get_hashed_value(item.key)] = False

class UniversalHash:
    def __init__(self, n=20):
        self.n = n
        self.reset_hash()

    def get_hashed_value(self, key):
        return (self.a * key + self.b % self.p) % self.n

    def reset_hash(self, size=self.n):
        self.n = size
        self.p = self.pick_prime(self.n)
        self.a = random.randrange(1, self.p)
        self.b = random.randrange(1, self.p)

    def pick_prime(self, n):
        primes_list = [True for i in xrange(2*n+1)]
        primes_list[0] = primes_list[1] = False
    
        for (i, isprime) in enumerate(primes_list):
            if isprime:
                if i > n:
                    return i
                for j in xrange(i**2, 2*n+1, i):
                    primes_list[j] = False
        return None


if __name__ == '__main__':
    h = UniversalHash(50)
    print h.get_hashed_value(223420)



                
