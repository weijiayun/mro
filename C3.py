
class L(object):
    def __init__(self,child, *base):
        self.child = child
        self.base= list(base)
        self.containerL = []

    def addBase(self, l):
        if isinstance(l, L):
            if self.base:
                basesName = map(lambda x: x.getName(), self.base)
                if l.getName() not in basesName:
                    self.base.append(l)
            else:
                self.base.append(l)
        else:
            raise TypeError


    def getL(self):
        bases = self.getBase()
        self.containerL.append(self)
        while not self.isObject() and bases:
            tmp = []
            for l in bases:
                if isinstance(l, L):
                   tmp.append(l.getL())
                else:
                    tmp.append(l)
            bases = tmp
            bases = self.merge(bases)
            self.containerL.append(bases[0])
            bases = bases[1:]
        else:
            if bases:
                self.containerL=[self, self.base[0]]

        return self.containerL

    def getBase(self):
        return self.base

    def isObject(self):
        for lbase in self.base:
            if lbase.getName() != 'O':
                return False
        return True

    def __repr__(self):
        return r'L< "{0}" >'.format(self.child)

    __str__ = __repr__

    def merge(self, bases):
        flag = True
        for l in bases:
            if l[0].getName() != 'O':
                flag = False
        if flag:
            return bases[0]
        for i, lbase in enumerate(bases):
            flag = False
            header = lbase[0].getName()
            if header == 'O':
                continue
            for llbase in bases:
                if self.__isBase(llbase[1:], header):
                    if i == len(bases)-1:
                        raise Exception('wrong class')
                    else:
                        flag = True
                        break
            if not flag:
                headerl = bases[i][0]
                for j in range(len(bases)):
                    if bases[j][0].getName() == header:
                        del bases[j][0]
                return [headerl]+bases

    def __isBase(self, bases, header):
        for l in bases:
            if isinstance(l, L):
                if l.isBase(header) or l.getName() == header:
                    return True
        return False

    def getName(self):
        return self.child

    def isBase(self, baseName):
        flag = {'flag': False}
        if self.base:
            self.__find(self.base, baseName, flag)
        return flag['flag']

    def __find(self, bases, baseName, flag):
        for elem in bases:
            if elem.getName() == baseName:
                flag['flag'] = True
                break
            else:
                if elem.base:
                    self.__find(elem.base, baseName, flag)


def getRefOrder(A):
    topName = A[0]
    nodesBaseDict = A[1]
    nodesDict = {}
    O = L('O')

    for key, bases in nodesBaseDict.items():
        if key not in nodesDict:
            nodesDict[key] = L(key)
        if bases:
            for lname in bases:
                if lname not in nodesDict:
                    nodesDict[lname] = L(lname)
                nodesDict[key].addBase(nodesDict[lname])
        else:
            nodesDict[key].addBase(O)

    mroL = nodesDict[topName].getL()
    idDict = {}
    for i, l in enumerate(mroL[:-1][::-1]):
        idDict[l.getName()] = i + 1

    return idDict

if __name__ == '__main__':
    A = ['A', {'A': ['B', 'C'], 'B': ['D', 'E'], 'C': ['D', 'F'], 'E': [], 'F': [], 'D': []}]
    print getRefOrder(A)













