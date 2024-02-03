# Importuri standard Python
import os
import json
import random
import asyncio
from io import BytesIO
from datetime import datetime, timedelta
from collections import Counter

# Importuri de terțe părți
import nextcord
import qrcode
import requests
from dotenv import load_dotenv
from pytz import timezone
from datetime import datetime


# Importuri Nextcord
from nextcord.ext import commands
from nextcord.ui import Button, View, Select

# Importuri locale (module specifice proiectului tău)
from skins import skinuri_samp
from masini import masini_samp




        

load_dotenv()
DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")

intents = nextcord.Intents.default()
intents.message_content = True
intents.members = True
intents.guilds = True
bot = commands.Bot(command_prefix="g.", intents=intents)












#cuvinte interzise
import json

def incarca_cuvinte_interzise():
    try:
        with open('cuvinte_interzise.json', 'r') as f:
            data = json.load(f)
            return data["cuvinte"]
    except FileNotFoundError:
        return []

def salveaza_cuvinte_interzise(cuvinte):
    with open('cuvinte_interzise.json', 'w') as f:
        json.dump({"cuvinte": cuvinte}, f, indent=4)


async def trimite_log(bot, titlu, descriere, canal_id, url_avatar=None, culoare=0x3498db):
    canal_loguri = bot.get_channel(canal_id)
    if canal_loguri:
        embed = nextcord.Embed(title=titlu, description=descriere, color=culoare)
        if url_avatar:  # Dacă este furnizat un URL pentru avatar, setează-l ca thumbnail
            embed.set_thumbnail(url=url_avatar)
        embed.set_footer(text="Log Bot")
        embed.timestamp = nextcord.utils.utcnow()
        await canal_loguri.send(embed=embed)
    else:
        print("Canalul de loguri nu a fost găsit.")



















@bot.event
async def on_message(message):
    if message.author.bot:
        return
    
    cuvinte_interzise = incarca_cuvinte_interzise()
    if any(cuvant.lower() in message.content.lower() for cuvant in cuvinte_interzise):
        try:
            mesaj_original = message.content  # Salvăm conținutul mesajului înainte de a-l șterge
            await message.delete()
            await message.channel.send(f"{message.author.mention}, mesajul tău conținea cuvinte interzise și a fost șters.")

            # Trimiterea logului pe canalul dedicat cu embed
            id_canal_loguri = 1202277836140838912 # Înlocuiește cu ID-ul real al canalului de loguri
            titlu_log = "Mesaj Șters pentru Cuvinte Interzise"
            descriere_log = f"Mesaj de la {message.author.mention} șters în {message.channel.mention}\nConținut: {mesaj_original}"
            await trimite_log(bot, titlu_log, descriere_log, id_canal_loguri, culoare=0xff0000)  # Culoare roșie pentru avertizare
        except nextcord.Forbidden:
            print("Nu am permisiuni pentru a șterge mesaje în acest canal.")
            # Trimitere log pentru eroare de permisiuni
            await trimite_log(bot, "Eroare de Permisiuni", "Nu am permisiuni pentru a șterge mesaje.", id_canal_loguri)

id_canal_loguri = 1202277836140838912 # Înlocuiește acest număr cu ID-ul real al canalului de loguri


@bot.slash_command(name="giverole", description="Oferă un rol unui membru")
@commands.has_permissions(manage_roles=True)
async def giverole(interaction: nextcord.Interaction, member: nextcord.Member, role: nextcord.Role):
    try:
        await member.add_roles(role)
        # Crează și trimite un embed de succes
        embed_succes = nextcord.Embed(
            title="Rol Adăugat cu Succes",
            description=f"Rolul **{role.name}** a fost adăugat membrului **{member.display_name}**.",
            color=0x00ff00
        )
        await interaction.response.send_message(embed=embed_succes)

        # Trimite logul către canalul de loguri
        descriere_log = f"Rolul **{role.name}** a fost adăugat membrului **{member.mention}** de către **{interaction.user.mention}**."
        await trimite_log(bot, "Rol Adăugat", descriere_log, id_canal_loguri)
    except Exception as e:
        # Crează și trimite un embed de eroare
        embed_eroare = nextcord.Embed(
            title="Eroare la Adăugarea Rolului",
            description=f"A apărut o eroare: {e}",
            color=0xff0000
        )
        await interaction.response.send_message(embed=embed_eroare)

        # Trimite logul de eroare către canalul de loguri
        descriere_log_eroare = f"Eroare la adăugarea rolului **{role.name}** membrului **{member.mention}** de către **{interaction.user.mention}**: {e}"
        await trimite_log(bot, "Eroare Rol Adăugat", descriere_log_eroare, id_canal_loguri)
