import os
import re
import time
import google.genai as genai
from google.api_core import exceptions
from dotenv import load_dotenv

# 1. Carrega as variáveis do arquivo .env (Onde deve estar sua GEMINI_API_KEY)
load_dotenv()

# 2. Configura a API usando a chave do Google AI Studio confirmada em sua imagem
gemini_key = os.getenv("GEMINI_API_KEY")

def initialize_model():
    """Inicializa o modelo Gemini 1.5 Flash para análise de conformidade."""
    if not gemini_key:
        return None
    try:
        genai.configure(api_key=gemini_key)
        # O modelo Flash é o mais indicado para processamento de logs e regras de texto
        return genai.GenerativeModel('gemini-2.5-flash')
    except Exception as e:
        print(f"Erro ao conectar com a API do Google: {e}")
        return None

# Instância global do modelo
model = initialize_model()

def load_governance_rules():
    """Lê o blueprint para que a IA conheça as regras de MacBooks, Redes e Valores."""
    path = 'blueprint_NOVO.md'
    if not os.path.exists(path):
        return "Atue como um analista de segurança. Regras: MacBooks apenas para Sênior/Lead/Diretoria."
    try:
        with open(path, 'r', encoding='utf-8') as f:
            return f.read()
    except Exception:
        return "Erro ao acessar o arquivo de regras."

def mask_sensitive_data(text):
    """Protege dados sensíveis antes de enviar para a nuvem (LGPD)."""
    # Mascara IPs internos
    text = re.sub(r'\b10\.\d{1,3}\.\d{1,3}\.\d{1,3}\b', '10.0.***.***', text)
    # Mascara possíveis senhas no texto
    text = re.sub(r'(?i)(password|pass|senha|token)\s*[:=]\s*[^\s]+', r'\1=***', text)
    return text

def analyze_compliance(asset_data, retries=2):
    """
    Envia os dados do ativo para a IA validar se há violações de governança.
    Implementa retry para lidar com limites de cota da conta gratuita.
    """
    if not model:
        return "⚠️ Erro: IA não inicializada. Verifique o GEMINI_API_KEY no arquivo .env."

    rules = load_governance_rules()
    clean_data = mask_sensitive_data(str(asset_data))
    
    prompt = f"""
    Você é o Auditor de IA do sistema AssetGuard.
    Siga estas REGRAS DE GOVERNANÇA:
    {rules}
    
    TAREFA:
    Analise o registro de ativo abaixo e verifique se ele viola as regras:
    - Verifique se MacBooks estão indo para cargos Sênior/Lead/Diretoria.
    - Verifique se Equipamentos de Rede estão indo para Departamentos (não CPFs).
    - Verifique se o valor do periférico exige aprovação (> R$ 3500).
    
    REGISTRO PARA ANÁLISE:
    {clean_data}
    
    RETORNE:
    1. STATUS: (Aprovado ou Violação Detectada)
    2. MOTIVO: (Explique qual regra do blueprint foi afetada)
    3. SEVERIDADE: (Baixa, Média ou Alta)
    """
    
    for i in range(retries + 1):
        try:
            response = model.generate_content(prompt)
            return response.text
        except exceptions.ResourceExhausted:
            if i < retries:
                time.sleep(10) # Pausa de segurança para a cota gratuita
                continue
            return "❌ Cota de IA excedida. Tente novamente em 1 minuto."
        except Exception as e:
            return f"❌ Erro na comunicação com Gemini: {str(e)}"