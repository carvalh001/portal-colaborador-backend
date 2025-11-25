import secrets

# Gerar SECRET_KEY de 32 bytes (64 caracteres hexadecimais)
secret_key = secrets.token_hex(32)

print("=" * 70)
print("🔑 SECRET_KEY gerada com sucesso!")
print("=" * 70)
print()
print("Cole esta chave no Railway (variável SECRET_KEY):")
print()
print(secret_key)
print()
print("=" * 70)