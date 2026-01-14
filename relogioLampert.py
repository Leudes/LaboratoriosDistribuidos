import threading
import time
import random
import queue

class ProcessoLamport(threading.Thread):
    def __init__(self, pid, lista_filas):
        super().__init__()
        self.pid = pid
        self.filas = lista_filas
        self.clock = 0
        self.total_eventos = 5  # Limite de eventos para o teste

    def log(self, acao, detalhes=""):
        print(f"[PROC {self.pid}] Clock: {self.clock:02d} | {acao} {detalhes}")

    def run(self):
        for _ in range(self.total_eventos):
            time.sleep(random.uniform(0.5, 1.2))
            
            # Verifica se há mensagens na caixa de entrada
            if not self.filas[self.pid].empty():
                timestamp_recebido, remetente = self.filas[self.pid].get()
                # Algoritmo de Lamport: max(local, recebido) + 1
                self.clock = max(self.clock, timestamp_recebido) + 1
                self.log("RECEIVE", f"<- de P{remetente} (MsgTime: {timestamp_recebido})")
            
            # Decide ação aleatória
            if random.random() < 0.5: # 50% chance de ser evento interno
                self.clock += 1
                self.log("INTERNAL", "")
            else:
                # Enviar mensagem
                self.clock += 1
                destinatario = (self.pid + 1) % 3
                self.filas[destinatario].put((self.clock, self.pid))
                self.log("SEND   ", f"-> para P{destinatario}")

if __name__ == "__main__":
    print(">>> SIMULAÇÃO LAMPORT INICIADA <<<")
    barramento = [queue.Queue() for _ in range(3)]
    pool_threads = []

    for i in range(3):
        proc = ProcessoLamport(i, barramento)
        pool_threads.append(proc)
        proc.start()