class Iterateur:
    current = 0

    def __init__(self, stop):
        self.stop = stop

    def __iter__(self):
        return self

    def next(self):
        self.current += 1

        if self.current > self.stop:
            raise StopIteration

        if self.current == 5:
            print
            "Quoi déjà 5eme tour?"

        return self.current


# appel a l'iterateur
for i in Iterateur(10):
    print(i)
