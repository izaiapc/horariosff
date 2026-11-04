import pandas as pd

# Formato ideal de Banco de Dados: Linhas independentes com chaves únicas
dados_base = [
    {"turma": "Turma A", "dia": "Segunda", "horario": "07:30 - 08:20", "disciplina": "Matemática"},
    {"turma": "Turma A", "dia": "Segunda", "horario": "08:20 - 09:10", "disciplina": "Matemática"},
    {"turma": "Turma A", "dia": "Terça",   "horario": "09:30 - 10:20", "disciplina": "História"},
    {"turma": "Turma A", "dia": "Sexta",   "horario": "10:20 - 11:10", "disciplina": "Português"},
    
    {"turma": "Turma B", "dia": "Segunda", "horario": "07:30 - 08:20", "disciplina": "História"},
    {"turma": "Turma B", "dia": "Terça",   "horario": "08:20 - 09:10", "disciplina": "Português"},
    {"turma": "Turma B", "dia": "Quarta",  "horario": "09:30 - 10:20", "disciplina": "Matemática"},
    {"turma": "Turma B", "dia": "Quarta",  "horario": "10:20 - 11:10", "disciplina": "Matemática"},
]

df_csv = pd.DataFrame(dados_base)
df_csv.to_csv("horarios_escolares.csv", index=False)
print("Arquivo 'horarios_escolares.csv' gerado com sucesso!")
