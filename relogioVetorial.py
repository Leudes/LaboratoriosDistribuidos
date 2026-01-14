import threading
import time
import random
import queue

class AgenteVetorial(threading.Thread):
    def __init__(self, uid, total_agentes, rede):
        super().__init__()
        self.uid = uid
        self.rede = rede
        # Inicializa vetor zerado
        self.vetor_estado = [0] * total_agentes

    def sincronizar_vetores(self, vetor_externo):
        """Atualiza o vetor local comparando posição por posição"""
        for i in range(len(self.vetor_estado)):
            self.vetor_estado[i] = max(self.vetor_estado[i], vetor_externo[i])

    def run(self):
        # Executa alguns ciclos
        for _ in range(4):
            time.sleep(random.uniform(0.8, 1.5))
            
            # Tenta receber mensagem (não bloqueante)
            try:
                v_recebido, origem = self.rede[self.uid].get(timeout=0.1)
                self.sincronizar_vetores(v_recebido)
                self.vetor_estado[self.uid] += 1 # Incrementa após receber
                print(f"Agente {self.uid} << RX de {origem} | Estado Atual: {self.vetor_estado}")
            except queue.Empty:
                pass

            # Realiza envio
            self.vetor_estado[self.uid] += 1
            destino = (self.uid + 1) % 3
            
            # Envia cópia da lista para não passar referência
            copia_vetor = list(self.vetor_estado)
            self.rede[destino].put((copia_vetor, self.uid))
            
            print(f"Agente {self.uid} >> TX p/ {destino} | Enviando: {copia_vetor}")

if __name__ == "__main__":
    N_AGENTES = 3
    canais_comunicacao = [queue.Queue() for _ in range(N_AGENTES)]
    
    print(">>> SISTEMA DE RELÓGIOS VETORIAIS <<<")
    
    agentes = []
    for i in range(N_AGENTES):
        a = AgenteVetorial(i, N_AGENTES, canais_comunicacao)
        agentes.append(a)
        a.start()