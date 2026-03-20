import streamlit as st
import pandas as pd
from datetime import datetime
import os
import data_service
import validators
import agent_core
import email_service

# Configuração da página conforme US05
st.set_page_config(page_title="AssetGuard - Governança de TI", layout="wide")

# Inicialização de sessão para o Mock Auth
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
    st.session_state.user_role = None

def login():
    st.title("🔐 AssetGuard - Login")
    user = st.text_input("Usuário")
    role = st.selectbox("Nível de Acesso", ["Admin", "Manager", "Staff"])
    if st.button("Entrar"):
        st.session_state.authenticated = True
        st.session_state.user_role = role
        st.session_state.user_name = user
        st.rerun()

if not st.session_state.authenticated:
    login()
else:
    # Menu de Navegação conforme US05
    st.sidebar.title(f"👤 {st.session_state.user_name}")
    st.sidebar.write(f"Nível: {st.session_state.user_role}")
    menu = st.sidebar.radio("Navegação", ["Dashboard", "Cadastro de Ativos", "Log de Auditoria"])
    
    if st.sidebar.button("Sair"):
        st.session_state.authenticated = False
        st.rerun()

    # --- ABA: DASHBOARD (US01 e US04) ---
    if menu == "Dashboard":
        st.title("📊 Dashboard de Inventário")
        
        data = data_service.load_data()
        if not data:
            st.warning("Nenhum dado encontrado. Vá em Cadastro para gerar dados sintéticos ou adicionar um ativo.")
        else:
            df = pd.DataFrame(data)
            
            # Filtro de Conformidade conforme US04
            show_violations = st.toggle("Filtrar apenas Violações de Política")
            if show_violations and 'compliance_violation' in df.columns:
                df = df[df['compliance_violation'] == True]

            # CORREÇÃO DO KEYERROR: Verifica se a coluna existe antes de aplicar a máscara
            df_display = df.copy()
            if 'assigned_to' in df_display.columns:
                df_display['assigned_to'] = df_display['assigned_to'].apply(validators.mask_cpf)
            
            st.dataframe(df_display, width='stretch')

            # Análise da IA Gemini sobre o estado atual
            if st.button("🤖 Solicitar Análise de Segurança da IA"):
                with st.spinner("O Gemini está analisando o inventário..."):
                    # Envia os dados mascarados para a IA
                    feedback = agent_core.analyze_compliance(data[:15]) 
                    st.info(feedback)

    # --- ABA: CADASTRO (US02, US03 e US07) ---
    elif menu == "Cadastro de Ativos":
        st.title("📝 Gestão de Ativos")
        
        # Botão para US03: Gerar 50 registros
        if st.button("⚡ Gerar 50 Dados Sintéticos (Reset de Banco)"):
            data_service.generate_synthetic_data(st.session_state.user_name)
            st.success("Dados gerados com sucesso! Verifique o Dashboard.")
            st.rerun()

        st.divider()
        st.subheader("Novo Cadastro")
        
        with st.form("asset_form"):
            col1, col2 = st.columns(2)
            asset_name = col1.text_input("Nome do Ativo (ex: MacBook Pro)")
            asset_type = col2.selectbox("Tipo", ["Notebook", "Periférico", "Switch", "Roteador"])
            value = col1.number_input("Valor (R$)", min_value=0.0)
            role_assigned = col2.selectbox("Cargo do Responsável", ["Sênior", "Lead", "Diretoria", "Pleno", "Júnior"])
            assigned_to = col1.text_input("Atribuído a (CPF ou Departamento)")
            regime = col2.selectbox("Regime", ["Presencial", "Remoto"])
            
            submitted = st.form_submit_button("Salvar Ativo")
            
            if submitted:
                new_asset = {
                    "id": len(data_service.load_data()) + 1,
                    "asset_name": asset_name,
                    "asset_type": asset_type,
                    "value": value,
                    "role": role_assigned,
                    "assigned_to": assigned_to,
                    "regime": regime,
                    "status": "Ativo",
                    "acquisition_date": datetime.now().strftime("%Y-%m-%d")
                }
                
                # Validação contra Regras de Governança
                is_valid, reason, final_data = validators.validate_asset(new_asset)
                final_data["compliance_violation"] = not is_valid
                
                # Salva e registra auditoria
                current_data = data_service.load_data()
                current_data.append(final_data)
                # data_service.save_data(current_data, st.session_state.user_name, "INSERT", f"Ativo {asset_name} adicionado.")
                data_service.save_data(data=current_data, user=st.session_state.user_name, action="INSERT", message=f"Ativo {asset_name} adicionado.")
                
                # US07: Envio de E-mail
                email_service.send_inventory_email("Inserido", final_data)
                
                if is_valid:
                    st.success("Ativo cadastrado e notificação enviada!")
                else:
                    st.warning(f"Ativo cadastrado com VIOLAÇÃO: {reason}")
                st.rerun()

    # --- ABA: LOG DE AUDITORIA (US06) ---
    elif menu == "Log de Auditoria":
        st.title("📜 Log de Auditoria Imutável")
        
        if os.path.exists('audit.log'):
            with open('audit.log', 'r', encoding='utf-8') as f:
                logs = f.readlines()
                for log in reversed(logs):
                    st.text(log.strip())
        else:
            st.info("Nenhum log registrado ainda.")