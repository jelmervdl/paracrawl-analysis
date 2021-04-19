import random
import warnings

class PopulationSizeWarning(Warning):
    pass

class RandomSample:
    def __init__(self, size):
        self.size = size
        self.n = 0
        self._sample = []
    
    def __iter__(self):
        if self.n < self.size:
            warnings.warn('Population (size {}) smaller than sample (size {})'.format(self.n + 1, self.size), PopulationSizeWarning)
        return iter(self._sample)
    
    def __getitem__(self, key):
        if self.n < self.size:
            warnings.warn('Population (size {}) smaller than sample (size {})'.format(self.n + 1, self.size), PopulationSizeWarning)
        return self._sample[key]
        
    def __len__(self):
        return len(self._sample)
    
    def add(self, item):
        if self.n < self.size:
            self._sample.append(item)
            self.n += 1
            if self.n == self.size:
                random.shuffle(self._sample)
        else:
            pos = random.randint(0, self.n)
            if pos < self.size:
                self._sample[pos] = item
            self.n += 1

    def update(self, items):
        for item in items:
            self.add(item)


