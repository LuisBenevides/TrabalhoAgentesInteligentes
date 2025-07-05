# --------------------
# Simulação
# --------------------
from ambiente import *
from agentes import *


def simular(tipo_agente, passos=100, n_execucoes=30):
    resultados = []

    for _ in range(n_execucoes):
        ambiente = Ambiente(largura=5, altura=5, taxa_sujeira=0.3, taxa_obstaculo=0.1)
        if tipo_agente == "reativo":
            agente = AgenteReativoSimples()
        else:
            agente = AgenteBaseadoEmModelo()

        # Posicionar agente aleatoriamente
        while True:
            pos = (random.randint(0, 4), random.randint(0, 4))
            if ambiente.matriz[pos] != "OBSTACULO":
                break

        ambiente.adicionar_agente(agente, pos)

        for _ in range(passos):
            agente.agir()
            if ambiente.esta_limpo():
                break

        resultados.append(agente.pontuacao)

    return resultados


# --------------------
# Executar e plotar resultados
# --------------------
# reativo = simular("reativo")
# modelo = simular("modelo")

# plt.boxplot([reativo, modelo], labels=["Reativo", "Modelo"])
# plt.title("Desempenho dos agentes")
# plt.ylabel("Pontuação")
# plt.grid(True)
# plt.show()

# print(f"Pontuação média Reativo: {sum(reativo)/len(reativo)}")
# print(f"Pontuação média Modelo: {sum(modelo)/len(modelo)}")




import tkinter as tk
import random
import time


class AmbienteGUI:
    def __init__(self, largura=4, altura=4, tamanho_celula=80):
        self.largura = largura
        self.altura = altura
        self.tamanho = tamanho_celula

        self.ambiente = Ambiente(largura, altura, taxa_sujeira=0.2, taxa_obstaculo=0.1)
        self.agente = AgenteBaseadoEmModelo()

        while True:
            pos = (random.randint(0, largura - 1), random.randint(0, altura - 1))
            if self.ambiente.matriz[pos] != "OBSTACULO":
                break

        self.ambiente.adicionar_agente(self.agente, pos)

        self.root = tk.Tk()
        self.root.title("Simulador de Robô Aspirador")
        self.canvas = tk.Canvas(self.root, width=largura * tamanho_celula,
                                height=altura * tamanho_celula)
        self.canvas.pack()

        self.desenhar_ambiente()
        self.root.after(500, self.executar)
        self.root.mainloop()

    def desenhar_ambiente(self):
        self.canvas.delete("all")
        for x in range(self.largura):
            for y in range(self.altura):
                x1 = x * self.tamanho
                y1 = y * self.tamanho
                x2 = x1 + self.tamanho
                y2 = y1 + self.tamanho

                estado = self.ambiente.matriz.get((x, y))
                visitado = (x, y) in self.agente.visitados

                if estado == "OBSTACULO":
                    cor = "black"
                elif estado == "SUJO":
                    cor = "brown"
                elif estado == "LIMPO" and not visitado:
                    cor = "lightgray"  # limpo mas não visitado
                else:
                    cor = "white"

                self.canvas.create_rectangle(
                    x1, y1, x2, y2, fill=cor, outline="gray"
                )

        # Desenha agente
        ax, ay = self.agente.posicao
        x1 = ax * self.tamanho + 10
        y1 = ay * self.tamanho + 10
        x2 = x1 + self.tamanho - 20
        y2 = y1 + self.tamanho - 20
        self.canvas.create_oval(
            x1, y1, x2, y2, fill="blue"
        )

    def executar(self):
        if not self.ambiente.esta_limpo():
            print(self.agente.posicao)
            self.agente.agir()
            self.desenhar_ambiente()
            self.root.after(500, self.executar)
        else:
            self.desenhar_ambiente()
            self.canvas.create_text(
                (self.largura * self.tamanho) / 2,
                (self.altura * self.tamanho) / 2,
                text="Limpo!",
                font=("Arial", 24),
                fill="green"
            )


# Reaproveitando as classes do código anterior (Ambiente, AgenteReativoSimples e AgenteBaseadoEmModelo)
# Copie-as aqui antes de rodar.

# Coloque aqui as classes Ambiente, AgenteReativoSimples e AgenteBaseadoEmModelo
# (exatamente como te passei antes ou com pequenas adaptações se desejar)


# Executar a interface
AmbienteGUI(largura=3, altura=3, tamanho_celula=80)

# --- Simulação múltipla e comparação dos agentes ---


# import matplotlib.pyplot as plt

# def simular_com_pontuacao_ao_longo_do_tempo(ambiente_largura, ambiente_altura, max_passos):
#     # from main import AgenteReativoSimples, AgenteBaseadoEmModelo, Ambiente  # Ou use suas classes

#     # Criar ambiente
#     ambiente1 = Ambiente(ambiente_largura, ambiente_altura)
#     ambiente2 = Ambiente(ambiente_largura, ambiente_altura)

#     # Gerar mesma configuração para ambos
#     # ambiente1.gerar_sujeira(taxa=0.4)
#     # ambiente1.gerar_obstaculos(taxa=0.1)
#     ambiente2.matriz = ambiente1.matriz.copy()

#     # Instanciar agentes
#     agente_r = AgenteReativoSimples()
#     agente_m = AgenteBaseadoEmModelo()

#     # Posicionar agentes em locais válidos
#     while True:
#         pos = (random.randint(0, ambiente_largura - 1), random.randint(0, ambiente_altura - 1))
#         if ambiente1.matriz[pos] != "OBSTACULO":
#             break

#     ambiente1.adicionar_agente(agente_r, pos)
#     ambiente2.adicionar_agente(agente_m, pos)

#     # Armazenar histórico
#     pontuacoes_r = [0]
#     pontuacoes_m = [0]

#     objetivo_atingido = False
#     for passo in range(max_passos):
#         if not ambiente1.esta_limpo(): 
#             agente_r.agir()
#         if not ambiente2.esta_limpo(): 
#             agente_m.agir()
#         pontuacoes_r.append(agente_r.pontuacao)
#         pontuacoes_m.append(agente_m.pontuacao)

#         # Parar se ambos os ambientes estiverem limpos
#         if ambiente1.esta_limpo() and ambiente2.esta_limpo():
#             print(passo, "passos para limpar ambos os ambientes.")
#             objetivo_atingido = True
#             break
#     if not objetivo_atingido:
#         print("Provavelmente o objetivo (limpar todos os quadrados sujos) não pode ser atingido no ambiente atual.")

#     # Plotar gráfico
#     plt.figure(figsize=(10, 5))
#     plt.plot(pontuacoes_r, label='Agente Reativo Simples')
#     plt.plot(pontuacoes_m, label='Agente Baseado em Modelo')
#     plt.title("Pontuação dos Agentes ao longo do tempo")
#     plt.xlabel("Tempo (passos)")
#     plt.ylabel("Pontuação acumulada")
#     plt.legend()
#     plt.grid(True)
#     plt.tight_layout()
#     plt.show()

# simular_com_pontuacao_ao_longo_do_tempo(5, 5, max_passos=300)
