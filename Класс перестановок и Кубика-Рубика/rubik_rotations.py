from copy import deepcopy
from permutation import perm

# U <-> D
# F <-> B
# R <-> L

# len = 8
cUFR, cUFL, cUBR, cUBL, cDFR, cDFL, cDBR, cDBL = range(8)
cURF, cULF, cURB, cULB, cDRF, cDLF, cDRB, cDLB = range(8)
cFUR, cFUL, cBUR, cBUL, cFDR, cFDL, cBDR, cBDL = range(8)
cFRU, cFLU, cBRU, cBLU, cFRD, cFLD, cBRD, cBLD = range(8)
cRUF, cLUF, cRUB, cLUB, cRDF, cLDF, cRDB, cLDB = range(8)
cRFU, cLFU, cRBU, cLBU, cRFD, cLFD, cRBD, cLBD = range(8)
decode_core_angle = {0: 'cUFR', 1: 'cUFL', 2: 'cUBR', 3: 'cUBL', 4: 'cDFR', 5: 'cDFL', 6: 'cDBR', 7: 'cDBL'}

# len = 12
cUF, cUR, cUB, cUL, cFR, cFL, cBR, cBL, cDF, cDR, cDB, cDL = range(12)
cFU, cRU, cBU, cLU, cRF, cLF, cRB, cLB, cFD, cRD, cBD, cLD = range(12)
decode_core_side = {0: 'cUF', 1: 'cUR', 2: 'cUB', 3: 'cUL', 4: 'cFR', 5: 'cFL',
                    6: 'cBR', 7: 'cBL', 8: 'cDF', 9: 'cDR', 10: 'cDB', 11: 'cDL'}

# len = 24
UFR, UFL, UBR, UBL, FUR, FUL, FDR, FDL, RUF, RUB, RDF, RDB = range(12)
DFR, DFL, DBR, DBL, BUR, BUL, BDR, BDL, LUF, LUB, LDF, LDB = range(12, 24)
URF, ULF, URB, ULB, FRU, FLU, FRD, FLD, RFU, RBU, RFD, RBD = range(12)
DRF, DLF, DRB, DLB, BRU, BLU, BRD, BLD, LFU, LBU, LFD, LBD = range(12, 24)
decode_angle = {0: 'UFR', 1: 'UFL', 2: 'UBR', 3: 'UBL', 4: 'FUR', 5: 'FUL', 6: 'FDR', 7: 'FDL',
                8: 'RUF', 9: 'RUB', 10: 'RDF', 11: 'RDB', 12: 'DFR', 13: 'DFL', 14: 'DBR', 15: 'DBL',
                16: 'BUR', 17: 'BUL', 18: 'BDR', 19: 'BDL', 20: 'LUF', 21: 'LUB', 22: 'LDF', 23: 'LDB'}

# len = 24
UF, UR, UB, UL, FU, FR, FD, FL, RU, RF, RD, RB = range(12)
DF, DR, DB, DL, BU, BR, BD, BL, LU, LF, LD, LB = range(12, 24)
decode_side = {0: 'UF', 1: 'UR', 2: 'UB', 3: 'UL', 4: 'FU', 5: 'FR', 6: 'FD', 7: 'FL',
               8: 'RU', 9: 'RF', 10: 'RD', 11: 'RB', 12: 'DF', 13: 'DR', 14: 'DB', 15: 'DL',
               16: 'BU', 17: 'BR', 18: 'BD', 19: 'BL', 20: 'LU', 21: 'LF', 22: 'LD', 23: 'LB'}

# len = 6
UUU, FFF, RRR, DDD, BBB, LLL = range(6)
decode_center = {0: 'UUU', 1: 'FFF', 2: 'RRR', 3: 'DDD', 4: 'BBB', 5: 'LLL'}

