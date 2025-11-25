from sqlalchemy.orm import Session
from app.models.user import User
from app.models.ctf import CTFFlag
from app.crud.user import user_crud
from app.crud.benefit import benefit_crud
from app.crud.message import message_crud
from app.crud.log_event import log_event_crud
from app.crud import ctf as ctf_crud
from datetime import datetime, timedelta


def seed_database(db: Session):
    """Popula o banco com dados iniciais se estiver vazio"""
    
    # Verificar se já existe algum usuário
    existing_user = db.query(User).first()
    if existing_user:
        print("Banco de dados já contém dados. Seed não será executado.")
        return
    
    print("Iniciando seed do banco de dados...")
    
    # ========== USUÁRIOS ==========
    users_data = [
        {
            "nome": "Maria Santos",
            "email": "maria.santos@empresa.com.br",
            "username": "maria",
            "senha": "123456",
            "cpf": "123.456.789-00",
            "telefone": "(11) 98765-4321",
            "papel": "COLABORADOR",
            "dadosBancarios": {
                "banco": "Banco do Brasil",
                "agencia": "1234-5",
                "conta": "12345-6"
            }
        },
        {
            "nome": "João Silva",
            "email": "joao.silva@empresa.com.br",
            "username": "joao",
            "senha": "123456",
            "cpf": "987.654.321-00",
            "telefone": "(11) 91234-5678",
            "papel": "GESTOR_RH",
            "dadosBancarios": {
                "banco": "Itaú",
                "agencia": "5678-9",
                "conta": "98765-4"
            }
        },
        {
            "nome": "Ana Admin",
            "email": "ana.admin@empresa.com.br",
            "username": "admin",
            "senha": "admin123",
            "cpf": "456.789.123-00",
            "telefone": "(11) 93456-7890",
            "papel": "ADMIN",
            "dadosBancarios": {
                "banco": "Bradesco",
                "agencia": "2345-6",
                "conta": "23456-7"
            }
        },
        {
            "nome": "Carlos Oliveira",
            "email": "carlos.oliveira@empresa.com.br",
            "username": "carlos",
            "senha": "123456",
            "cpf": "789.123.456-00",
            "telefone": "(11) 94567-8901",
            "papel": "COLABORADOR",
            "dadosBancarios": {
                "banco": "Santander",
                "agencia": "3456-7",
                "conta": "34567-8"
            }
        },
        {
            "nome": "Fernanda Lima",
            "email": "fernanda.lima@empresa.com.br",
            "username": "fernanda",
            "senha": "123456",
            "cpf": "321.654.987-00",
            "telefone": "(11) 95678-9012",
            "papel": "COLABORADOR",
            "is_active": False,
            "dadosBancarios": {
                "banco": "Caixa Econômica",
                "agencia": "4567-8",
                "conta": "45678-9"
            }
        }
    ]
    
    print("Criando usuários...")
    users = []
    for user_data in users_data:
        user = user_crud.create(db, user_data)
        users.append(user)
        print(f"  - Criado: {user.name} ({user.username})")
    
    # ========== BENEFÍCIOS ==========
    benefits_data = [
        # Benefícios da Maria (id=1)
        {"userId": 1, "nome": "Vale Refeição", "categoria": "ALIMENTACAO", "status": "ATIVO", "valor": "R$ 1.200,00/mês", "descricao": "Vale refeição para alimentação diária"},
        {"userId": 1, "nome": "Plano de Saúde", "categoria": "SAUDE", "status": "ATIVO", "valor": "Cobertura completa", "descricao": "Plano de saúde empresarial com cobertura nacional"},
        {"userId": 1, "nome": "Vale Transporte", "categoria": "OUTROS", "status": "ATIVO", "valor": "R$ 300,00/mês", "descricao": "Vale transporte para deslocamento"},
        {"userId": 1, "nome": "Auxílio Home Office", "categoria": "OUTROS", "status": "ATIVO", "valor": "R$ 150,00/mês", "descricao": "Auxílio para custos de trabalho remoto"},
        
        # Benefícios do João (id=2)
        {"userId": 2, "nome": "Vale Refeição", "categoria": "ALIMENTACAO", "status": "ATIVO", "valor": "R$ 1.500,00/mês", "descricao": "Vale refeição para alimentação diária"},
        {"userId": 2, "nome": "Plano de Saúde Premium", "categoria": "SAUDE", "status": "ATIVO", "valor": "Cobertura completa + odontológico", "descricao": "Plano de saúde premium com cobertura ampliada"},
        {"userId": 2, "nome": "Auxílio Educação", "categoria": "OUTROS", "status": "ATIVO", "valor": "R$ 800,00/mês", "descricao": "Auxílio para cursos e capacitações"},
        {"userId": 2, "nome": "Seguro de Vida", "categoria": "OUTROS", "status": "ATIVO", "valor": "Cobertura de R$ 500.000", "descricao": "Seguro de vida em grupo"},
        
        # Benefícios da Ana (id=3)
        {"userId": 3, "nome": "Vale Refeição", "categoria": "ALIMENTACAO", "status": "ATIVO", "valor": "R$ 1.100,00/mês", "descricao": "Vale refeição para alimentação diária"},
        {"userId": 3, "nome": "Plano de Saúde", "categoria": "SAUDE", "status": "ATIVO", "valor": "Cobertura completa", "descricao": "Plano de saúde empresarial com cobertura nacional"},
        {"userId": 3, "nome": "Vale Transporte", "categoria": "OUTROS", "status": "SUSPENSO", "valor": "R$ 250,00/mês", "descricao": "Vale transporte para deslocamento"},
        
        # Benefícios do Carlos (id=4)
        {"userId": 4, "nome": "Vale Refeição", "categoria": "ALIMENTACAO", "status": "ATIVO", "valor": "R$ 1.200,00/mês", "descricao": "Vale refeição para alimentação diária"},
        {"userId": 4, "nome": "Plano de Saúde", "categoria": "SAUDE", "status": "ATIVO", "valor": "Cobertura completa", "descricao": "Plano de saúde empresarial com cobertura nacional"},
        
        # Benefícios da Fernanda (id=5)
        {"userId": 5, "nome": "Vale Refeição", "categoria": "ALIMENTACAO", "status": "SUSPENSO", "valor": "R$ 1.000,00/mês", "descricao": "Vale refeição para alimentação diária"},
    ]
    
    print("Criando benefícios...")
    for benefit_data in benefits_data:
        benefit = benefit_crud.create(db, benefit_data)
        print(f"  - Criado: {benefit.name} para user_id={benefit.user_id}")
    
    # ========== MENSAGENS ==========
    messages_data = [
        {
            "user_id": 1,
            "titulo": "Dúvida sobre Vale Refeição",
            "conteudo": "Olá, gostaria de saber se o valor do vale refeição será reajustado este ano. Obrigada!",
            "status": "PENDENTE"
        },
        {
            "user_id": 1,
            "titulo": "Atualização de dados bancários",
            "conteudo": "Preciso atualizar meus dados bancários. Como devo proceder?",
            "status": "EM_ANALISE"
        },
        {
            "user_id": 4,
            "titulo": "Solicitação de auxílio home office",
            "conteudo": "Gostaria de solicitar o auxílio home office, pois trabalho remotamente 3x na semana.",
            "status": "PENDENTE"
        }
    ]
    
    print("Criando mensagens...")
    for msg_data in messages_data:
        user_id = msg_data.pop("user_id")
        message = message_crud.create(db, msg_data, user_id)
        print(f"  - Criada: {message.title} de user_id={message.user_id}")
    
    # ========== LOGS ==========
    logs_data = [
        {
            "user_id": 1,
            "event_type": "LOGIN",
            "description": "Login realizado por Maria Santos"
        },
        {
            "user_id": 2,
            "event_type": "LOGIN",
            "description": "Login realizado por João Silva"
        },
        {
            "user_id": 3,
            "event_type": "LOGIN",
            "description": "Login realizado por Ana Admin"
        },
        {
            "user_id": 1,
            "event_type": "UPDATE_DATA",
            "description": "Maria Santos atualizou seus dados pessoais"
        },
        {
            "user_id": 1,
            "event_type": "NEW_MESSAGE",
            "description": "Maria Santos enviou mensagem: Dúvida sobre Vale Refeição"
        },
        {
            "user_id": 1,
            "event_type": "NEW_MESSAGE",
            "description": "Maria Santos enviou mensagem: Atualização de dados bancários"
        },
        {
            "user_id": 4,
            "event_type": "LOGIN",
            "description": "Login realizado por Carlos Oliveira"
        },
        {
            "user_id": 4,
            "event_type": "NEW_MESSAGE",
            "description": "Carlos Oliveira enviou mensagem: Solicitação de auxílio home office"
        },
        {
            "user_id": 3,
            "event_type": "CHANGE_ROLE",
            "description": "Papel de Carlos Oliveira alterado de COLABORADOR para COLABORADOR por Ana Admin"
        },
        {
            "user_id": None,
            "event_type": "LOGIN",
            "description": "Tentativa de login sem sucesso"
        }
    ]
    
    print("Criando logs...")
    for log_data in logs_data:
        log = log_event_crud.create(db, log_data)
        print(f"  - Criado: {log.event_type} - {log.description}")
    
    # ========== CTF FLAGS ==========
    print("Criando flags CTF...")
    
    # As flags reais que estão escondidas na aplicação
    flags = [
        # Flag Fácil - escondida no Footer.tsx
        {
            "flag": "FLAG{1nsp3ct_th3_d0m_345y}",
            "difficulty": "EASY",
            "points": 10,
            "hint": "Inspecione o rodapé da página. Use F12 ou botão direito > Inspecionar."
        },
        # Flag Média - escondida no endpoint /api/ctf/easter-egg
        {
            "flag": "FLAG{h1dd3n_3ndp01nt_m4st3r}",
            "difficulty": "MEDIUM",
            "points": 20,
            "hint": "Explore endpoints não documentados da API. Procure por 'easter-egg'."
        },
        # Flag Difícil - escondida no Home.tsx em base64
        {
            "flag": "FLAG{d3c0d3_b45364_h4rd_m0d3}",
            "difficulty": "HARD",
            "points": 30,
            "hint": "Verifique o código-fonte e o console do navegador. Algumas coisas estão codificadas."
        }
    ]
    
    from app.schemas.ctf import CTFFlagCreate, CTFDifficulty
    
    for flag_data in flags:
        flag_str = flag_data["flag"]
        flag_hash = ctf_crud.hash_flag(flag_str)
        
        flag_create = CTFFlagCreate(
            flag_hash=flag_hash,
            difficulty=CTFDifficulty(flag_data["difficulty"]),
            points=flag_data["points"],
            hint=flag_data["hint"],
            active=True
        )
        
        flag = ctf_crud.create_flag(db, flag_create)
        print(f"  - Criada: Flag {flag.difficulty.value} ({flag.points}pts)")
        print(f"    Real flag (para referência): {flag_str}")
    
    print("Seed concluído com sucesso!")

