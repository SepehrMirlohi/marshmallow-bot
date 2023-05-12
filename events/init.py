import os, sys
from dotenv import load_dotenv
load_dotenv()
path = os.path.dirname(os.path.dirname(__file__))
sys.path.insert(0, path)


from lib.config import *
from lib.invite import *

import discord

from discord.ext import commands

from discord import app_commands