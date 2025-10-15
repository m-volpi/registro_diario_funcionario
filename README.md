# Registro Diário de Funcionários

## Descrição

Este projeto consiste em um script de ETL (Extração, Transformação e Carga) desenvolvido para automatizar a criação de um histórico diário do quadro de funcionários. O script extrai dados de uma tabela de produção, realiza uma transformação para obter o registro mais recente de cada funcionário no dia e os carrega em uma tabela de histórico em um banco de dados separado.

O objetivo é manter um registro sólido e confiável das alocações de funcionários ao longo do tempo, permitindo análises e cálculos de negócio futuros com base em dados históricos consistentes.

## Tecnologias Utilizadas

*   **Python 3**
*   **PostgreSQL** (para ambos os bancos de dados, origem e destino)
*   **Bibliotecas Python:**
    *   `psycopg2-binary`: Para conexão com o PostgreSQL.
    *   `python-dotenv`: Para gerenciamento de variáveis de ambiente e credenciais.
    *   `tqdm`: Para exibir uma barra de progresso durante a migração.

## Configuração do Ambiente

Siga os passos abaixo para configurar e executar o projeto localmente.

**1. Clone o Repositório**
```bash
git clone https://github.com/m-volpi/registro_diario_funcionario.git
cd registro_diario_funcionario
```

**2. Instale as Dependências**

É recomendado criar um ambiente virtual para o projeto.

```bash
# Crie um ambiente virtual (opcional, mas recomendado)
python -m venv venv

# Ative o ambiente virtual
# No Windows:
venv\Scripts\activate
# No macOS/Linux:
# source venv/bin/activate
```

Instale as bibliotecas necessárias a partir do arquivo `requirements.txt`.
```bash
pip install -r requirements.txt
```

**3. Configure as Variáveis de Ambiente**

O projeto utiliza um arquivo `.env` para armazenar as credenciais de acesso aos bancos de dados de forma segura.

*   Crie uma cópia do arquivo de exemplo `.env.example` e renomeie-a para `.env`.
*   Abra o arquivo `.env` e preencha as variáveis com as informações de conexão dos seus bancos de dados de origem e destino.

O arquivo `.env` deve ter a seguinte estrutura:
```
ORIGEM_HOST=seu_host_de_origem
ORIGEM_DBNAME=seu_banco_de_origem
ORIGEM_USER=seu_usuario_de_origem
ORIGEM_PASSWORD=sua_senha_de_origem
ORIGEM_PORT=sua_porta_de_origem

DESTINO_HOST=seu_host_de_destino
DESTINO_DBNAME=seu_banco_de_destino
DESTINO_USER=seu_usuario_de_destino
DESTINO_PASSWORD=sua_senha_de_destino
DESTINO_PORT=sua_porta_de_destino
```

## Uso

Para executar o script de migração, basta rodar o arquivo `main.py`:

```bash
python main.py
```

O script se conectará aos bancos de dados, executará a migração e registrará o progresso em um arquivo de log na pasta `logs/`.

## Licença

Este projeto está licenciado sob a [Licença Apache 2.0](LICENSE).