class rubik:
    def __init__(self, stringlist, core_angle, core_side, angle, side, center):
        self._array = [deepcopy(stringlist), core_angle.copy(), core_side.copy(), angle.copy(), side.copy(), center.copy()]
    
    def __str__(self):
        aa = self._array[0]
        if not aa:
            return "Identity"
        def list_to_str(ll):
            if isinstance(ll[0], str):
                string = ll[0]
            else:
                string = "(" + list_to_str(ll[0][0]) + ")^" + str(ll[0][1])
            for ss in ll[1:]:
                if isinstance(ss, str):
                    string += " " + ss
                else:
                    string += " (" + list_to_str(ss[0]) + ")^" + str(ss[1])
            return string
        return list_to_str(aa)
    
    def __repr__(self):
        aa = self._array
        ss = str(self) + "\nCore angle: "
        buf = str(aa[1])
        for i in range(8):
            buf = buf.replace(str(i), decode_core_angle[i])
        ss += buf + "\n Core side: "
        buf = str(aa[2])
        for i in range(11, -1, -1):
            buf = buf.replace(str(i), decode_core_side[i])
        ss += buf + "\n     Angle: "
        buf = str(aa[3])
        for i in range(23, -1, -1):
            buf = buf.replace(str(i), decode_angle[i])
        ss += buf + "\n      Side: "
        buf = str(aa[4])
        for i in range(23, -1, -1):
            buf = buf.replace(str(i), decode_side[i])
        ss += buf + "\n    Center: "
        buf = str(aa[5])
        for i in range(6):
            buf = buf.replace(str(i), decode_center[i])
        ss += buf
        ss = ss.replace(")(", ") (")
        ss = ss.replace(", ", ",")
        return ss
    
    def __len__(self):
        def getLength(ll):
            length = 0
            for item in ll:
                if isinstance(item, str):
                    length += 1
                else:
                    length += getLength(item[0]) * item[1]
            return length
        return getLength(self._array[0])
    
    def __mul__(self, other):
        aa, bb = self._array, other._array
        return rubik(deepcopy(aa[0]+bb[0]), aa[1]*bb[1], aa[2]*bb[2], aa[3]*bb[3], aa[4]*bb[4], aa[5]*bb[5])
    
    def __pow__(self, p):
        aa = self._array
        if aa[0]:
            aaa = [(deepcopy(aa[0]), p)]
        else:
            aaa = []
        return rubik(aaa, aa[1]**p, aa[2]**p, aa[3]**p, aa[4]**p, aa[5]**p)
    
    def __eq__(self, other):
        aa, bb = self._array, other._array
        if aa[1] != bb[1]:
            return False
        if aa[2] != bb[2]:
            return False
        if aa[3] != bb[3]:
            return False
        if aa[4] != bb[4]:
            return False
        if aa[5] != bb[5]:
            return False
        return True
    
    def __ne__(self, other):
        aa, bb = self._array, other._array
        if aa[1] != bb[1]:
            return True
        if aa[2] != bb[2]:
            return True
        if aa[3] != bb[3]:
            return True
        if aa[4] != bb[4]:
            return True
        if aa[5] != bb[5]:
            return True
        return False
    
    def __bool__(self):
        return True
    
    __imul__ = __mul__
    __ipow__ = __pow__
    
    def copy(self):
        aa = self._array
        return rubik(deepcopy(aa[0]), aa[1].copy(), aa[2].copy(), aa[3].copy(), aa[4].copy(), aa[5].copy())
    
    def getInv(self):
        aa = self._array
        strarr = deepcopy(aa[0])
        def do_reverse(ll):
            ll.reverse()
            for i in range(len(ll)):
                if isinstance(ll[i], str):
                    if len(ll[i]) == 1:
                        ll[i] = ll[i].swapcase()
                else:
                    do_reverse(ll[i][0])
        do_reverse(strarr)
        return rubik(strarr, aa[1].getInv(), aa[2].getInv(), aa[3].getInv(), aa[4].getInv(), aa[5].getInv())
    
    def setInv(self):
        aa = self._array
        def do_reverse(ll):
            ll.reverse()
            for i in range(len(ll)):
                if isinstance(ll[i], str):
                    if len(ll[i]) == 1:
                        ll[i] = ll[i].swapcase()
                else:
                    do_reverse(ll[i][0])
        do_reverse(aa[0])
        aa[1].setInv()
        aa[2].setInv()
        aa[3].setInv()
        aa[4].setInv()
        aa[5].setInv()
    
    def getNorm(self):
        return self * _norm_dict[self._array[5]]
    
    def setNorm(self):
        arr = self._array
        brr = (self * _norm_dict[self._array[5]])._array
        arr[0] = brr[0]
        arr[1] = brr[1]
        arr[2] = brr[2]
        arr[3] = brr[3]
        arr[4] = brr[4]
        arr[5] = brr[5]
    
    def getReflect(self, orient):
        aa = self._array
        # U, D, E
        if orient in "Zz":
            strlist = _reflect_opers(aa[0], "UuDd", "Ee")
            perm1 = aa[1] * perm.fromCycle([cUFR, cDFR], [cUFL, cDFL], [cUBR, cDBR], [cUBL, cDBL])
            perm2 = aa[2] * perm.fromCycle([cUF, cDF], [cUB, cDB], [cUR, cDR], [cUL, cDL])
            perm3 = aa[3] * perm.fromCycle([UFR, DFR], [UFL, DFL], [UBR, DBR], [UBL, DBL],
                                          [FUR, FDR], [FUL, FDL], [BUR, BDR], [BUL, BDL],
                                          [RUF, RDF], [LUF, LDF], [RUB, RDB], [LUB, LDB])
            perm4 = aa[4] * perm.fromCycle([UF, DF], [UB, DB], [UR, DR], [UL, DL], [FU, FD], [BU, BD], [RU, RD], [LU, LD])
            perm5 = aa[5] * perm.fromCycle([UUU, DDD])
        # R M L
        elif orient in "Yy":
            strlist = _reflect_opers(aa[0], "RrLl", "Mm")
            perm1 = aa[1] * perm.fromCycle([cRFU, cLFU], [cRFD, cLFD], [cRBU, cLBU], [cRBD, cLBD])
            perm2 = aa[2] * perm.fromCycle([cRF, cLF], [cRB, cLB], [cRU, cLU], [cRD, cLD])
            perm3 = aa[3] * perm.fromCycle([RFU, LFU], [RFD, LFD], [RBU, LBU], [RBD, LBD],
                                          [FRU, FLU], [FRD, FLD], [BRU, BLU], [BRD, BLD],
                                          [URF, ULF], [DRF, DLF], [URB, ULB], [DRB, DLB])
            perm4 = aa[4] * perm.fromCycle([RF, LF], [RB, LB], [RU, LU], [RD, LD], [FR, FL], [BR, BL], [UR, UL], [DR, DL])
            perm5 = aa[5] * perm.fromCycle([RRR, LLL])
        # F B S
        else:
            strlist = _reflect_opers(aa[0], "FfBb", "Ss")
            perm1 = aa[1] * perm.fromCycle([cFUR, cBUR], [cFUL, cBUL], [cFDR, cBDR], [cFDL, cBDL])
            perm2 = aa[2] * perm.fromCycle([cFU, cBU], [cFD, cBD], [cFR, cBR], [cFL, cBL])
            perm3 = aa[3] * perm.fromCycle([FUR, BUR], [FUL, BUL], [FDR, BDR], [FDL, BDL],
                                          [UFR, UBR], [UFL, UBL], [DFR, DBR], [DFL, DBL],
                                          [RFU, RBU], [LFU, LBU], [RFD, RBD], [LFD, LBD])
            perm4 = aa[4] * perm.fromCycle([FU, BU], [FD, BD], [FR, BR], [FL, BL], [UF, UB], [DF, DB], [RF, RB], [LF, LB])
            perm5 = aa[5] * perm.fromCycle([FFF, BBB])
        return rubik(strlist, perm1, perm2, perm3, perm4, perm5)
    
    def setReflect(self, orient):
        aa = self._array
        # U, D, E
        if orient in "Zz":
            aa[0] = _reflect_opers(aa[0], "UuDd", "Ee")
            aa[1] *= perm.fromCycle([cUFR, cDFR], [cUFL, cDFL], [cUBR, cDBR], [cUBL, cDBL])
            aa[2] *= perm.fromCycle([cUF, cDF], [cUB, cDB], [cUR, cDR], [cUL, cDL])
            aa[3] *= perm.fromCycle([UFR, DFR], [UFL, DFL], [UBR, DBR], [UBL, DBL],
                                          [FUR, FDR], [FUL, FDL], [BUR, BDR], [BUL, BDL],
                                          [RUF, RDF], [LUF, LDF], [RUB, RDB], [LUB, LDB])
            aa[4] *= perm.fromCycle([UF, DF], [UB, DB], [UR, DR], [UL, DL], [FU, FD], [BU, BD], [RU, RD], [LU, LD])
            aa[5] *= perm.fromCycle([UUU, DDD])
        # R M L
        elif orient in "Yy":
            aa[0] = _reflect_opers(aa[0], "RrLl", "Mm")
            aa[1] *= perm.fromCycle([cRFU, cLFU], [cRFD, cLFD], [cRBU, cLBU], [cRBD, cLBD])
            aa[2] *= perm.fromCycle([cRF, cLF], [cRB, cLB], [cRU, cLU], [cRD, cLD])
            aa[3] *= perm.fromCycle([RFU, LFU], [RFD, LFD], [RBU, LBU], [RBD, LBD],
                                          [FRU, FLU], [FRD, FLD], [BRU, BLU], [BRD, BLD],
                                          [URF, ULF], [DRF, DLF], [URB, ULB], [DRB, DLB])
            aa[4] *= perm.fromCycle([RF, LF], [RB, LB], [RU, LU], [RD, LD], [FR, FL], [BR, BL], [UR, UL], [DR, DL])
            aa[5] *= perm.fromCycle([RRR, LLL])
        # F B S
        else:
            aa[0] = _reflect_opers(aa[0], "FfBb", "Ss")
            aa[1] *= perm.fromCycle([cFUR, cBUR], [cFUL, cBUL], [cFDR, cBDR], [cFDL, cBDL])
            aa[2] *= perm.fromCycle([cFU, cBU], [cFD, cBD], [cFR, cBR], [cFL, cBL])
            aa[3] *= perm.fromCycle([FUR, BUR], [FUL, BUL], [FDR, BDR], [FDL, BDL],
                                          [UFR, UBR], [UFL, UBL], [DFR, DBR], [DFL, DBL],
                                          [RFU, RBU], [LFU, LBU], [RFD, RBD], [LFD, LBD])
            aa[4] *= perm.fromCycle([FU, BU], [FD, BD], [FR, BR], [FL, BL], [UF, UB], [DF, DB], [RF, RB], [LF, LB])
            aa[5] *= perm.fromCycle([FFF, BBB])
    
    def __getitem__(self, key):
        if len(key) == 4:
            return decode_core_angle[self._array[1][eval(key)]]
        elif key[0] == "c":
            return decode_core_side[self._array[2][eval(key)]]
        elif len(key) == 2:
            return decode_side[self._array[4][eval(key)]]
        elif key[0] != key[2]:
            return decode_angle[self._array[3][eval(key)]]
        else:
            return decode_center[self._array[5][eval(key)]]
    
    def opers(self):
        return deepcopy(self._array[0])
    
    def coreAngle(self):
        return self._array[1].copy()
    
    def coreSide(self):
        return self._array[2].copy()
    
    def angle(self):
        return self._array[3].copy()
    
    def side(self):
        return self._array[4].copy()
    
    def center(self):
        return self._array[5].copy()


