# Projeto: AssetGuard

## Contexto e Objetivo
O AssetGuard é uma aplicação de gestão de ativos de TI desenvolvida para demonstrar o paradigma de Engenharia de Software Orientada por Agentes. O software permite o controle de inventário de hardware, garantindo que a distribuição de equipamentos siga rigorosamente as políticas de governança e conformidade da empresa, movendo o foco do desenvolvimento da escrita de código (sintaxe) para a definição de regras (semântica).

## Stack Técnica
- **Framework:** Streamlit (Python)
- **Database:** JSON Local (`assets_data.json`)
- **Auth:** Mock Auth (Simulação de login por nível: Admin, Manager, Staff)

## User Stories (Tabela de Implementação)

| ID   | Descrição | Critérios de Aceite | Prioridade |
|:---  |:--- |:--- |:--- |
| US01 | Dashboard de Inventário | Exibir tabela interativa com todos os ativos e gráficos de custos por departamento usando Plotly. | Alta |
| US02 | Atribuição com Auditoria | Formulário de cadastro que valida os inputs contra as "Regras de Governança" antes de salvar no JSON. | Alta |
| US03 | Geração de Dados Sintéticos | Criar função para gerar 50 registros fictícios no JSON. **Nota:** 20% dos dados devem violar as regras de governança para fins de teste de auditoria. | Alta |
| US04 | Filtro de Conformidade | Toggle na interface para filtrar apenas ativos que apresentam "Violação de Política". | Média |
| US05 | Menu de Navegação | Criar menu para separar as áreas de "Dashboard" e "Cadastro", exibindo o "Dashboard" como tela inicial por padrão. | Média |
| **US06** | **Log de Auditoria Imutável (Melhoria 1)** | **Como Auditor, quero que cada alteração no banco de dados seja registrada em um arquivo audit.log separado, contendo data, hora, usuário e a ação realizada, para garantir a rastreabilidade total.** | **Alta** |

## Regras de Governança e Segurança

### Regras de Negócio
- **Elegibilidade:** Apenas cargos "Sênior", "Lead" ou "Diretoria" podem receber "MacBook Pro". Níveis "Pleno" e "Júnior" recebem "Dell Latitude".
- **Teto Financeiro:** Periféricos com valor acima de **R$ 3.500,00** devem ser marcados com status "Pendente de Aprovação".
- **Geolocalização:** Ativos para funcionários em regime "Presencial" devem receber automaticamente a tag `[BH-OFFICE]`.
- **Restrição de Tipo:** Equipamentos de rede (Switches/Roteadores) só podem ser atribuídos a "Departamentos", nunca a pessoas físicas (CPFs).
- **Bloqueio de Deleção Condicional (Melhoria 2):** **Segurança: Impedir a exclusão de qualquer ativo que possua um valor de compra superior a R$ 0,00, exigindo um processo de 'Baixa' em vez de deleção física.**

### Segurança e Qualidade
- **Privacidade (LGPD):** Mascarar o CPF do colaborador na exibição (Ex: `***.456.***-99`).
- **Arquitetura:** As validações devem ser isoladas em um arquivo `validators.py` separado da camada de UI.
- **Integridade:** Impedir a deleção de ativos que possuam valor residual de compra superior a R$ 0,00.
