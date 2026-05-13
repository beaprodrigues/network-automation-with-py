# Network Automation - Automação de Infraestrutura com Python

#### Esse repositório contém uma série de projetos focados em automação de rede, desenvolvidos para demonstrar a evolução de scripts básicos de conectividade até a criação de uma API de monitoramento.
#### Esse projeto foi construído pensando em cenários reais de **Suporte de TI e Redes**, onde a agilidade e a padronização na coleta de dados são fundamentais. Automatiza a coleta de status de interfaces, evitando falhas manuais de digitação ou esquecimento de equipamentos.
---

## Estrutura do Projeto

O repositório está organizado em etapas evolutivas, facilitando o entendimento da lógica aplicada:

* **Projeto 01: Conexão Base**
    * Scripts iniciais para automação de login via protocolo Telnet em equipamentos de rede.
    * Foco: Automação de tarefas repetitivas de login.
      
* **Projeto 02: Escalabilidade com Multiprocessing**
    * Implementação de paralelismo para execução de comandos em múltiplos dispositivos simultaneamente.
    * Foco: Redução do tempo de execução em infraestruturas maiores.
      
* **Projeto 03: Extração de Dados e Parsing**
    * Uso de **Expressões Regulares (Regex)** para filtrar o output do comando `show ip int brief`.
    * Foco: Transformar dados brutos de texto em informações estruturadas (JSON).
      
* **Projeto 04: Monitoramento via Web API**
    * Criação de um **Web Service (Flask)** que expõe os dados coletados dos equipamentos.
    * Foco: Integração com outras ferramentas e visibilidade de dados em tempo real.

---

## Tecnologias e Ferramentas

* **Linguagem:** Python 
* **Protocolos:** Telnet (Telnetlib)
* **Framework Web:** Flask (Flask-RESTful)
* **Paralelismo:** Multiprocessing (Pool)
* **Processamento de Texto:** RE (Regular Expressions)
* **Automação de Versão:** Bash Scripts (`push.sh`)

---

## Notas de Segurança

> **Importante:** Este repositório é um estudo, portanto profissionalmente o ideal é:
> * Substituir o protocolo Telnet por **SSH (Netmiko/Paramiko)**.
> * Utilizar **Variáveis de Ambiente (.env)** ou cofres de senha para gerenciar credenciais, evitando a exposição de senhas no código fonte.

---

## Como Executar

1. Clone o repositório:
   ```bash
   git clone [https://github.com/seu-usuario/Network-automation.git](https://github.com/seu-usuario/Network-automation.git)