# OPERATIONS
U = rubik(["U"],
    perm.fromCycle([cUFR, cUFL, cUBL, cUBR], length=8, fullset=True),
    perm.fromCycle([cUF, cUL, cUB, cUR], length=12, fullset=True),
    perm.fromCycle([UFR, UFL, UBL, UBR], [FUR, LUF, BUL, RUB], [FUL, LUB, BUR, RUF], length=24, fullset=True),
    perm.fromCycle([UF, UL, UB, UR], [FU, LU, BU, RU], length=24, fullset=True),
    perm.getIdentity(6) )

D = rubik(["D"],
    perm.fromCycle([cDFR, cDBR, cDBL, cDFL], length=8, fullset=True),
    perm.fromCycle([cDF, cDR, cDB, cDL], length=12, fullset=True),
    perm.fromCycle([DFR, DBR, DBL, DFL], [FDR, RDB, BDL, LDF], [FDL, RDF, BDR, LDB], length=24, fullset=True),
    perm.fromCycle([DF, DR, DB, DL], [FD, RD, BD, LD], length=24, fullset=True),
    perm.getIdentity(6) )

F = rubik(["F"],
    perm.fromCycle([cFUR, cFDR, cFDL, cFUL], length=8, fullset=True),
    perm.fromCycle([cFU, cFR, cFD, cFL], length=12, fullset=True),
    perm.fromCycle([FUR, FDR, FDL, FUL], [UFR, RFD, DFL, LFU], [RFU, DFR, LFD, UFL], length=24, fullset=True),
    perm.fromCycle([FU, FR, FD, FL], [UF, RF, DF, LF], length=24, fullset=True),
    perm.getIdentity(6) )