#logs event
@bot.event
async def on_user_update(before, after):
    if before.avatar != after.avatar:
        descriere_log = f"{after.mention} și-a schimbat avatarul."
        url_avatar = str(after.avatar.url) if after.avatar else "URL implicit pentru avatarul lipsă"
        await trimite_log(bot, "Schimbare Avatar", descriere_log, id_canal_loguri, url_avatar=url_avatar)

@bot.event
async def on_message_delete(message):
    if not message.author.bot:  # Ignoră mesajele șterse de bot
        descriere_log = f"Mesaj șters în {message.channel.mention} de către {message.author.mention}: {message.content}"
        url_avatar = str(message.author.avatar.url) if message.author.avatar else "URL implicit pentru avatarul lipsă"
        await trimite_log(bot, "Mesaj Șters", descriere_log, id_canal_loguri, url_avatar=url_avatar)

@bot.event
async def on_message_edit(before, after):
    if not after.author.bot:  # Ignoră mesajele editate de bot
        if before.content != after.content:  # Verifică dacă conținutul mesajului s-a schimbat
            descriere_log = f"Mesaj editat în {after.channel.mention} de către {after.author.mention}\nÎnainte: {before.content}\nDupă: {after.content}"
            url_avatar = str(after.author.avatar.url) if after.author.avatar else "URL implicit pentru avatarul lipsă"
            await trimite_log(bot, "Mesaj Editat", descriere_log, id_canal_loguri, url_avatar)





@bot.event
async def on_ready():
    servers_count = len(bot.guilds)
    activity = nextcord.Game(name=f"pe {servers_count} servere")
    await bot.change_presence(activity=activity)
    
    print(f"Logged in as {bot.user.name} ({bot.user.id})")
    print("------")

#comanda de avatar

@bot.slash_command(name="avatar", description="Arată avatarul tău sau al altui membru")
async def avatar(ctx, member: nextcord.Member = None):
    member = member or ctx.author

    avatar_url = member.avatar.url if member.avatar else member.default_avatar.url

    embed = nextcord.Embed(title=f"Avatarul lui {member.display_name}", color=nextcord.Color.blurple())
    embed.set_image(url=avatar_url)

    await ctx.send(embed=embed)

#comanda de ping

@bot.slash_command(name="ping", description="Verifică ping-ul botului")
async def ping(ctx):
    latency = bot.latency * 1000  # Convertim la milisecunde
    await ctx.send(f"Pong! Ping-ul botului este: {latency:.2f}ms")

@bot.slash_command(name="online", description="Afișează membrii online în server")
async def online_members(ctx):
    online_members = [member.name for member in ctx.guild.members if member.status == nextcord.Status.online]

    if online_members:
        online_list = "\n".join(online_members)
        embed = nextcord.Embed(
            title="Membri Online",
            description=f"Membri online în {ctx.guild.name}:\n{online_list}",
            color=0x00ff00  # Culoare verde
        )
    else:
        embed = nextcord.Embed(
            title="Membri Online",
            description=f"Niciun membru online în {ctx.guild.name} în acest moment.",
            color=0xff0000  # Culoare roșie
        )

    await ctx.send(embed=embed)





#comanda de post

