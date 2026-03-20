import re
import math

def validate_asset(data):
    """
    Valida um ativo contra as regras de governança do AssetGuard.
    Retorna (is_valid, reason, updated_data)
    """
    errors = []
    updated_data = data.copy()
    
    # 1. Regra de Elegibilidade (Sênior/Lead/Diretoria -> MacBook Pro)
    role = data.get('role', '')
    asset_name = data.get('asset_name', '')
    if "MacBook Pro" in asset_name:
        if role not in ["Sênior", "Lead", "Diretoria"]:
            errors.append(f"Elegibilidade: {role} não pode receber MacBook Pro. Apenas Sênior, Lead ou Diretoria.")
    elif "Dell Latitude" in asset_name:
         if role in ["Sênior", "Lead", "Diretoria"]:
            # Nota: O blueprint foca na restrição do MacBook, mas implica a divisão de categorias.
            pass

    # 2. Teto Financeiro para Periféricos
    value = float(data.get('value', 0))
    asset_type = data.get('asset_type', '')
    if asset_type == "Periférico" and value > 3500.00:
        updated_data['status'] = "Pendente de Aprovação"
        # Não bloqueia o salvamento, apenas altera o status conforme regra.

    # 3. Geolocalização Automática (Regime)
    regime = data.get('regime', '')
    tags = data.get('tags', [])
    if isinstance(tags, str): tags = [tags] # Garante que seja lista
    
    if regime == "Presencial" and "[BH-OFFICE]" not in tags:
        tags.append("[BH-OFFICE]")
    elif regime == "Remoto" and "[HOME-OFFICE]" not in tags:
        tags.append("[HOME-OFFICE]")
    updated_data['tags'] = tags

    # 4. Restrição de Tipo (Equipamentos de Rede)
    if asset_type in ["Switch", "Roteador"]:
        assigned_to = data.get('assigned_to', '')
        # Verifica se o que foi preenchido parece um CPF (contém números)
        if any(char.isdigit() for char in assigned_to):
            errors.append("Restrição: Equipamentos de rede só podem ser atribuídos a Departamentos, não a CPFs.")

    # 5. Integridade: Deleção (Lógica será usada no data_service, mas a regra reside aqui)
    # Impedir deleção se valor > 0
    
    is_valid = len(errors) == 0
    reason = " | ".join(errors) if errors else "Conforme"
    
    return is_valid, reason, updated_data

def mask_cpf(cpf):
    """Aplica máscara LGPD no CPF: ***.456.***-99

    Trata casos onde `cpf` pode ser `NaN` (float), `None`, números ou strings.
    Retorna o valor original quando não for possível aplicar a máscara.
    """
    # Preserve None
    if cpf is None:
        return cpf

    # Handle pandas NaN (float('nan'))
    if isinstance(cpf, float):
        try:
            if math.isnan(cpf):
                return cpf
        except Exception:
            return cpf

    # Convert to string for processing
    s = str(cpf)
    # If empty after conversion, return original
    if not s or s.lower() == 'nan':
        return cpf

    # Remove non-numeric characters and mask when we have 11 digits
    clean_cpf = re.sub(r'\D', '', s)
    if len(clean_cpf) == 11:
        return f"***.{clean_cpf[3:6]}.***-{clean_cpf[9:]}"

    return cpf