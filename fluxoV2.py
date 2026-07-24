from selenium import webdriver
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException  # <--- MONITOR
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import Select
import os
import time
import threading  # <--- MONITOR
from Transform import transform_sheet
import warnings
import urllib3


urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)
with warnings.catch_warnings():
    warnings.simplefilter("ignore", UserWarning)

def automacao_quantum(listaClasses, user, password,data):
    os.environ['WDM_SSL_VERIFY'] = '0' #Comando para impedir erros de execução relativos a certificado SSL
    
    nome_relatorio = ''
    PASTA_DOWNLOAD = os.path.join(os.path.dirname(__file__), "RelatoriosExtraidos")

    options = webdriver.ChromeOptions()
    options.add_argument("--log-level=3")          # suprime warnings/erros do Chrome
    options.add_argument("--disable-notifications") # elimina o GCM/push registration
    options.add_experimental_option("excludeSwitches", ["enable-logging"])  # Windows-specific
    options.add_experimental_option("prefs", {
        "download.default_directory": PASTA_DOWNLOAD,
        "download.prompt_for_download": False,
        "download.directory_upgrade": True,
        "safebrowsing.enabled": True
    })
    nome_relatorio_categoria = str(list(dict(listaClasses).keys())[0]).upper()
    max_temp = 60
    
    #head_less = input("Headless Mode?  1 - Sim | 0 - Não")
    #if head_less ==1:
        #options.add_argument("--headless=new")
        #print("Headless Ativado")
    options.add_argument('--window-size=900,900')
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver,max_temp)

    # <--- MONITOR: flag e thread de monitoramento de fechamento da janela
    fechamento_intencional = {"valor": False}  # dict para permitir mutação dentro do closure

    def monitorar_fechamento(intervalo=1):
        def _verificar():
            while True:
                if fechamento_intencional["valor"]:
                    return
                try:
                    _ = driver.window_handles
                except WebDriverException:
                    if not fechamento_intencional["valor"]:
                        print("\n[ERRO] Janela do Chrome fechada pelo usuário. Encerrando.")
                        #raise WebDriverException("Janela fechada pelo usuário")
                    return
                time.sleep(intervalo)
        threading.Thread(target=_verificar, daemon=True).start()

    monitorar_fechamento()
    # <--- FIM MONITOR

    print("")

    def autenticacao():
        #print("Tentando localizar campos de login e senha...")
        try:
            driver.get("https://www.quantumaxis.com.br/webaxis/login.jsp")
    
            usuario_input = wait.until(EC.visibility_of_element_located((By.ID, "campoLogin")))
            senha_input = driver.find_element(By.ID, "campoSenha")
            usuario_input.send_keys(user)
            senha_input.send_keys(password)
            wait.until(EC.element_to_be_clickable((By.ID, "botaoEntrar"))).click()
            print("Login efetuado com sucesso!")
            # Espera algum elemento da página pós-login para confirmar que entrou
            wait.until(EC.presence_of_element_located((By.ID, "linkFiltro")))
    
        except Exception as e:
            print(f"Erro no login: {e}")
            fechamento_intencional["valor"] = True  # <--- MONITOR
            driver.quit()


    def esperar_elemento(driver, xpath, timeout=10):
        """Apenas espera e retorna o elemento."""
        wait_local = WebDriverWait(driver, timeout)
        return wait_local.until(EC.visibility_of_element_located((By.XPATH, xpath)))


    def adicionar_indicador_selecao(driver, timeout=10):
        try:
            # Tenta rápido primeiro (4s)
            xpath_CDI = "/html/body/div[8]/div[1]/div[2]/ul/li/ul/li/div"
            esperar_elemento(driver, xpath_CDI, timeout=10)
        except TimeoutException:
            # Demorou mais que 4s — refaz o processo com timeout completo
            print("Elemento demorou. Refazendo o processo...")
            className = ".jqx-combobox-input-menuPrincipalAxis"
            input_pesquisa = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, className)))
            time.sleep(3)
            input_pesquisa.click()
            time.sleep(2)
            xpath_btn_contextual = '//*[@id="botaoContextual"]'
            esperar_elemento(driver, xpath_btn_contextual, timeout).click()
            time.sleep(2)
            xpath_menuContextual_adicionar_ativo = '//*[@id="menuContextual"]/div[1]/div/div/div/div[1]'
            esperar_elemento(driver, xpath_menuContextual_adicionar_ativo, timeout).click()
                

    def adiciona_Indicadores(indicadores):
        
        #dentro da lista os elementos serão dicionários que possuem chave e valor. a chave é o nome do Indicador, e o valor será seu xpath. o primeiro 
        # dicionario terá como chave nome do tipo de indicador e valor o xpath associado. o segundo dicionário terá como chave nome do indicador 
        # e xpath associado.
        #exemplo:
        # [ {'índices' : '123//123', 'CDI': '345//345}]
        
        #localizar input de pesquisa principal
        for indicador in indicadores:
            className = ".jqx-combobox-input-menuPrincipalAxis"
            input_pesquisa = wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, className)))
            btnFiltros = driver.find_element(By.ID, "filtrosBuscaGlobal")
            time.sleep(2)
            btnFiltros.click()
            indices = wait.until(EC.visibility_of_element_located((By.XPATH, list(indicador.values())[0] ))).click()
            valorIndicador = list(indicador.keys())[1]
            time.sleep(2)
            input_pesquisa.send_keys(valorIndicador) #indicador.keys() -> chav do dicionário: "CDI"
            xpathIndicador = list(indicador.values())[1]
            valorCDI = wait.until(EC.visibility_of_element_located((By.XPATH, xpathIndicador ))) #
            time.sleep(1)
            valorCDI.click()
            adicionar_Indicador_selecao = wait.until(EC.visibility_of_element_located((By.XPATH, '//*[@id="menuContextual"]/div[1]/div/div/div/div[1]'))) #labe:Adicionar ativo à seleção
            time.sleep(2)
            adicionar_Indicador_selecao.click()
            adicionar_indicador_selecao(driver,timeout=5)
            time.sleep(2)
        
    
    def adicionaFundos():
        #        for fundoNomes in listaClasses.values():
        for categoria, lista_fundos in listaClasses.items():   
            print(f"Categoria: {str(categoria).upper()}")

                # IMPORTANTE: lista_fundos precisa ser uma lista de strings. Ex: ["Ações Livre", "Renda Fixa"]
            for fundo in lista_fundos:
                # Campo
                time.sleep(0.5)
                wait.until(EC.element_to_be_clickable((By.NAME, "cmbCampos")))
                Select(driver.find_element(By.NAME, "cmbCampos")).select_by_visible_text("Classificação Anbima")
                time.sleep(0.5)
                # Operador
                Select(driver.find_element(By.NAME, "cmbOperador")).select_by_value("2")
                time.sleep(0.5)
                # Sinal
                Select(driver.find_element(By.NAME, "cmbSinal")).select_by_value("1")
                time.sleep(0.5)
                # Valor — espera as opções carregarem (mais que o valor padrão "0")
                wait.until(lambda d: len(Select(d.find_element(By.NAME, "cmbValor")).options) > 1)
                Select(driver.find_element(By.NAME, "cmbValor")).select_by_visible_text(fundo)
                time.sleep(0.5)
                # Adicionar
                wait.until(EC.element_to_be_clickable((By.ID, "btnAdicionar"))).click()
                time.sleep(0.5)
                # Espera o número de fundos atualizar
                wait.until(EC.presence_of_element_located((By.XPATH, "//font[contains(., 'Número de Fundos:')]")))
                numero = driver.find_element(By.XPATH, "//font[contains(., 'Número de Fundos:')]").text.split(":")[-1].strip()
                print(f"Classificação Anbima | Fundo: {fundo} | Nº Fundos: {numero}")
        time.sleep(2)
        # Clica em OK
        btOk=wait.until(EC.element_to_be_clickable((By.ID, "btnOK")))
        time.sleep(3)
        btOk.click()
        time.sleep(2)
        # Volta ao contexto principal após sair do iframe
        driver.switch_to.default_content()
    
    def filtrar():
        #print("Esperando iframe carregar ...")
        driver.switch_to.default_content()
        driver.execute_script("document.getElementById('linkFiltro').click()")
        time.sleep(1)
        driver.execute_script("document.getElementById('linkFiltro').click()")
        # Espera o iframe carregar e troca contexto
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "main")))
        time.sleep(1)

    def abrirRelatorio():
        
        wait = WebDriverWait(driver, 400)
        # Clica no botão de relatório
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "main")))
        time.sleep(1)
        btnRelatorio = wait.until(EC.element_to_be_clickable((By.ID, "imgPersonalizada")))
        time.sleep(1)
        btnRelatorio.click()
        time.sleep(1)
        # Abre o seletor de arquivos
        btnAbrir = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(@class, "Button--ok") and .//span[text()="Abrir"]]')))
        time.sleep(1)
        btnAbrir.click()
        # Seleciona o arquivo de medidas
        variaveis = wait.until(EC.element_to_be_clickable((
            By.XPATH,
            "//td[contains(@class, 'ListaArquivosMedidas__celula--nome') and text()='M_FUNDOS TODOS PARA IA 2025']"
        )))
        time.sleep(1)
        variaveis.click()
        # Confirma
        inputData = wait.until(EC.visibility_of_element_located((By.CLASS_NAME,"MedidasSelecionadasHeader__input-data-base")))
        time.sleep(1)
        inputData.click()
        # 8 dígitos = 8 backspaces (ou 10 se contar as barras)
        for _ in range(8):
            inputData.send_keys(Keys.BACKSPACE)
        time.sleep(1)
        inputData.send_keys(data)
        #time.sleep(1)
        #BTN Abrir
        #inputData.send_keys(Keys.TAB)
        time.sleep(1)
        print("Esperando fundos...")
        # espera os fundos serem carregados
        #Para garantir que o driver busque no lugar exato e não se perca em outros elementos da página, force a busca partindo da div principal (#listaItensSelecionados):
        driver.switch_to.default_content() # sair do iframe principal para detectar fundos,
        wait.until(
            EC.visibility_of_element_located((By.CLASS_NAME, 'ellipsis-overflow'))#"//span[@class='nomePai' and text()='Fundos']"))
        )
        time.sleep(0.5)
        print("Fundos Carregados!")
        #voltar pro iframe principal
        wait.until(EC.frame_to_be_available_and_switch_to_it((By.NAME, "main")))
        element = wait.until(EC.element_to_be_clickable((By.XPATH, '//*[@id="root"]/div/div[6]/button[8]')))
        time.sleep(1)
        element.click()
        
        time.sleep(1)
        
        print("Esperando relatório carregar...")
        # Espera até o carregamento do relatório na tela antes de clicar em download.
        wait.until(EC.element_to_be_clickable((By.XPATH, '/html/body/div[2]/div/div/div/div[3]/div/div/div[2]/div[1]/div[3]'))) 
        time.sleep(1)
        btnDownload = wait.until(EC.visibility_of_element_located((By.CLASS_NAME,'q-icon-excel2')))
        time.sleep(1)
        btnDownload.click()
        time.sleep(1)
        print("Iniciando download...")
        
        ###################################################################################
        antes = set(os.listdir(PASTA_DOWNLOAD))
        fim = time.time() + 790
        nome_relatorio ='' 
        while time.time() < fim:
            
            novos = set(os.listdir(PASTA_DOWNLOAD)) - antes
            concluidos = [f for f in novos if f.endswith(".xlsx") and not f.endswith(".crdownload")]
            if concluidos:
            
                nome_relatorio = concluidos[0]
                nomefinal = f"{nome_relatorio_categoria}_{data} - BRUTO.xlsx"
                os.replace(os.path.join(PASTA_DOWNLOAD, nome_relatorio), os.path.join(PASTA_DOWNLOAD, nomefinal))
                print(f"Download confirmado: {nomefinal}")
            
                break
            time.sleep(1)
        time.sleep(1)
        driver.switch_to.default_content()
        fechamento_intencional["valor"] = True  # <--- MONITOR
        driver.quit()
        return nomefinal
    antes = time.time()
    
    
    autenticacao()
    if nome_relatorio_categoria == 'INDICADORES':
        adiciona_Indicadores(
            [
            {"Índices":"//*[@id='filtroBuscaGlobalOpcoes']/ul/li[8]" , 'CDI':"//div[@role='option'][.//span[normalize-space()='CDI']]"},
            {"Índices":"//*[@id='filtroBuscaGlobalOpcoes']/ul/li[8]" , 'IBOVESPA':"//div[@role='option'][.//span[normalize-space()='IBOVESPA']]"},
            {"Índices":"//*[@id='filtroBuscaGlobalOpcoes']/ul/li[8]" , 'IFIX':"//div[@role='option'][.//span[normalize-space()='IFIX']]"},
            {"BenchMarks Personalizados":"//*[@id='filtroBuscaGlobalOpcoes']/ul/li[9]", '105% DO CDI':"//div[@role='option'][.//span[normalize-space()='105% DO CDI']]"},
            {"BenchMarks Personalizados":"//*[@id='filtroBuscaGlobalOpcoes']/ul/li[9]", 'ÍNDICE IPCA +5,00%':"//div[@role='option'][.//span[normalize-space()='ÍNDICE IPCA +5,00%']]"},
            {"BenchMarks Personalizados":"//*[@id='filtroBuscaGlobalOpcoes']/ul/li[9]", 'ÍNDICE INPC + 5,25%':"//div[@role='option'][.//span[normalize-space()='ÍNDICE INPC +5,25%']]"}
            ])
    
    if nome_relatorio_categoria != 'INDICADORES':
        filtrar()
        adicionaFundos()

    nome_relatorio_recebido = abrirRelatorio() 
    
    
    PASTA_GPT = os.path.join(os.path.dirname(__file__), "RelatoriosGPT")
    PASTA_TRATADOS = os.path.join(os.path.dirname(__file__), "RelatoriosTratados")
    PASTA_DOWNLOAD = os.path.join(os.path.dirname(__file__), "RelatoriosExtraidos")
    nome_relatorio_final = os.path.join(PASTA_TRATADOS,nome_relatorio_categoria)
    nome_relatorio_recebido = os.path.join(PASTA_DOWNLOAD,nome_relatorio_recebido)
    
    transform_sheet(nome_relatorio_recebido,nome_relatorio_final,data,nome_relatorio_categoria,PASTA_GPT)
    tempo = (time.time() - antes)/60
    print("Tratamento Finalizado com Sucesso!")
    print(f"Tempo de execução: {tempo:.2f} min")