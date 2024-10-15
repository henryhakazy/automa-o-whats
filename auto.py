from selenium import webdriver
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.chrome.service import Service  # Import necessário no Selenium 4
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
import time
import pandas as pd

# Caminho do ChromeDriver
chrome_driver_path = "D:/chromedriver/chromedriver.exe"

profile_path = "C:/Users/Henrique Silva Ramos/AppData/Local/Google/Chrome/User Data/Default"  # Mude para um diretório de sua escolha

# Carrega a planilha
planilha = pd.read_excel('contatos.xlsx')

# Mensagem a ser enviada
mensagem = "Olá! Tudo bem? Somos da Loja Viva Conceito, por gentileza poderia me enviar os nomes que serão gravados no colar? Obrigado e tenha um ótima tarde."

# Configura o navegador sem user-data-dir
options = webdriver.ChromeOptions()
options = webdriver.ChromeOptions()
options.add_argument(f"user-data-dir={profile_path}")
options.add_argument("--profile-directory=adadad")  # Substitua "Default" pelo nome do perfil se você estiver usando um diferente
options.add_argument("--no-sandbox")
options.add_argument("--disable-dev-shm-usage")


# Inicialize o Service para usar o ChromeDriver
service = Service(executable_path=chrome_driver_path)
navegador = webdriver.Chrome(service=service, options=options)

# Abre o WhatsApp Web
navegador.get("https://web.whatsapp.com")
time.sleep(15)  # Tempo para escanear o QR Code

# Loop para enviar a mensagem para cada número na planilha
for index, linha in planilha.iterrows():
    telefone = linha['Telefone']
    
    # Abre o chat com o número
    url = f"https://web.whatsapp.com/send?phone={telefone}&text={mensagem}"
    navegador.get(url)
    
    # Aguarda a página carregar
    time.sleep(10)  # Ajuste o tempo se necessário
    
    try:
        # Aguarda até que o botão de enviar esteja presente e clicável
        enviar_btn = WebDriverWait(navegador, 20).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@data-icon="send"]'))
        )
        enviar_btn.click()  # Clica no botão de enviar
        time.sleep(5)  # Aguarda o envio
        print(f"Mensagem enviada para ({telefone})")
    except Exception as e:
        print(f"Erro ao enviar mensagem para ({telefone}): {e}")
    
    # Espera antes de enviar a próxima mensagem
    time.sleep(5)


# Fecha o navegador
navegador.quit()
