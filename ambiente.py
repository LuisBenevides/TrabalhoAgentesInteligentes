import random
import matplotlib.pyplot as plt


class Ambiente:
    def __init__(self, largura, altura, taxa_sujeira=0.3, taxa_obstaculo=0.1):
        self.largura = largura
        self.altura = altura
        self.matriz = {} #a matriz é um dicionário com tuplas (x, y) como chaves
                         #e valores "LIMPO", "SUJO" ou "OBSTACULO" 
        self.agentes = []

        for x in range(largura):
            for y in range(altura):
                # v 
                v = random.random() 
                if v < taxa_sujeira:
                    self.matriz[(x, y)] = "SUJO"
                elif v < taxa_sujeira + taxa_obstaculo:
                    self.matriz[(x, y)] = "OBSTACULO"
                else:
                    self.matriz[(x, y)] = "LIMPO"


    def adicionar_agente(self, agente, posicao):
        if self.matriz.get(posicao) != "OBSTACULO": 
            self.agentes.append(agente)
            agente.posicao = posicao
            agente.ambiente = self

    def percept(self, posicao):
        estado_local = self.matriz.get(posicao, None)
        vizinhos = {}
        movimentos = {"CIMA": (0, -1), "BAIXO": (0, 1),
                      "ESQUERDA": (-1, 0), "DIREITA": (1, 0)}
        for direcao, (dx, dy) in movimentos.items():
            viz = (posicao[0] + dx, posicao[1] + dy)
            
            #se o quadrado vizinho está dentro dos limites do ambiente
            if 0 <= viz[0] < self.largura and 0 <= viz[1] < self.altura: 
                if self.matriz.get(viz) == "OBSTACULO":
                    vizinhos[direcao] = "OBSTACULO"
                else:
                    vizinhos[direcao] = "LIVRE"
            else:
                vizinhos[direcao] = "PAREDE"
        return estado_local, vizinhos

    def sofrer_acao(self, agente, acao):
        if acao == "LIMPAR":
            if self.matriz[agente.posicao] == "SUJO":
                self.matriz[agente.posicao] = "LIMPO"
                return "LIMPOU"
            #ja que o agente não estará na mesma posição que um obstáculo, ele estará em uma posição já limpa
            else:
                return "JA_LIMPO"     
        elif acao in ["CIMA", "BAIXO", "ESQUERDA", "DIREITA"]:
            dx, dy = {
                "CIMA": (0, -1),
                "BAIXO": (0, 1),
                "ESQUERDA": (-1, 0),
                "DIREITA": (1, 0)
            }[acao]
            nova_pos = (agente.posicao[0] + dx, agente.posicao[1] + dy)
            if (0 <= nova_pos[0] < self.largura and
                0 <= nova_pos[1] < self.altura and
                    self.matriz[nova_pos] != "OBSTACULO"):
                agente.posicao = nova_pos
                return "MOVEU"
            else:
                return "BATEU"
        return "INUTIL"

    def esta_limpo(self):
        return all(estado != "SUJO" for estado in self.matriz.values())