@bot.command(name='post', description='Copiază un mesaj într-un alt canal.')
async def copiapost_command(ctx, canal_destinatie: nextcord.TextChannel, *, mesaj_de_copiat):
    if not mesaj_de_copiat and not ctx.message.attachments:
        await ctx.send("Vă rugăm să furnizați cel puțin un mesaj sau să încărcați o imagine.")
        return

    try:
        embed = nextcord.Embed(description=mesaj_de_copiat, color=0x3498db)

        embed.set_author(name=ctx.author.display_name, icon_url=ctx.author.avatar.url)

        if ctx.message.attachments:
            # Verificăm dacă există atașamente (imagini)
            image_url = None
            for attachment in ctx.message.attachments:
                if attachment.url.endswith(('png', 'jpeg', 'jpg', 'gif')):
                    image_url = attachment.url
                    break

            if image_url:
                # Dacă avem o imagine validă, o adăugăm la embed
                embed.set_image(url=image_url)

        await canal_destinatie.send(embed=embed)
    except nextcord.Forbidden:
        await ctx.send("Nu am permisiuni pentru a trimite mesaje în canalul specificat.")
    except nextcord.HTTPException:
        await ctx.send("A apărut o eroare în timpul copierii mesajului sau încărcării imaginii.")

#comanda de ban si unban

@bot.slash_command(name='ban', description='Interzice un membru.')
@commands.has_permissions(ban_members=True)
async def ban(ctx, member: nextcord.Member, *, reason="Fără motiv specificat."):
    await member.ban(reason=reason)
    await ctx.send(f"{member.mention} a fost interzis. Motiv: {reason}")

@ban.error
async def ban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Nu aveți permisiuni pentru a interzice membrii.")

@bot.slash_command(name='unban', description='Deblochează un membru.')
@commands.has_permissions(ban_members=True)
async def unban(ctx, member: str):
    banned_users = await ctx.guild.bans()
    member_name, member_discriminator = member.split('#')

    for entry in banned_users:
        user = entry.user
        if (user.name, user.discriminator) == (member_name, member_discriminator):
            await ctx.guild.unban(user)
            await ctx.send(f"{user.mention} a fost deblocat.")

@unban.error
async def unban_error(ctx, error):
    if isinstance(error, commands.MissingPermissions):
        await ctx.send("Nu aveți permisiuni pentru a debloca membrii.")

#commanda de cautat skinuri



#comanda pentru masini
    
@bot.slash_command(name='car' , description="cauta detali despre masina")
async def masina_info(ctx, masina_dorita):
    masina_dorita= masina_dorita.lower()
    vehicle_name   = ""
    id_masina = ""
    url_imagine = ""
    category = ""
    modifications = ""
    model_name = ""
    num_seats = ""

    if masina_dorita in masini_samp:
        mașină = masini_samp[masina_dorita]
        id_masina = mașină["id"]
        url_imagine = mașină["imagine"]
        vehicle_name = masina_dorita.capitalize()
        category = "Categorie: " + mașină.get("categoria", "Nedeterminată")
        modifications = "Modificări: " + mașină.get("modificari", "Niciuna")
        model_name = "Model name: " + mașină.get("model_name", masina_dorita)
        num_seats = "Number of seats: " + str(mașină.get("numar_scaune", 2))

    elif masina_dorita.isdigit():
        for nume, detalii_masina in masini_samp.items():
            if str(detalii_masina["id"]) == masina_dorita:
                vehicle_name = nume.capitalize()
                id_masina = detalii_masina["id"]
                url_imagine = detalii_masina.get("imagine", "")
                category = "Categorie: " + detalii_masina.get("categoria", "Nedeterminată")
                modifications = "Modificări: " + detalii_masina.get("modificari", "Niciuna")
                model_name = "Model name: " + detalii_masina.get("model_name", nume)
                num_seats = "Number of seats: " + str(detalii_masina.get("numar_scaune", 2))
                break

    if vehicle_name:
        embed = nextcord.Embed(title=f"Vehicle Model ID: {id_masina}", color=0x3498db)
        embed.set_image(url=url_imagine)
        embed.add_field(name="Vehicle Name", value=vehicle_name)
        embed.add_field(name="Category", value=category)
        embed.add_field(name="Modifications", value=modifications)
        embed.add_field(name="Model name", value=model_name)
        embed.add_field(name="Number of seats", value=num_seats)

        await ctx.send(embed=embed)
    else:
        await ctx.send(f"Nu am putut găsi mașina cu numele sau ID-ul '{masina_dorita}'.")    
