#!/usr/bin/python3
# -*- coding: utf-8 -*-
import os
try:
    import telnetlib
except ModuleNotFoundError:
    telnetlib = None
import re
import json
import socket
import getpass
import time
from multiprocessing import Pool

class SimpleTelnet:
    def __init__(self, host=None, port=23, timeout=None):
        self.sock = None
        self.buffer = b""
        if host is not None:
            self.open(host, port, timeout)

    def open(self, host, port=23, timeout=None):
        self.sock = socket.create_connection((host, port), timeout)
        self.buffer = b""

    def read_until(self, expected, timeout=10):
        expected = expected if isinstance(expected, bytes) else expected.encode('utf-8')
        end_time = time.time() + timeout
        while expected not in self.buffer:
            if time.time() > end_time:
                break
            chunk = self.sock.recv(4096)
            if not chunk:
                break
            self.buffer += chunk
        idx = self.buffer.find(expected)
        if idx != -1:
            result = self.buffer[:idx + len(expected)]
            self.buffer = self.buffer[idx + len(expected):]
        else:
            result = self.buffer
            self.buffer = b""
        return result

    def write(self, data):
        if isinstance(data, str):
            data = data.encode('utf-8')
        self.sock.sendall(data)

    def close(self):
        if self.sock:
            self.sock.close()
            self.sock = None

class NetworkAutomation:
    def __init__(self, equipamentos):
        self.equipamentos = equipamentos
        self.saida_final = []

    def executar(self):
        """Inicia o processamento paralelo para coletar dados."""
        with Pool(processes=len(self.equipamentos)) as p:
            resultados = p.map(self.processar_conexao, self.equipamentos)
        
        self.saida_final = [res for res in resultados if res is not None]
        return self.saida_final

    def processar_conexao(self, dado):
        """Instancia a conexão e trata possíveis erros de rede."""
        try:
            conn = ConexaoEquipamento(dado)
            return conn.dado_host
        except (socket.timeout, ConnectionRefusedError):
            print(f"[ERRO] Falha ao conectar em {dado['ip']}: Host inacessível.")
            return None
        except Exception as e:
            print(f"[ERRO] Erro inesperado no IP {dado['ip']}: {e}")
            return None

class ConexaoEquipamento:
    def __init__(self, dado):
        self.ip = dado['ip']
        self.usuario = dado['usuario']
        self.senha = dado['senha']
        self.hostname = dado['hostname']
        
        self.start_conn()
        saida_comando = self.get_ip()
        
        parser = TextoUtils()
        lista_interface = parser.extract_ip(saida_comando)
        
        self.dado_host = {self.hostname: lista_interface}

    def start_conn(self):
        """Inicia a conexão Telnet com timeout de segurança."""
        if telnetlib is not None:
            self.tn = telnetlib.Telnet(self.ip, port=23, timeout=10)
        else:
            self.tn = SimpleTelnet(self.ip, port=23, timeout=10)
        
        self.tn.read_until(b":")
        self.tn.write((self.usuario + "\n").encode('utf-8'))
        self.tn.read_until(b":")
        self.tn.write((self.senha + "\n").encode('utf-8'))
        
        self.tn.read_until(b"#")

    def get_ip(self):
        """Executa o comando de diagnóstico."""
        self.tn.write(b"show ip int brief\n")
        saida = self.tn.read_until(b"#").decode('utf-8')
        self.tn.close()
        return saida

class TextoUtils:
    @staticmethod
    def extract_ip(dado):
        """Extrai informações de interface e status usando Regex."""
        linhas = dado.split("\n")
        
        corpo = linhas[2:-1] 
        
        lista_interface = []
        for linha in corpo:
            
            linha_limpa = re.sub(r'\s+', ' ', linha).strip()
            colunas = linha_limpa.split(' ')
            
            if len(colunas) >= 5:
                lista_interface.append({
                    'interface': colunas[0],
                    'ip': colunas[1],
                    'status': colunas[4]
                })
        return lista_interface


def load_credentials():
    usuario = os.getenv("NET_USER")
    senha = os.getenv("NET_PASS")

    if not usuario:
        usuario = input("Usuário de acesso ao equipamento: ").strip()
    if not senha:
        senha = getpass.getpass("Senha de acesso ao equipamento: ")

    return usuario, senha


if __name__ == "__main__":
    meus_equipamentos = [
        {'ip': '10.95.1.1', 'hostname': 'R1'},
        {'ip': '10.95.1.3', 'hostname': 'R2'}
    ]

    usuario, senha = load_credentials()
    for equipamento in meus_equipamentos:
        equipamento['usuario'] = usuario
        equipamento['senha'] = senha

    automacao = NetworkAutomation(meus_equipamentos)
    resultado = automacao.executar()
    print(json.dumps(resultado, indent=4))