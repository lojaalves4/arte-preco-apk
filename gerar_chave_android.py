from core.license_core import gerar_chave

cliente = input("Nome do cliente: ").strip()
device_id = input("ID do aparelho (o cliente envia): ").strip()
dias = int(input("Validade em dias (ex: 30 / 365): ").strip())

chave = gerar_chave(cliente, dias, device_id)

print("\nCHAVE GERADA (OFFLINE - POR APARELHO):")
print(chave)