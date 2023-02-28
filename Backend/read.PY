from Func.Generar_Tabla import writeTruthTable  
from Func.Generar_Tabla2 import writeTruthTable2  

#writeTruthTable("P∨(Q →(R∧T))")
truthTable = writeTruthTable2("P∨(Q →(R∧T))")
for row in truthTable:
    print(row)