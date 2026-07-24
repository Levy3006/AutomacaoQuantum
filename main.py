from testelogo import print_banner
from fluxoV2 import automacao_quantum 
import time
from classesInvestimentos import classes
from classesInvestimentos import tela_lista_e_seleciona_categorias
#from classesInput import classesinput
import json
import pwinput
from rich.console import Console
console = Console()

antes = time.time()

# =========== Fluxo de Macro Operações =============
print_banner("Quantum  Axis")
with open('credenciais.json', 'r') as f:
    credenciais = json.load(f)


credenciais['user'] = str(input('Email: '))
credenciais['senha'] = pwinput.pwinput(prompt="Senha: ", mask="*")

print("Credenciais Coletadas!")

data = input("Insira uma data sem caracteres (DDMMAAAA): ")
while not(len(data) == 8 and data.isdigit()):
    print("Formato inválido. Digite exatamente 8 números.")
    data = input("Insira uma data sem caracteres (DDMMAAAA): ")

classes = tela_lista_e_seleciona_categorias(classes)    
#print(classes)
#classes = classesinput

cont = 0
for classeDict in classes:
    
    def mainFunction(classe,user,password,data):
        global cont
    
        try:
            print(f"=================================== {str(list(classe.keys())[0]).upper()} ===================================")
            automacao_quantum(classe,user,password,data)
            cont+=1
            console.print(f"-------------------- |[green] {cont} Classe(s) iterada(s) com Sucesso [/green]| --------------------")
        except Exception as e:
            console.print(f"[bold red]Erro : {e}[/bold red]")
            console.print("[yellow]Executando Novamente...[/yellow]")
            mainFunction(classe,user,password,data)

    mainFunction(classeDict,credenciais['user'],credenciais['senha'],data)
    
tempo = (time.time() - antes)/60
print(f"Nº de Execuções: {cont}")
print_banner("Quantum  Axis")
print(f"#################### TEMPO TOTAL DA OPERAÇÂO: {tempo:.2f} min #################### ")
print("")
print("Developed by Levy Pinheiro | Levypinheiro2022@gmail.com | https://www.linkedin.com/in/levypinheiro2023/")
