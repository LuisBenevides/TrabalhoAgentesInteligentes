# --------------------
# Simulação
# --------------------
from ambiente import *
from agentes import *


import matplotlib.pyplot as plt
import random
import copy

def clonar_ambiente(orig):
    novo = Ambiente(orig.largura, orig.altura, taxa_sujeira=0, taxa_obstaculo=0)
    novo.matriz = dict(orig.matriz)  # clona os estados das células
    return novo

def simular(passos=100, n_execucoes=30):
    resultados_reativo = []
    resultados_modelo = []

    for _ in range(n_execucoes):
        # Gerar ambiente-base
        ambiente_base = Ambiente(largura=4, altura=4, taxa_sujeira=0.3, taxa_obstaculo=0.1)

        # Escolher posição inicial válida
        while True:
            pos_inicial = (random.randint(0, ambiente_base.largura - 1),
                           random.randint(0, ambiente_base.altura - 1))
            if ambiente_base.matriz[pos_inicial] != "OBSTACULO":
                break

        # -------------------------
        # Agente Reativo
        # -------------------------
        ambiente_r = clonar_ambiente(ambiente_base)
        agente_r = AgenteReativoSimples()
        ambiente_r.adicionar_agente(agente_r, pos_inicial)

        for _ in range(passos):
            agente_r.agir()
            if ambiente_r.esta_limpo():
                break

        resultados_reativo.append(agente_r.pontuacao)

        # -------------------------
        # Agente Baseado em Modelo
        # -------------------------
        ambiente_m = clonar_ambiente(ambiente_base)
        agente_m = AgenteBaseadoEmModelo()
        ambiente_m.adicionar_agente(agente_m, pos_inicial)

        for _ in range(passos):
            agente_m.agir()
            if ambiente_m.esta_limpo():
                break

        resultados_modelo.append(agente_m.pontuacao)

    return resultados_reativo, resultados_modelo

# Executar e plotar resultados
reativo, modelo = simular()

plt.boxplot([reativo, modelo], tick_labels=["Reativo", "Modelo"])
plt.title("Desempenho dos agentes")
plt.ylabel("Pontuação")
plt.grid(True)
plt.show()

print(f"Pontuação média Reativo: {sum(reativo)/len(reativo):.2f}")
print(f"Pontuação média Modelo: {sum(modelo)/len(modelo):.2f}")





import tkinter as tk
import random
import time


class AmbienteGUI:
    def __init__(self, largura=4, altura=4, tamanho_celula=80, taxa_sujeira=0.2, taxa_obstaculo=0.2):
        self.largura = largura
        self.altura = altura
        self.tamanho = tamanho_celula
        self.pos_inicial = None

        self.ambiente = Ambiente(largura, altura, taxa_sujeira, taxa_obstaculo)
        self.agente = AgenteBaseadoEmModelo()

        while True:
            self.pos_inicial = (random.randint(0, largura - 1), random.randint(0, altura - 1))
            if self.ambiente.matriz[self.pos_inicial] != "OBSTACULO":
                break

        self.ambiente.adicionar_agente(self.agente, self.pos_inicial)

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
                x_rel = x - self.pos_inicial[0]
                y_rel = y - self.pos_inicial[1]

                visitado = (x_rel, y_rel) in self.agente.visitados

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
            self.root.after(1000, self.desenhar_mapa_interno)

    def desenhar_mapa_interno(self):
        # self.canvas.delete("all")
        nova_janela = tk.Toplevel(self.root)
        nova_janela.title("Mapa Interno do Agente")

        mapa = tk.Canvas(nova_janela, width=self.largura * self.tamanho,
                                height=self.altura * self.tamanho)
        mapa.pack()
        for x in range(self.largura):
            for y in range(self.altura):
                x1 = x * self.tamanho
                y1 = y * self.tamanho
                x2 = x1 + self.tamanho
                y2 = y1 + self.tamanho

                # estado = self.ambiente.matriz.get((x, y))
                x_rel = x - self.pos_inicial[0]
                y_rel = y - self.pos_inicial[1]

                visitado = (x_rel, y_rel) in self.agente.visitados
                # padrão: desconhecido = laranja
                cor = "orange"

                if (x_rel, y_rel) in self.agente.mapa:
                    estado = self.agente.mapa[(x_rel, y_rel)]
                    if estado == "OBSTACULO":
                        cor = "black"
                    else:
                        cor = "green"

                mapa.create_rectangle(
                    x1, y1, x2, y2, fill=cor, outline="gray"
                )

        # Desenha agente na última posição conhecida
        ax, ay = self.agente.posicao
        x1 = ax * self.tamanho + 10
        y1 = ay * self.tamanho + 10
        x2 = x1 + self.tamanho - 20
        y2 = y1 + self.tamanho - 20
        mapa.create_oval(
            x1, y1, x2, y2, fill="blue"
        )

        # Mensagem final
        mapa.create_text(
            (self.largura * self.tamanho) / 2,
            (self.altura * self.tamanho) + 20,
            text="Mapa Interno do Agente",
            font=("Arial", 16),
            fill="black"
        )
    


##################################### Executar a interface #####################################
AmbienteGUI(largura=4, altura=4, tamanho_celula=80, taxa_sujeira=0.2, taxa_obstaculo=0.15)
################################################################################################







