import threading
import time
import random
from datetime import datetime

class NoFisico(threading.Thread):
    def __init__(self, node_id):
        super().__init__()
        self.node_id = node_id

    def run(self):
        # Executa 5 iterações como exemplo
        for i in range(1, 6):
            time.sleep(random.uniform(0.2, 0.6))
            
            # Pega o timestamp atual
            timestamp = time.time()
            # Formata para humano ler também
            hora_legivel = datetime.fromtimestamp(timestamp).strftime('%H:%M:%S.%f')[:-3]
            
            print(f"[LOG SERVER-{self.node_id}] | ID: {i} | Time: {hora_legivel}")

if __name__ == "__main__":
    print(">>> INICIANDO MONITORAMENTO DE TEMPO FÍSICO <<<")
    processos = []
    
    # Criando 3 nós
    for i in range(3):
        p = NoFisico(i)
        processos.append(p)
        p.start()

    for p in processos:
        p.join()