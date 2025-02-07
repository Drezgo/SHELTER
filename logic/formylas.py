# Аз ≤ Азф = 1,18 (Ky,i × Kn,i) × Kp × KN / (Ky,i + Kn,i)

# Аз ≤ Азф = 1,18 (Ky,i × Kn,i) × (Kзаб / Кбуд) × KN / (Ky,i + Kn,i)
# Kp = Kзаб / Кбуд
# KN = Min KN з таблиці шарів (напевно в бд шарів зберігати КИ і потім находити мін)
# Аз=А.1; Ку,Кп=Г.1; Кзаб=Г.2; Кбуд=Г.3; KN=Г.4

# АIV (1000)      (a4- самий слабий захист??)
# бетон, 10 см, (вологість 2)
# житлова, забор з бетону
# висота 8-10, щільність 10%, товщина забору 20 см, площа отворів 10%

results = {'Az': 1000, 'coefficients': [{'material': 'Сталь', 'thickness': 30, 'kn': 14.0, 'ky': 430.0}, {'material': 'Цегла', 'thickness': 35, 'kn': 24.0, 'ky': 10.0}, {'material': 'Бетон', 'thickness': 20, 'kn': 23.0, 'ky': 5.3}], 'coefficient_zab': 1.8, 'coefficient_bud': 0.1}

Az = results["Az"]
Kzab = results["coefficient_zab"]
Kbud = results["coefficient_bud"]

Ky = 1
for coeff in results["coefficients"]:
    Ky = Ky * coeff["ky"]

Kn = 1
for coeff in results["coefficients"]:
    Kn = Kn * coeff["kn"]

KN = 1.0

Azf = 1.18 * (Ky * Kn) * (Kzab / Kbud) * KN / (Ky + Kn)
print("Az: ", Az)
print("Azf: ", Azf)

# OLD
# Az = 1000
# Ky = 2
# Kn = 6.2

# Kzab = 1.0
# Kbud = 0.50

# KN = 1.4

# Azf = 1.18 * (Ky * Kn) * (Kzab / Kbud) * KN / (Ky + Kn)
# print("Az: ", Az)
# print(
#     Azf,
#     " = 1.18 * ",
#     "( ",
#     Ky,
#     " * ",
#     Kn,
#     ") * (",
#     Kzab,
#     " / ",
#     Kbud,
#     ") * ",
#     KN,
#     " / (",
#     Ky,
#     " + ",
#     Kn,
#     ")",
# )
# print("Azf: ", Azf)
# print("Az<=Azf", Az <= Azf)
