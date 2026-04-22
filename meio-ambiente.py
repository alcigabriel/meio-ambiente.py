import sqlite3

conexao = sqlite3.connect("meio_ambiente.db")
cursor = conexao.cursor()

cursor.execute("""
CREATE TABLE IF NOT EXISTS registros (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    tipo TEXT,
    valor REAL
)
""")

def adicionar_registro():
    print("\nTipos disponíveis:")
    print("1. Água (litros)")
    print("2. Energia (kWh)")
    print("3. Reciclagem (kg)")
    
    opcao = input("Escolha o tipo: ")
    
    if opcao == "1":
        tipo = "agua"
    elif opcao == "2":
        tipo = "energia"
    elif opcao == "3":
        tipo = "reciclagem"
    else:
        print("Tipo inválido!")
        return
    
    valor = float(input("Digite o valor: "))
    
    cursor.execute("INSERT INTO registros (tipo, valor) VALUES (?, ?)", (tipo, valor))
    conexao.commit()
    
    print("Registro salvo!")

def ver_historico():
    cursor.execute("SELECT * FROM registros")
    dados = cursor.fetchall()
    
    print("\n Histórico geral:")
    for d in dados:
        print(f"ID: {d[0]} | Tipo: {d[1]} | Valor: {d[2]}")

def calcular_media():
    tipo = input("Digite o tipo (agua, energia, reciclagem): ").lower()
    
    cursor.execute("SELECT AVG(valor) FROM registros WHERE tipo = ?", (tipo,))
    media = cursor.fetchone()[0]
    
    if media:
        print(f"\n Média de {tipo}: {media:.2f}")
        
        if tipo == "agua":
            if media > 150:
                print("Consumo alto de água!")
            else:
                print("Consumo de água OK!")
                
        elif tipo == "energia":
            if media > 200:
                print("Alto consumo de energia!")
            else:
                print("Consumo de energia controlado!")
                
        elif tipo == "reciclagem":
            if media < 5:
                print("Reciclagem baixa! Tente melhorar.")
            else:
                print("Boa reciclagem!")
                
    else:
        print("Nenhum dado encontrado.")

def resumo():
    print("\n Resumo geral:")

    for tipo in ["agua", "energia", "reciclagem"]:
        cursor.execute("SELECT AVG(valor) FROM registros WHERE tipo = ?", (tipo,))
        media = cursor.fetchone()[0]
        
        if media:
            print(f"{tipo.capitalize()}: {media:.2f}")
        else:
            print(f"{tipo.capitalize()}: sem dados")

def limpar_dados():
    confirmar = input("Tem certeza que deseja apagar todos os dados? (s/n): ")
    
    if confirmar.lower() == "s":
        cursor.execute("DELETE FROM registros")
        
        cursor.execute("DELETE FROM sqlite_sequence WHERE name='registros'")
        
        conexao.commit()
        print("Dados apagados e ID reiniciado!")
    else:
        print("Operação cancelada.")

def menu():
    while True:
        print("\n--- Sistema Ambiental ---")
        print("1. Adicionar registro")
        print("2. Ver histórico")
        print("3. Ver média por tipo")
        print("4. Ver resumo geral")
        print("5. Limpar dados")
        print("6. Sair")
        
        opcao = input("Escolha: ")
        
        if opcao == "1":
            adicionar_registro()
        elif opcao == "2":
            ver_historico()
        elif opcao == "3":
            calcular_media()
        elif opcao == "4":
            resumo()
        elif opcao == "5":
            limpar_dados()
        elif opcao == "6":
            print("Saindo...")
            break
        else:
            print("Opção inválida!")

menu()

conexao.close()