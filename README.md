# 🛡️ AssetGuard - Gestão de Ativos de TI (AI-Driven)

O **AssetGuard** é uma aplicação avançada de gestão de inventário de hardware desenvolvida para a Pós-Graduação da **PUC Minas**. O projeto demonstra o paradigma de **Engenharia de Software Orientada por Agentes (ASOE)**, onde a governança e a conformidade são orquestradas por Inteligência Artificial Generativa.



## 🚀 Diferenciais Tecnológicos
- **Cérebro de IA:** Integração nativa com **Google Gemini 2.0 Flash** para auditoria semântica de conformidade.
- **Governança Executável:** Regras de negócio extraídas diretamente do `blueprint.md` (Constituição do Agente).
- **Privacidade por Design:** Mascaramento automático de CPFs e IPs (LGPD) antes do processamento em nuvem.
- **Notificação em Tempo Real:** Sistema SMTP para alertas de alterações críticas via e-mail HTML.

## 🛠️ Funcionalidades Principais

### 1. Dashboard de Governança (US01 & US04)
- Visualização interativa de ativos com **Plotly**.
- Filtro de **Violação de Política** para identificação imediata de inconformidades.
- Botão de **Auditoria IA**: O Gemini analisa o inventário e fornece diagnóstico técnico sobre riscos.

### 2. Cadastro com Auditoria (US02 & US07)
- Validação rigorosa de hardware:
    - **MacBook Pro:** Restrito a cargos Sênior, Lead e Diretoria.
    - **Rede (Switches/Roteadores):** Restrito a Departamentos (bloqueio de CPF).
- **Envio Automático de E-mail:** Notificação tabular enviada para a equipe de DevOps a cada alteração.

### 3. Log de Auditoria Imutável (US06)
- Registro de todas as operações (Login, Inserção, Deleção) no arquivo `audit.log`.
- **Bloqueio de Deleção:** Ativos com valor residual > R$ 0,00 não podem ser removidos, garantindo integridade financeira.

## ⚙️ Configuração do Ambiente

### 1. Variáveis de Ambiente (`.env`)
Crie um arquivo `.env` na raiz com as seguintes chaves:
```env
GEMINI_API_KEY=Sua_Chave_Google_AI_Studio
EMAIL_USER=seu_email@gmail.com
EMAIL_PASS=sua_senha_de_app_google
Fazer ajuste no arquivo email_service.py
Na linha 17 inserir o email definido como destinatario

## Como Executar

### Opção 1: Via Docker (Recomendado)
1. Certifique-se de ter o Docker e Docker Compose instalados.
2. Build e execução do container:
   ```bash
   docker-compose up --build
   ```
3. Acesse em seu navegador: `http://localhost:8501`

### Opção 2: Localmente (Ambiente Virtual)
1. Crie um ambiente virtual:
   ```bash
   python -m venv venv
   source venv/bin/activate  # No Windows: venv\Scripts\activate
   ```
2. Instale as dependências:
   ```bash
   pip install -r requirements.txt
   ```
3. Execute a aplicação:
   ```bash
   streamlit run app.py
   ```

## Estrutura do Projeto
- `app.py`: Interface do usuário (Streamlit) e orquestração do sistema.
- `agent_core.py`: Motor de Inteligência Artificial (Google Gemini 2.0 Flash).
- `email_service.py`: Serviço de notificações SMTP (E-mail HTML).
- `validators.py`: Regras de governança e validações isoladas.
- `data_service.py`: Persistência, log de auditoria e geração de dados.
- `blueprint.md`: A "Constituição" do software com requisitos e regras.
- `audit.log`: Registro histórico de todas as operações do sistema.
- `assets_data.json`: Banco de dados local em formato JSON.
- `Dockerfile` & `docker-compose.yml`: Configuração para ambiente agnóstico.
