from random import randint

class perm:
    RIGHT_PERM_FIRST = False
    
    def __init__(self, array=[0]):
        self._array = array
        self._order = None
        self._id = None
    
    @property
    def length(self):
        return len(self._array)
    
    def isIdentity(self):
        arr = self._array
        for i in range(len(arr)):
            if arr[i] != i:
                return False
        return True
    
    def setOrder(self):
        order = 1
        arr = self._array
        length = len(arr)
        once = [True] * length
        for start in range(length):
            if once[start] and arr[start] != start:
                i = arr[start]
                cycle_len = 1
                while i != start:
                    cycle_len += 1
                    once[i] = False
                    i = arr[i]
                a, b = order, cycle_len
                while b:
                    a, b = b, a % b
                order = order * cycle_len // a
        self._order = order
    
    def setID(self):
        arr = self._array
        length = len(arr)
        factorial = 1
        ID = 0
        for i in range(2, length):
            factorial *= i
        once = [1] * length
        for i in range(length-1, 0, -1):
            ID += sum(once[arr[i]+1:]) * factorial
            once[arr[i]] = 0
            factorial //= i
        self._id = ID
    
    def order(self):
        if self._order is None:
            self.setOrder()
        return self._order
    
    def ID(self):
        if self._id is None:
            self.setID()
        return self._id
    
    def copy(self):
        obj = perm(self._array)
        obj._order = self._order
        obj._id = self._id
        return obj
    
    def distinct(self):
        arr = self._array
        dist = 0
        for i in range(len(arr)):
            if arr[i] != i:
                dist += 1
        return dist
    
    def __repr__(self):
        return f"array=[{','.join(map(str, self._array))}] length={self.length} order={self._order} id={self._id}"
    
    def __str__(self):
        arr = self._array
        once = [True] * len(arr)
        string = ""
        for start in range(len(arr)):
            if once[start] and arr[start] != start:
                string += "(" + str(start)
                i = arr[start]
                while i != start:
                    string += ", " + str(i)
                    once[i] = False
                    i = arr[i]
                string += ")"
        if string:
            return string
        else:
            return "e"
    
    def setInv(self, **kwargs):
        arrorig = self._array
        arrinv = list(arrorig)
        for i in range(len(arrorig)):
            arrinv[arrorig[i]] = i
        self._array = arrinv
        self._id = None
        if kwargs.get("fullset"):
            self.order()
            self.setID()
        else:
            if kwargs.get("setorder"):
                self.order()
            if kwargs.get("setid"):
                self.setID()
    
    def getInv(self, **kwargs):
        arrorig = self._array
        arrinv = list(arrorig)
        for i in range(len(arrorig)):
            arrinv[arrorig[i]] = i
        obj = perm(arrinv)
        obj._order = self._order
        if kwargs.get("fullset"):
            obj.order()
            obj.setID()
        else:
            if kwargs.get("setorder"):
                obj.order()
            if kwargs.get("setid"):
                obj.setID()
        return obj
    
    def setRandom(self, length=None, **kwargs):
        if length is None:
            length = self.length
        arr = [0] * length
        once = [1] * length
        for i in range(length):
            rand = randint(1, length - i)
            rand -= once[0]
            j = 0
            while rand:
                j += 1
                rand -= once[j]
            once[j] = 0
            arr[i] = j
        self._array = arr
        self._order = None
        self._id = None
        if kwargs.get("fullset"):
            self.setOrder()
            self.setID()
        else:
            if kwargs.get("setorder"):
                self.setOrder()
            if kwargs.get("setid"):
                self.setID()
    
    def __getitem__(self, key):
        return self._array[key]
    
    def __mul__(left, right):
        l, r = left._array, right._array
        llen, rlen = len(l), len(r)
        if llen < rlen:
            l = l + list(range(llen, rlen))
        else:
            r = r + list(range(rlen, llen))
            rlen = llen
        arr = list(r)
        if perm.RIGHT_PERM_FIRST:
            for i in range(rlen):
                arr[i] = l[r[i]]
        else:
            for i in range(rlen):
                arr[i] = r[l[i]]
        return perm(arr)
    
    def __imul__(left, right):
        l, r = left._array, right._array
        llen, rlen = len(l), len(r)
        if llen < rlen:
            l = l + list(range(llen, rlen))
        else:
            r = r + list(range(rlen, llen))
            rlen = llen
        arr = list(r)
        for i in range(rlen):
            arr[i] = r[l[i]]
        return perm(arr)
    
    def __pow__(self, power):
        if self._order is None:
            self.setOrder()
        order = self._order
        power = power % order
        if not power:
            obj = perm(list(range(self.length)))
            obj._order = 1
            obj._id = 0
            return obj
        if power > (order >> 1):
            power = order - power
            arrbuf = self._array
            arrorig = list(arrbuf)
            length = len(arrorig)
            for i in range(length):
                arrorig[arrbuf[i]] = i
            arr = list(arrorig)
        else:
            arrorig = self._array
            arr = list(arrorig)
            length = len(arr)
        i = 1
        while power >> i:
            i += 1
        i -= 2
        while i >= 0:
            arrbuf = list(arr)
            for j in range(length):
                arrbuf[j] = arr[arr[j]]
            arr = arrbuf
            if (power >> i) & 1:
                arrbuf = list(arr)
                for j in range(length):
                    arrbuf[j] = arr[arrorig[j]]
                arr = arrbuf
            i -= 1
        obj = perm(arr)
        a = order
        while power:
            a, power = power, a % power
        obj._order = order // a
        return obj
    
    __ipow__ = __pow__
    
    def __hash__(self):
        return (self.ID() * 1624152263628726963) % 2305843009213693951
    
    def __eq__(left, right):
        l, r = left._array, right._array
        llen, rlen = len(l), len(r)
        if llen < rlen:
            l, r = r, l
            llen, rlen = rlen, llen
        for i in range(rlen, llen):
            if l[i] != i:
                return False
        for i in range(rlen):
            if l[i] != r[i]:
                return False
        return True
    def __ne__(left, right):
        l, r = left._array, right._array
        llen, rlen = len(l), len(r)
        if llen < rlen:
            l, r = r, l
            llen, rlen = rlen, llen
        for i in range(rlen, llen):
            if l[i] != i:
                return True
        for i in range(rlen):
            if l[i] != r[i]:
                return True
        return False
    
    def __lt__(left, right):
        l, r = left._array, right._array
        llen, rlen = len(l), len(r)
        if llen == rlen:
            for i in range(llen-1, 0, -1):
                if l[i] != r[i]:
                    return l[i] > r[i]
            return False
        elif llen < rlen:
            for i in range(llen, rlen):
                if r[i] != i:
                    return True
            for i in range(llen-1, 0, -1):
                if l[i] != r[i]:
                    return l[i] > r[i]
            return False
        else:
            for i in range(rlen, llen):
                if l[i] != i:
                    return False
            for i in range(rlen-1, 0, -1):
                if l[i] != r[i]:
                    return l[i] > r[i]
            return False
    def __ge__(left, right):
        l, r = left._array, right._array
        llen, rlen = len(l), len(r)
        if llen == rlen:
            for i in range(llen-1, 0, -1):
                if l[i] != r[i]:
                    return l[i] < r[i]
            return True
        elif llen < rlen:
            for i in range(llen, rlen):
                if r[i] != i:
                    return False
            for i in range(llen-1, 0, -1):
                if l[i] != r[i]:
                    return l[i] < r[i]
            return True
        else:
            for i in range(rlen, llen):
                if l[i] != i:
                    return True
            for i in range(rlen-1, 0, -1):
                if l[i] != r[i]:
                    return l[i] < r[i]
            return True
    
    def __gt__(left, right):
        l, r = left._array, right._array
        llen, rlen = len(l), len(r)
        if llen == rlen:
            for i in range(llen-1, 0, -1):
                if l[i] != r[i]:
                    return l[i] < r[i]
            return False
        elif llen < rlen:
            for i in range(llen, rlen):
                if r[i] != i:
                    return False
            for i in range(llen-1, 0, -1):
                if l[i] != r[i]:
                    return l[i] < r[i]
            return False
        else:
            for i in range(rlen, llen):
                if l[i] != i:
                    return True
            for i in range(rlen-1, 0, -1):
                if l[i] != r[i]:
                    return l[i] < r[i]
            return False
    def __le__(left, right):
        l, r = left._array, right._array
        llen, rlen = len(l), len(r)
        if llen == rlen:
            for i in range(llen-1, 0, -1):
                if l[i] != r[i]:
                    return l[i] > r[i]
            return True
        elif llen < rlen:
            for i in range(llen, rlen):
                if r[i] != i:
                    return True
            for i in range(llen-1, 0, -1):
                if l[i] != r[i]:
                    return l[i] > r[i]
            return True
        else:
            for i in range(rlen, llen):
                if l[i] != i:
                    return False
            for i in range(rlen-1, 0, -1):
                if l[i] != r[i]:
                    return l[i] > r[i]
            return True

    @classmethod
    def fromArray(cls, *args, **kwargs):
        
        if not isinstance(args[0], int):
            args = args[0]
        arr = list(args)
        once = [True] * len(args)
        for i in args:
            assert once[i] and i >= 0, "Passed non-permutation list"
            once[i] = False
        if kwargs.get("length") and kwargs["length"] > len(arr):
            arr = arr + list(range(len(arr), kwargs["length"]))
        obj = cls(arr)
        if kwargs.get("fullset"):
            obj.setOrder()
            obj.setID()
        else:
            if kwargs.get("setorder"):
                obj.setOrder()
            if kwargs.get("setid"):
                obj.setID()
        return obj

    @classmethod
    def fromCycle(cls, *args, **kwargs):
        if not isinstance(args[0][0], int):
            args = args[0]
        arr = list(range(max(max(map(max, args))+1, kwargs.get("length", 0))))
        once = [True] * len(arr)
        for cycle in args:
            for i in range(-1, len(cycle)-1):
                assert once[cycle[i]] and cycle[i] >= 0, "Passed non-permutation list"
                once[cycle[i]] = False
                arr[cycle[i]] = cycle[i+1]
        obj = cls(arr)
        if kwargs.get("fullset"):
            obj.setOrder()
            obj.setID()
        else:
            if kwargs.get("setorder"):
                obj.setOrder()
            if kwargs.get("setid"):
                obj.setID()
        return obj

    @classmethod
    def fromPerm(cls, other):
        obj = cls(other._array)
        obj._order = other._order
        obj._id = other._id
        return obj

    @classmethod
    def fromID(cls, ID, length=0, **kwargs):
        factorial = 1
        if length:
            for i in range(2, length+1):
                factorial *= i
            ID %= factorial
        else:
            length = 1
            while factorial <= ID:
                length += 1
                factorial *= length
        factorial //= length
        arr = [0] * length
        once = [1] * length
        obj = cls()
        obj._id = ID
        for i in range(length-1, 0, -1):
            num, ID = divmod(ID, factorial)
            factorial //= i
            j = length-1
            num += 1 - once[j]
            while num:
                j -= 1
                num -= once[j]
            once[j] = 0
            arr[i] = j
        i = 0
        while not once[i]:
            i += 1
        arr[0] = i
        obj._array = arr
        if kwargs.get("setorder") or kwargs.get("fullset"):
            obj.setOrder()
        return obj

    @classmethod
    def getRandom(cls, length, **kwargs):
        arr = [0] * length
        once = [1] * length
        for i in range(length):
            rand = randint(1, length - i)
            rand -= once[0]
            j = 0
            while rand:
                j += 1
                rand -= once[j]
            once[j] = 0
            arr[i] = j
        obj = cls(arr)
        if kwargs.get("fullset"):
            obj.setOrder()
            obj.setID()
        else:
            if kwargs.get("setorder"):
                obj.setOrder()
            if kwargs.get("setid"):
                obj.setID()
        return obj

    @classmethod
    def getIdentity(cls, length):
        obj = cls(list(range(length)))
        obj._order = 1
        obj._id = 0
        return obj