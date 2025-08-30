KEY_VAULT_NAME = "EUWDCANTNSAKV01"
KV_URI = f"https://{KEY_VAULT_NAME}.vault.azure.net"
SECRET_KEYS = [
    "CanvasAutomationUser1",
    "CanvasAutomationUser2",
    "CanvasAutomationUser3",
    "CanvasAutomationUser4",
    "CanvasAutomationUser5",
    "CanvasAutomationUser6",
    "CanvasAutomationUser7",
    "CanvasAutomationUser8",
    "CanvasAutomationUser9",
    "CanvasAutomationUser10",
    "CanvasAutomationUser11",
    "CanvasAutomationUser12",
    "CanvasAutomationUser13",
    "CanvasAutomationUser14",
    "CanvasAutomationUser15",
    "LTCanvasAutomationUser1",
    "LTCanvasAutomationUser1",
    "LTCanvasAutomationUser2",
    "LTCanvasAutomationUser3",
    "LTCanvasAutomationUser4",
    "LTCanvasAutomationUser5",
    "LTCanvasAutomationUser6",
    "LTCanvasAutomationUser10",
    "LTCanvasAutomationUser11",
    "LTCanvasAutomationUser12",
    "LTCanvasAutomationUser13",
    "LTCanvasAutomationUser14",
    "LTCanvasAutomationUser15"
]

# Color codes for terminal output
COLOR_CODES = {
    "RED": "\33[91m",
    "BLUE": "\33[94m",
    "GREEN": "\033[32m",
    "YELLOW": "\033[93m",
    "PURPLE": '\033[0;35m',
    "CYAN": "\033[36m",
    "END": "\033[0m"
}

ANIMATION = [
    "[g       ]",
    "[ng      ]",
    "[ing     ]",
    "[ding    ]",
    "[ading   ]",
    "[oading  ]",
    "[loading ]",
    "[ loading]",
    "[  loadin]",
    "[   loadi]",
    "[    load]",
    "[      lo]",
    "[       l]",
    "[        ]"
]

BANNER = f"""
      {COLOR_CODES['YELLOW']}   
      🚧 🔐                                                     🔐 🚧
        '  ┏┓┏┓┳┓┓┏┏┓┏┓  ┏┓┳┳┏┳┓┏┓┳┳┓┏┓┏┳┓┳┏┓┳┓  ┏┓┏┓┏┓┳┓┏┓┏┳┓┏┓
        '  ┃ ┣┫┃┃┃┃┣┫┗┓  ┣┫┃┃ ┃ ┃┃┃┃┃┣┫ ┃ ┃┃┃┃┃  ┗┓┣ ┃ ┣┫┣  ┃ ┗┓
        '  ┗┛┛┗┛┗┗┛┛┗┗┛  ┛┗┗┛ ┻ ┗┛┛ ┗┛┗ ┻ ┻┗┛┛┗  ┗┛┗┛┗┛┛┗┗┛ ┻ ┗┛
        '  
      🚧 🔐                                                     🔐 🚧                                                                
        {COLOR_CODES['END']}  
      """

MESSAGE = [
    "Do you want to update the secrets in the keyvault? Y/N (press enter to update your local .env): ",
    f"{COLOR_CODES['YELLOW']} WARNING!{COLOR_CODES['END']} are you 100% sure to update the secrets in the keyvault? Y/N (press enter to update your local .env): ",
    f" ⚠{COLOR_CODES['YELLOW']} FINAL WARNING! {COLOR_CODES['END']}⚠ {COLOR_CODES['CYAN']}(This will update with your .env "
    f"the keyvault user password values, that the pipeline and the team are using){COLOR_CODES['END']} \n👮🚨 are you 100% sure "
    f"to update the secrets in the keyvault? Y/N (press enter to update your local .env): ",

]