B = rubik(["B"],
    perm.fromCycle([cBUR, cBUL, cBDL, cBDR], length=8, fullset=True),
    perm.fromCycle([cBU, cBL, cBD, cBR], length=12, fullset=True),
    perm.fromCycle([BUR, BUL, BDL, BDR], [UBR, LBU, DBL, RBD], [RBU, UBL, LBD, DBR], length=24, fullset=True),
    perm.fromCycle([BU, BL, BD, BR], [UB, LB, DB, RB], length=24, fullset=True),
    perm.getIdentity(6) )

R = rubik(["R"],
    perm.fromCycle([cRUF, cRUB, cRDB, cRDF], length=8, fullset=True),
    perm.fromCycle([cRF, cRU, cRB, cRD], length=12, fullset=True),
    perm.fromCycle([RUF, RUB, RDB, RDF], [URF, BRU, DRB, FRD], [FRU, URB, BRD, DRF], length=24, fullset=True),
    perm.fromCycle([RU, RB, RD, RF], [UR, BR, DR, FR], length=24, fullset=True),
    perm.getIdentity(6) )

L = rubik(["L"],
    perm.fromCycle([cLUF, cLDF, cLDB, cLUB], length=8, fullset=True),
    perm.fromCycle([cLF, cLD, cLB, cLU], length=12, fullset=True),
    perm.fromCycle([LUF, LDF, LDB, LUB], [ULF, FLD, DLB, BLU], [FLU, DLF, BLD, ULB], length=24, fullset=True),
    perm.fromCycle([LU, LF, LD, LB], [UL, FL, DL, BL], length=24, fullset=True),
    perm.getIdentity(6) )

