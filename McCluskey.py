import numpy as np
from sympy import *




Notation = ["Z_2", "Z_1", "Z_0", "T"]
lookupTable = np.array([0,0,0,1,1,0,1,1,2,2,2,2,1,1,1,1])



Notation.reverse()
EV = 10
x0, x1, x2, x3, x4, x5, x6, x7, x8, x9 = symbols('x_0 x_1 x_2 x_3 x_4 x_5 x_6 x_7 x_8 x_9')

TableSize = [0] * pow(2,EV)
Menge_1_cache = np.array(TableSize)
Menge_0_cache = np.array(TableSize)

x_1 = 0
x_0 = 0
c = 0
for n in lookupTable:
    if n == 1:
        Menge_1_cache[x_1] = c
        x_1 += 1
    elif n == 0:
        Menge_0_cache[x_0] = c
        x_0 += 1
    c += 1

TableSize = [0] * x_1
Menge_1 = np.array(TableSize)

TableSize = [0] * x_0
Menge_0 = np.array(TableSize)

c = 0
for n in Menge_1:
    Menge_1[c] = Menge_1_cache[c]
    c += 1

c = 0
for n in Menge_0:
    Menge_0[c] = Menge_0_cache[c]
    c += 1

print("M1")
print(Menge_1)

print("M0")
print(Menge_0)

TableSize = [0] * x_0
M0_Kern_cache = np.array(TableSize)

c_1 = 0
c_0 = 0
temp_primterm = ''
temp_kern = 0
Kern_gefunden = 0

TableSize = [0] * EV
temp_bit_register = np.array(TableSize)

bit_counter = 0
output = ''

def printCore(xored_val): 
    for n in range(EV):
        if xored_val == pow(2, n):
            print()
            print("Kern gefunden in M1(" + str(c_1 + 1) + ") und M0(" + str(c_0 + 1) + ") mit Bit " + str(np.int0(np.log2(xored_val))))
            return 1

def bitCore(xored_val):
    for n in range(EV):
        bitposDec = pow(2, n)
        if xored_val == bitposDec:
            if Menge_1[c_1] & bitposDec == bitposDec:
                print("Kern: x" +str(n))
                temp_primterm_def = 'x' + str(n)
                temp_kern_def = bitposDec
            else:
                print("Kern: ~x" + str(n))
                temp_primterm_def = '~x' + str(n)
                temp_kern_def = 0
            return (temp_primterm_def, temp_kern_def)

def getRawPrimString(xored_val, core_term):
    core_term += '&('
    for n in range(EV):
        bitposDec = pow(2, n)
        if xored_val & bitposDec == bitposDec:
            if Menge_1[c_1] & bitposDec == bitposDec:
                core_term += 'x' + str(n) + '|'
            else:
                core_term += '~x' + str(n) + '|'

    core_term = core_term.rstrip(core_term[-1])
    core_term += ')'
    return core_term

for n in Menge_1:
    for m in Menge_0:

        if Menge_1[c_1] >= 0:
            temp = Menge_1[c_1] ^ Menge_0[c_0]

            Kern_gefunden = 0
            Kern_gefunden = printCore(temp)

            if Kern_gefunden:
                temp_primterm, temp_kern = bitCore(temp)

            if Kern_gefunden:
                c = 0
                for n in Menge_0:
                    if n & temp == temp_kern:
                        M0_Kern_cache[c] = n
                        c += 1

                if c == 0:
                    print("Keine Übereinstimmungen in M0, Primterm ist Kern.")
                    f = false
                else: 
                    for n in range(c):
                        temp = M0_Kern_cache[n] ^ Menge_1[c_1]
                        temp_primterm = getRawPrimString(temp, temp_primterm)
                    f = true

                if f: print("Berechneter Primterm (ungekürzt): ", temp_primterm)
                temp_primterm_simp = simplify(temp_primterm)
                print("Berechneter Primterm: ", temp_primterm_simp)
                output += ' (' + str(temp_primterm_simp) + ') |'

                c = 0
                for n in Menge_1:
                    
                    if n >= 0:

                        for m in temp_bit_register:
                            temp_bit_register[bit_counter] = (Menge_1[c] & pow(2, bit_counter)) >> bit_counter
                            bit_counter += 1
                        bit_counter = 0

                        x0_subs = temp_bit_register[0]
                        x1_subs = temp_bit_register[1]
                        x2_subs = temp_bit_register[2]
                        x3_subs = temp_bit_register[3]
                        x4_subs = temp_bit_register[4]
                        x5_subs = temp_bit_register[5]
                        x6_subs = temp_bit_register[6]
                        x7_subs = temp_bit_register[7]
                        x8_subs = temp_bit_register[8]
                        x9_subs = temp_bit_register[9]

                        p = eval(temp_primterm).subs({x0: x0_subs, x1: x1_subs, x2: x2_subs, x3: x3_subs, x4: x4_subs, x5: x5_subs, x6: x6_subs, x7: x7_subs,
                        	x8: x8_subs, x9: x9_subs})
                        if p:
                            Menge_1[c] = -1

                    c += 1

        else:
            break
        c_0 += 1
    c_1 += 1
    c_0 = 0

output = output.rstrip(output[-1])
print()
print(output)
print()
output_rep = output
for n, Sym in enumerate(Notation):
        output_rep = output_rep.replace('x' + str(n), Sym)
print(output_rep)
print()
