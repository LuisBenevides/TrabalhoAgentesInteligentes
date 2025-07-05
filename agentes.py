from ambiente import *

class Agente:
    """Superclasse para todos os agentes"""

    def __init__(self):
        self.posicao = None
        self.ambiente = None
        self.pontuacao = 0

    def agir(self):
        raise NotImplementedError("Subclasses devem implementar este método.")


class AgenteReativoSimples(Agente):
    """Agente que reage apenas ao estado atual do ambiente."""

    def agir(self):
        percept_atual, vizinhos = self.ambiente.percept(self.posicao) #tem uma percepção do ambiente a partir da posição atual
        if percept_atual == "SUJO":
            if self.ambiente.sofrer_acao(self, "LIMPAR") == "LIMPOU":   
                self.pontuacao += 1 # Se limpou, ganha ponto
        else:
            #vizinhos é um dicionário com direções ("CIMA", "BAIXO", "ESQUERDA", "DIREITA") como chaves 
            # e estados ("LIVRE", "OBSTACULO", "PAREDE") como valores
            acoes_possiveis = [direcao for direcao, estado in vizinhos.items() if estado == "LIVRE"]
            if acoes_possiveis:
                direcao = random.choice(acoes_possiveis) # escolhe uma ação au hasard
                self.ambiente.sofrer_acao(self, direcao)
                self.pontuacao -= 1  # Movimento custa ponto


class AgenteBaseadoEmModelo(Agente):
    """Agente que mantém um modelo interno do ambiente."""

    def __init__(self):
        super().__init__()
        self.mapa = {}
        self.visitados = set()

    def agir(self):
        percept_atual, vizinhos = self.ambiente.percept(self.posicao)
        self.mapa[self.posicao] = percept_atual
        self.visitados.add(self.posicao)

        if percept_atual == "SUJO":
            if self.ambiente.sofrer_acao(self, "LIMPAR") == "LIMPOU":   
                self.pontuacao += 1 # Se limpou, ganha ponto
            return

        # Procurar vizinho não visitado
        for direcao, estado in vizinhos.items():
            dx, dy = {
                "CIMA": (0, -1),
                "BAIXO": (0, 1),
                "ESQUERDA": (-1, 0),
                "DIREITA": (1, 0)
            }[direcao]
            viz = (self.posicao[0] + dx, self.posicao[1] + dy)
            if estado == "LIVRE" and viz not in self.visitados:
                self.ambiente.sofrer_acao(self, direcao)
                print(direcao)
                self.pontuacao -= 1
                return

        # Senão, mover para qualquer vizinho livre
        livres = [d for d, estado in vizinhos.items() if estado == "LIVRE"]
        if livres:
            direcao = random.choice(livres)
            self.ambiente.sofrer_acao(self, direcao)
            self.pontuacao -= 1