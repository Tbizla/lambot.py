import os

from utils import default
from utils.data import Bot
from utils.data import HelpFormat

config = default.get("config.json")
print("Booting the matrix...")

bot = Bot(
    command_prefix=config.prefix,
    prefix=config.prefix,
    command_attrs=dict(hidden=True),
    help_command=HelpFormat()
)

for file in os.listdir("cogs"):
    if file.endswith(".py"):
        name = file[:-3]
        bot.load_extension(f"cogs.{name}")


bot.run(config.token)
