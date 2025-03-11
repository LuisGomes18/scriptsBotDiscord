# Command untimeout
# Exemplo: /untimeout <usuário> <motivo>
# Linguagem usada: py
# Author: Luis Gomes

import discord
from discord.ext import commands
from discord import app_commands
import datetime

intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    print(f'Bot conectado como {bot.user}')
    try:
        synced = await bot.tree.sync()
        print(f'Slash commands sincronizados: {len(synced)} comandos')
    except Exception as e:
        print(f'Erro ao sincronizar slash commands: {e}')

@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, commands.CommandNotFound):
        await ctx.send('Comando não encontrado.')
    elif isinstance(error, commands.MissingPermissions):
        await ctx.send('Você não tem permissão para dar desmute membros.')
    elif isinstance(error, commands.BadArgument):
        await ctx.send('Use um ID válido para dar desmute um usuário.')
    else:
        await ctx.send(f'Ocorreu um erro: {error}')

@bot.tree.command(name='untimeout', description='Desmutar um usuario')
@app_commands.describe(usuario='Usuário que será desmutado', motivo='Motivo do desmute')
@commands.has_permissions(moderate_members=True)
async def timeout(interaction: discord.Interaction, usuario: discord.Member, motivo: str):
    try:
        await usuario.edit(timed_out_unitl=None)
        await interaction.response.send_message(f'{usuario.mention} teve o timeout removido')
    except discord.Forbidden:
        await interaction.response.send_message('Não tenho permissão para remover o timeout desse usuário.')
    except discord.HTTPException:
        await interaction.response.send_message('Ocorreu um erro ao tentar remove o timeout do usuário.')
    except Exception as error:
        await interaction.response.send_message(f'Ocorreu um erro: {error}')

bot.run('TOKEN')