#comanda de lock si unlock

@bot.slash_command(name='lock')
@commands.has_permissions(manage_channels=True)
async def lock_channel(ctx, channel: nextcord.TextChannel = None):
    channel = channel or ctx.channel
    await channel.set_permissions(ctx.guild.default_role, send_messages=False)
    await ctx.send(f"Canalul {channel.mention} a fost blocat.")

@bot.slash_command(name='unlock')
@commands.has_permissions(manage_channels=True)
async def unlock_channel(ctx, channel: nextcord.TextChannel = None):
    channel = channel or ctx.channel
    await channel.set_permissions(ctx.guild.default_role, send_messages=True)
    await ctx.send(f"Canalul {channel.mention} a fost deblocat.")
      




@bot.slash_command(name="calc", description="calculeaza diferite calcule")
async def calculate(ctx, *, expression: str):
    try:
        result = eval(expression)
        await ctx.send(f"Rezultat: {result}")
    except Exception as e:
        await ctx.send(f"A apărut o eroare în timpul calculului: {e}")





#welcome settings

# Încarcă sau inițializează setările de welcome
def load_welcome_settings():
    try:
        with open("welcome_settings.json", "r") as file:
            return json.load(file)
    except FileNotFoundError:
        return {"channel_id": None, "welcome_message": "Bine ai venit, {member}!"}

welcome_settings = load_welcome_settings()

# Salvează setările de welcome
def save_welcome_settings():
    with open("welcome_settings.json", "w") as file:
        json.dump(welcome_settings, file, indent=4)

@bot.slash_command(name="setwelcome", description="seteaza cnalul de welcome")
@commands.has_permissions(administrator=True)
async def set_welcome(ctx, channel: nextcord.TextChannel, *, welcome_message: str):
    welcome_settings["channel_id"] = channel.id
    welcome_settings["welcome_message"] = welcome_message
    save_welcome_settings()
    await ctx.send(f"Canalul de welcome a fost setat la {channel.mention} cu mesajul: \"{welcome_message}\"")

@bot.event
async def on_member_join(member):
    channel_id = welcome_settings.get("channel_id")
    if channel_id:
        channel = bot.get_channel(channel_id)
        if channel:
            welcome_message = welcome_settings["welcome_message"].format(member=member.mention)
            await channel.send(welcome_message)




#dugesti

# Încărcarea comenzilor
initial_extensions = ['commands.feedback', 'commands.dice','commands.pacanele','commands.clear','commands.tickets','commands.serverinfo','commands.setwords','commands.help','commands.cautaskin']

if __name__ == '__main__':
    for extension in initial_extensions:
        bot.load_extension(extension)


@bot.slash_command(name="showcontent", description="Afișează un embed personalizat cu imagine, text și un link opțional.")
async def show_content(
    interaction: nextcord.Interaction,
    image_url: str,
    text: str,
    link_url: str = ""  # Acest argument este opțional
):
    # Creează un embed cu textul furnizat
    embed = nextcord.Embed(title="Announces", description=text, color=0x3498db)
    
    # Verifică și adaugă imaginea dacă URL-ul este valid
    if image_url.startswith("http://") or image_url.startswith("https://"):
        embed.set_image(url=image_url)
    else:
        await interaction.response.send_message("URL-ul imaginii nu este valid. Folosind doar textul.")
        return

    # Creează o vizualizare pentru buton dacă este furnizat un link URL valid
    if link_url.startswith("http://") or link_url.startswith("https://"):
        button = Button(label="Mai multe informații", url=link_url, style=nextcord.ButtonStyle.url)
        view = View()
        view.add_item(button)
        await interaction.response.send_message(embed=embed, view=view)
    else:
        # Dacă nu este furnizat un link URL valid, trimite doar embed-ul
        await interaction.response.send_message(embed=embed)






bot.run(DISCORD_TOKEN)
