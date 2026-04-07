import time

class ExperimentSession:
    def __init__(self, lista_imagens):
        self.lista_imagens = lista_imagens
        self.index_atual = 0
        self.respostas = []
        self.tempo_inicio = 0

    def iniciar_cronometro(self):
        """Chame isso toda vez que uma nova imagem aparecer na tela."""
        self.tempo_inicio = time.time()

    def get_current_image(self):
        """Retorna os dados da imagem atual ou None se o teste acabou."""
        if self.index_atual < len(self.lista_imagens):
            return self.lista_imagens[self.index_atual]
        return None

    def registrar_resposta(self, escolha):
        """Calcula o tempo de reação e pula para a próxima imagem."""
        tempo_reacao = time.time() - self.tempo_inicio
        img_data = self.get_current_image()
        
        if img_data:
            self.respostas.append({
                "image": img_data["url"],
                "label_real": img_data["label"],
                "escolha_usuario": escolha,
                "tempo_segundos": round(tempo_reacao, 3)
            })
            self.index_atual += 1
