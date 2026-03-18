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