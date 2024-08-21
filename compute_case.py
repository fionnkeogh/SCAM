
Fc_max = 10
Fm_max = 10
Ic_1 = 1
Ic_2 = 2
Im_1 = 1
Im_2 = 2
Rc = 1
Rm = 1
S1 = 10
S2 = 5
Pm = 0.54

eq_21 = Pm*(Fm_max - Im_2 - Rm)
eq_22 = (1-Pm)*(Fc_max - Ic_2 - Rc)
eq_23 = Fm_max - Im_2
eq_24 = Fm_max - Im_1 - Rm - S2
eq_25 = Fc_max - Ic_2
eq_26 = Fm_max - Im_1 - S1
eq_27 = Fc_max - Ic_1

print("equation 2.1: " + str(eq_21))
print("equation 2.4: " + str(eq_24))
print(f'Im_1 + S1 < Im_2: {Im_1} + {S1} < {Im_2} == {str(Im_1 + S1 < Im_2)}')
print(f'Im_1 + S1 > Im_2: {Im_1} + {S1} > {Im_2} == {str(Im_1 + S1 > Im_2)}')

if Im_1 + S1 > Im_2 and eq_21 > eq_24:
    print("case 1")

if Im_1 + S1 < Im_2 and eq_21 < eq_24:
    print("case 2")

if Im_1 + S1 < Im_2 and eq_21 > eq_24:
    print("case 3")

if Im_1 + S1 > Im_2 and eq_21 < eq_24:
    print("case 4")