M = rubik(["M"],
    perm.getIdentity(8),
    perm.fromCycle([cUF, cUB, cDB, cDF], length=12, fullset=True),
    perm.getIdentity(24),
    perm.fromCycle([UF, BU, DB, FD], [FU, UB, BD, DF], length=24, fullset=True),
    perm.fromCycle([UUU, BBB, DDD, FFF], length=6, fullset=True) )

S = rubik(["S"],
    perm.getIdentity(8),
    perm.fromCycle([cUL, cUR, cDR, cDL], length=12, fullset=True),
    perm.getIdentity(24),
    perm.fromCycle([UL, RU, DR, LD], [LU, UR, RD, DL], length=24, fullset=True),
    perm.fromCycle([UUU, RRR, DDD, LLL], length=6, fullset=True) )

E = rubik(["E"],
    perm.getIdentity(8),
    perm.fromCycle([cFR, cFL, cBL, cBR], length=12, fullset=True),
    perm.getIdentity(24),
    perm.fromCycle([FR, LF, BL, RB], [RF, FL, LB, BR], length=24, fullset=True),
    perm.fromCycle([FFF, LLL, BBB, RRR], length=6, fullset=True) )

I = rubik([],
    perm.getIdentity(8),
    perm.getIdentity(12),
    perm.getIdentity(24),
    perm.getIdentity(24),
    perm.getIdentity(6) )

