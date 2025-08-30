import ast
import json
import os
import threading
from time import sleep

from azure.core.exceptions import HttpResponseError, ResourceNotFoundError
from dotenv import load_dotenv, set_key, find_dotenv
from azure.keyvault.secrets import SecretClient
from azure.identity import DefaultAzureCredential

try:
    from Resources.AzureCloud.Constants import KV_URI, COLOR_CODES, ANIMATION, SECRET_KEYS, BANNER, MESSAGE
except ModuleNotFoundError:
    import pathlib
    import sys

    sys.path.append(str(pathlib.Path(__file__).parent.parent.parent))
    from Resources.AzureCloud.Constants import KV_URI, COLOR_CODES, ANIMATION, SECRET_KEYS, BANNER, MESSAGE

is_loading = True


def initialize_key_vault_client():
    """Initialize the Azure Key Vault client."""
    credential = DefaultAzureCredential()
    return SecretClient(vault_url=KV_URI, credential=credential)


def display_banner():
    """Display the application banner."""
    print(BANNER)


def execute_loader():
    """
    Async execute the loader for user experience loading
    Returns:
        None
    """
    thread = threading.Thread(target=loader,
                              args=())
    thread.daemon = True
    thread.start()


def loader():
    """
    prints a yellow loader like this [loading ]
    Returns:
        None
    """
    i = 0
    while is_loading:
        print(f"{COLOR_CODES['YELLOW']} {ANIMATION[i % len(ANIMATION)]} {COLOR_CODES['END']} ", end='\r')
        sleep(.1)
        i += 1
        if i == len(ANIMATION) - 1:
            i = 0


def confirm_update():
    """Prompt the user for confirmation to update secrets."""
    index = 0
    for _ in range(3):
        response = input(MESSAGE[index])
        index += 1
        if response.upper() != 'Y':
            return False
    return True


def update_key_vault_secrets(client):
    """
    Update secrets in the Azure Key Vault.

    Args:
        client: Azure client, that will be auth using AZURE CLI

    Returns:
        None
    """
    updated_values = []
    load_dotenv()

    for key in SECRET_KEYS:
        key_value = os.getenv(key)
        if key_value:
            key_value = ast.literal_eval(key_value)['password']
            try:
                value_in_keyvault = client.get_secret(key).value
            except:
                value_in_keyvault = None
            if key_value != value_in_keyvault:
                try:
                    client.set_secret(key, key_value)
                    updated_values.append(key)
                except HttpResponseError as e:
                    print(f"{COLOR_CODES['RED']}You are not member of the core team, so you shouldn't perform this "
                          f"action{COLOR_CODES['END']}, \n details: {e.message}")
                    return None

    if updated_values:
        print(f"The secrets {updated_values} were updated in the keyvault.")
    else:
        print("No secrets were updated.")


def update_local_env_file(client):
    """
    Update secrets in the .env from the key vault.

    Args:
        client: Azure client, that will be auth using AZURE CLI

    Returns:
        None
    """
    dotenv_file = find_dotenv()
    load_dotenv(dotenv_file)

    for key in SECRET_KEYS:
        if os.getenv(key):
            actual_value = ast.literal_eval(os.environ[key])
            try:
                actual_value['password'] = client.get_secret(key).value
            except ResourceNotFoundError:
                print(f"{COLOR_CODES['YELLOW']} ⚠ WARN the {key} secret is not in the keyvault so was not updated in the .env{COLOR_CODES['END']}")
            set_key(dotenv_path=dotenv_file, key_to_set=key,
                    value_to_set=json.dumps(actual_value).replace('"', "'"), quote_mode="never")

    print("Your .env file was updated with the values from the keyvault!")


def main():
    display_banner()
    confirm_update_var = confirm_update()
    client = initialize_key_vault_client()
    execute_loader()
    if confirm_update_var:
        update_key_vault_secrets(client)
    else:
        update_local_env_file(client)
    is_loading = False


if __name__ == "__main__":
    main()
