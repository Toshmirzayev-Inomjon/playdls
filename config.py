BOT_TOKEN = "8223820713:AAGtYE-4uRoqOw8rRdhwIrCCnKS_AMc95Ks"
ADMINS = [7795087338]

# Required channels for subscription (add your channel usernames or IDs here)
REQUIRED_CHANNELS = ["@InomjonToshmirzayev"]  # Example: ["@mychannel", -1001234567890]

MEDIA_PATH = "media/"
ORDERS_FILE = "orders.json"

# item mapping: key -> (display name, price, image file, long description)
ITEMS = {
    # Coins
    "coins_bundle": ("Bundle (Coins)", "35.000", "coins.jpg", "Bundle: qisqacha ta'rif..."),
    "coins_stack":  ("Stack (Coins)", "70.000", "coins.jpg", "Stack: qisqacha ta'rif..."),
    "coins_cup":    ("Cup (Coins)", "115.000", "coins.jpg", "Cup: qisqacha ta'rif..."),
    "coins_case":   ("Case (Coins)", "190.000", "coins.jpg", "Case: qisqacha ta'rif..."),
    "coins_locker": ("Locker (Coins)", "330.000", "coins.jpg", "Locker: qisqacha ta'rif..."),
    "coins_vault":  ("Vault (Coins)", "700.000", "coins.jpg", "Vault: qisqacha ta'rif..."),
    # Gems
    "gems_90":   ("90 Gems", "35.000", "gems.jpg", "90 Gems: qisqacha..."),
    "gems_400":  ("400 Gems", "130.000", "gems.jpg", "400 Gems: qisqacha..."),
    "gems_910":  ("910 Gems", "275.000", "gems.jpg", "910 Gems: qisqacha..."),
    "gems_2700": ("2700 Gems", "700.000", "gems.jpg", "2700 Gems: qisqacha..."),
    "gems_6000": ("6000 Gems", "1.600.000", "gems.jpg", "6000 Gems: qisqacha..."),
    # Season
    "season_sale":    ("Season Pass (Aksiya)", "25.000", "season pass.jpg", "Aksiya narxi: ..."),
    "season_normal":  ("Season Pass (Normal)", "38.000", "season pass.jpg", "Normal narxi: ..."),
    "season_premium": ("Season Pass (Premium)", "150.000", "season pass.jpg", "Premium: ..."),
    # Stadium / club / sticker
    "stadium_upgrade": ("Stadium Upgrade", "400.000", "stadium.jpg", "Stadionni yaxshilash..."),
    "club_info":       ("Dream Club", "—", "dream club.jpg", "Dream Club a'zo paketi..."),
    "sticker_buy":     ("Sticker", "50.000", "sitiker.jpg", "Stikerlar: ..."),
}
