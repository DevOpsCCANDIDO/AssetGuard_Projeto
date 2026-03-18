import json
import os
import random
from datetime import datetime, timedelta

DB_FILE = 'assets_data.json'
AUDIT_LOG = 'audit.log'

def log_audit(user, action, details):
    # Improvement 1: Log de Auditoria Imutável (US06)
    timestamp = datetime.now().strftime('%Y-%m-%d %H:%M:%S')
    log_entry = f"[{timestamp}] User: {user} | Action: {action} | Details: {details}\n"
    with open(AUDIT_LOG, 'a') as f:
        f.write(log_entry)

def load_data():
    if not os.path.exists(DB_FILE):
        return []
    with open(DB_FILE, 'r') as f:
        try:
            return json.load(f)
        except json.JSONDecodeError:
            return []

def save_data(data, user="System", action="Update"):
    with open(DB_FILE, 'w') as f:
        json.dump(data, f, indent=4)
    log_audit(user, action, f"Database updated. Total records: {len(data)}")

def generate_synthetic_data(user="System"):
    roles = ['Estagiário', 'Júnior', 'Pleno', 'Sênior', 'Lead', 'Diretoria']
    types = ['MacBook Pro', 'Dell Latitude', 'Switch', 'Roteador', 'Monitor', 'Teclado']
    departments = ['TI', 'RH', 'Financeiro', 'Vendas', 'Engenharia']
    regimes = ['Presencial', 'Remoto', 'Híbrido']
    
    data = []
    for i in range(50):
        is_violating = random.random() < 0.2
        role = random.choice(roles)
        asset_type = random.choice(types)
        value = random.uniform(500, 20000)
        regime = random.choice(regimes)
        
        asset = {
            "id": i + 1,
            "owner": f"User {i+1}",
            "cpf": f"123.456.{789 + i}-{i:02d}",
            "role": role,
            "type": asset_type,
            "category": "Periférico" if asset_type in ['Monitor', 'Teclado'] else "Hardware",
            "department": random.choice(departments),
            "value": round(value, 2),
            "regime": regime,
            "owner_type": "Pessoa Física",
            "status": "Ativo",
            "last_maintenance": (datetime.now() - timedelta(days=random.randint(0, 365))).strftime('%Y-%m-%d'),
            "tags": []
        }
        
        if not is_violating:
            if asset['type'] == 'MacBook Pro':
                asset['role'] = random.choice(['Sênior', 'Lead', 'Diretoria'])
            elif asset['type'] == 'Dell Latitude':
                asset['role'] = random.choice(['Pleno', 'Júnior'])
            if asset['type'] in ['Switch', 'Roteador']:
                asset['owner_type'] = 'Departamento'
                asset['owner'] = asset['department']
            if asset['regime'] == 'Presencial':
                asset['tags'].append('[BH-OFFICE]')
                
        data.append(asset)
    
    save_data(data, user, "Generate Synthetic Data")
    return data