U2 = U*U
D2 = D*D
F2 = F*F
B2 = B*B
R2 = R*R
L2 = L*L
U2._array[0] = ["U2"]
D2._array[0] = ["D2"]
F2._array[0] = ["F2"]
B2._array[0] = ["B2"]
R2._array[0] = ["R2"]
L2._array[0] = ["L2"]

u = U2*U
d = D2*D
f = F2*F
b = B2*B
r = R2*R
l = L2*L
u._array[0] = ["u"]
d._array[0] = ["d"]
f._array[0] = ["f"]
b._array[0] = ["b"]
r._array[0] = ["r"]
l._array[0] = ["l"]

M2 = M*M
S2 = S*S
E2 = E*E
M2._array[0] = ["M2"]
S2._array[0] = ["S2"]
E2._array[0] = ["E2"]

m = M2*M
s = S2*S
e = E2*E
m._array[0] = ["m"]
s._array[0] = ["s"]
e._array[0] = ["e"]

X = F*S*b
Y = R*M*l
Z = U*E*d
X._array[0] = ["X"]
Y._array[0] = ["Y"]
Z._array[0] = ["Z"]

X2 = X*X
Y2 = Y*Y
Z2 = Z*Z
X2._array[0] = ["X2"]
Y2._array[0] = ["Y2"]
Z2._array[0] = ["Z2"]

x = X2*X
y = Y2*Y
z = Z2*Z
x._array[0] = ["x"]
y._array[0] = ["y"]
z._array[0] = ["z"]

_norm_dict = dict()
for op1 in [I, z, Z2, Z]:
    for op2 in [I, z, Z2, Z, y, Y2, Y, x, X2, X]:
        opop = op1 * op2
        if _norm_dict.get(opop._array[5]):
            if len(_norm_dict[opop._array[5]]._array[0]) > len(opop.getInv()._array[0]):
                _norm_dict[opop._array[5]].append(opop.getInv())
        else:
            _norm_dict[opop._array[5]] = opop.getInv()

basOpers = [U, U2, u, D, D2, d, F, F2, f, B, B2, b, R, R2, r, L, L2, l]
advOpers = [U, U2, u, D, D2, d, F, F2, f, B, B2, b, R, R2, r, L, L2, l, M, M2, m, S, S2, s, E, E2, e]
def sameKind(op1, op2):
    return (ord(op1._array[0][0][0]) - ord(op2._array[0][0][0])) in {-32, 0, 32}

def _reflect_opers(ll, baslet, advlet):
    newllll = deepcopy(ll)
    def _reflect_wrapper(newll):
        for ii in range(len(newll)):
            if isinstance(newll[ii], str):
                cc = newll[ii]
                if cc[0] in baslet:
                    if len(cc) == 2:
                        newll[ii] = baslet[2*(cc[0] == baslet[0])] + "2"
                    else:
                        newll[ii] = baslet[3 - baslet.find(cc)]
                elif cc[0] not in advlet and len(cc) == 1:
                    newll[ii] = cc.swapcase()
            else:
                _reflect_wrapper(newll[ii][0])
    _reflect_wrapper(newllll)
    return newllll