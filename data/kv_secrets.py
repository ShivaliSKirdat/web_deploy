import os
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

VAULT_URL = os.environ["https://demo-web-key.vault.azure.net/"]
credential = DefaultAzureCredential()
client = SecretClient(vault_url=VAULT_URL, credential=credential)

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()

secret_client = SecretClient(vault_url="https://my-key-vault.vault.azure.net/", credential=credential)
secret = secret_client.get_secret("user")
secret = secret_client.get_secret("password")

print(secret.name)
print(secret.value)
