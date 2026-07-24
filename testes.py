import subprocess
import sys
import time
t = 0
e = 0
tempo_inicial =  time.time()
print("================================ Inicialização: Etapas de Stress Testing ================================")
for x in range(1,30):

    resultado = subprocess.run([sys.executable,"main.py"])
    t+=1
    if resultado.returncode != 0:
        print(f"Script main.py falhou na execução {x}")
        e+=1
    else:
        print(f"Sucesso na execução {x}")
    
    taxa_erro = (e/t)*100 if t > 0 else 0
    print(f"Sucessos: {t - e} | Falhas:{e} | Taxa de Erro: {taxa_erro:.2f}%")
taxa_acerto = 100 - taxa_erro
tempo_final  = time.time() - tempo_inicial
print("==================================== FIM ===============================================")
print(f"************************ TEMPO TOTAL DOS TESTES: {tempo_final} *************************")
print("")
print(f"Sucessos: {t - e} | Falhas:{e} | Taxa de Erro: {taxa_erro:.2f}% | Taxa de Acerto: {taxa_acerto:.2f}")



    