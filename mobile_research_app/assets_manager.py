import random
import requests

def get_experiment_images():
    # --- CONFIGURAÇÃO DO GITHUB ---
    USER = "igaog"
    REPO = "captcha-trust-ai"
    BRANCH = "main"
    # Caminho exato que você definiu
    PATH = "dataset-subsampled/test"
    
    base_raw_url = f"https://raw.githubusercontent.com/{USER}/{REPO}/{BRANCH}/{PATH}"
    
    lista_final = []

    try:
        print(f"--- Conectando ao GitHub: {REPO} ---")
        
        # Lê os catálogos que você criou no Passo 1
        res_real = requests.get(f"{base_raw_url}/lista_real.txt")
        res_fake = requests.get(f"{base_raw_url}/lista_fake.txt")
        
        if res_real.status_code != 200 or res_fake.status_code != 200:
            print("Erro: Não foi possível ler as listas no GitHub. Verifique o PUSH.")
            return []

        nomes_reais = res_real.text.splitlines()
        nomes_fakes = res_fake.text.splitlines()

        # Sorteia 40 de cada entre as milhares disponíveis
        sorteio_real = random.sample(nomes_reais, min(40, len(nomes_reais)))
        sorteio_fake = random.sample(nomes_fakes, min(40, len(nomes_fakes)))

        for nome in sorteio_real:
            lista_final.append({"url": f"{base_raw_url}/real/{nome}", "label": "human"})

        for nome in sorteio_fake:
            lista_final.append({"url": f"{base_raw_url}/fake/{nome}", "label": "ai"})

        random.shuffle(lista_final)
        print(f"Sucesso! {len(lista_final)} imagens prontas para o teste.")
        return lista_final

    except Exception as e:
        print(f"Erro na conexão com assets: {e}")
        return []
