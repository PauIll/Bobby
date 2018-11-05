import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import datetime
import time
import requests
from threading import *
import os


client = discord.Client()
nbplayer = 32                                                    #Variable du nombre de joueurs connectés
nblimit = 30
wlplayer = []
wlcrash = []
wlplayerid = []
wlcrashid = []
channelbot = '502555286574202880' #rocade                       #Channel où le bot affiche les listes
channelref = '503155396920213507' #communication                #Channel de référence pour communiquer avec le bot
channelweb = '502510555618344960' #nb-joueur
channelhisto = '502789558656696321' #historique                 #Channel d'historique
channela = '410420102161367040' #accueil                        #Channel ou le !vote fonctionne
cRole = "Citoyens"                                                #cRole (Common Role) Défini le role lambda qui interagit avec le Bot
textmp = "```markdown\n# Bonjour à toi, je suis Bobby, c'est moi qui gère la Rocade de Sandy Island.```\n\nComment m'utiliser : \n\n :one: Quand le serveur est complet tu dois m'envoyer le message : **!enter** via le channel spécial qui va te permettre de rejoindre la File d'attente. \n \n :two: Si tu étais sur le serveur mais que tu as crash ou time out tu peux m'envoyer : **!crash** via le channel spécial qui va te permettre de rejoindre la File d'attente **Prioritaire**.\n \n :three: Dès que tu as réussi à te connecter n'oublies surtout pas de m'envoyer : **!quit** via le channel spécial qui va permettre de libérer la File d'attente ! \n \n :warning: Vous ne pouvez vous connecter uniquement quand je vous le dis, tout **abus** sur l'utilisation de la rocade sera sévèrement **sanctionné**  :warning: \n \n ```Bonne journée à toi !```"
URL = "http://37.187.158.139:30120/players.json"

@client.event
async def on_ready():
    global nbplayer
    t = datetime.datetime.now()
    await client.change_presence(status=discord.Status.dnd, game= discord.Game(name="le péage (connecting...)", type=3))
    await client.send_message(client.get_channel(channelhisto),f"**{t.hour}:{t.minute:02}** : Le BOT à bien démarré :grin:")
    print("Bobby is ready!")
   
@client.event
async def on_message(message):
    global nbplayer
    if message.author == client.user:
        return
    
    role_names = [role.name for role in message.author.roles]   #Vérifie les roles d'un utilisateur
    channeltyping = message.channel.id                          #channel où est posté le message
    bot_status = discord.Status.idle                            #Initialise l'état du bot
    r = requests.get(url = URL)                                 #Récupère toutes les infos "joueur" du serveur FiveM
    data = r.json()                                             #On garde que les infos
    long = len(data)                                            #Mise dans une liste des infos
    nbplayer = long                                             #On Change la variable nbplayer par la taille de la liste
    name = message.author.nick
    t = datetime.datetime.now()
    var2 = ""
    var3 = ""
    
    if "!enter" in message.content and cRole in role_names and channeltyping == channelref:
        #if message.author.nick not in wlplayer:
        wlplayer.append((message.author.nick))
        wlplayerid.append((message.author))
        print("oui")
        await client.send_message(client.get_channel(channelhisto),f"**{t.hour}:{t.minute:02}** : {name} est entré dans la rocade :white_check_mark: ")
        await client.purge_from(client.get_channel(channelbot), limit=200, check=None, before=None, after=None, around=None)
        await client.purge_from(client.get_channel(channelref), limit=1, check=None, before=None, after=None, around=None)
        t = datetime.datetime.now()
        await client.send_message(client.get_channel(channelbot),f"```markdown\n# Etat de la rocade à : {t.hour}:{t.minute:02}```")
        
        if len(wlcrash) > 0 :
            var2 = "\n- **Liste Prioritaire :**" 
            for k in range(len(wlcrash)):
                var = wlcrash[k]
                var2 = var2 + f"\n{k+1} {var} P"
                var22 = f"```{var2}```"
            await client.send_message(client.get_channel(channelbot),var22)
                                       
        if len(wlplayer) > 0 :
            var3 = "\n- **Liste de Connexion :**" 
            for i in range(len(wlplayer)):
                var = wlplayer[i]
                var3 = var3 + f"\n{i+1} {var}"
                var33 = f"```{var3}```"
            await client.send_message(client.get_channel(channelbot),var33)
        return
    
    if "!crash" in message.content and cRole in role_names and channeltyping == channelref:
        #if message.author.nick not in wlcrash:
        wlcrash.append((message.author.nick))
        wlcrashid.append((message.author))
        await client.send_message(client.get_channel(channelhisto),f"**{t.hour}:{t.minute:02}** : {name} est entré dans la rocade (*Crash*) :warning:")
        
        if len(wlplayer) > 0 and len(wlcrash) == 1:
            await client.send_message(wlplayerid[0],f":warning: C'est désormais **{wlcrash[0]}** qui est prioritaire à cause de son crash, tu dois attendre qu'il se connecte :grin:")

        await client.purge_from(client.get_channel(channelbot), limit=100, check=None, before=None, after=None, around=None)
        await client.purge_from(client.get_channel(channelref), limit=1, check=None, before=None, after=None, around=None)
        t = datetime.datetime.now()
        await client.send_message(client.get_channel(channelbot),f"```markdown\n# Etat de la rocade à : {t.hour}:{t.minute:02}```")
       
        if len(wlcrash) > 0 :
            var2 = "\n- **Liste Prioritaire :**" 
            for k in range(len(wlcrash)):
                var = wlcrash[k]
                var2 = var2 + f"\n```{k+1} {var} P```"
            await client.send_message(client.get_channel(channelbot),var2)
                                       
        if len(wlplayer) > 0 :
            var3 = "\n **- Liste de Connexion :**" 
            for i in range(len(wlplayer)):
                var = wlplayer[i]
                var3 = var3 + f"\n```{i+1} {var}```"
            await client.send_message(client.get_channel(channelbot),var3)
        return
    
    if "!vote" in message.content and channeltyping == channela :
         await client.purge_from(client.get_channel(channela), limit=1, check=None, before=None, after=None, around=None)
         await client.send_message(client.get_channel(channela),"Votez pour soutenir le serveur ! :smiley_cat:  \n https://gta.top-serveurs.net/sandy-island")
         await client.send_message(client.get_channel(channelhisto),f"**{t.hour}:{t.minute:02}** : {name} a lancer le lien de vote ")
         return

    if "!help" in message.content and cRole in role_names and channeltyping == channelref:
        if message.author == client.user:
            return
        await client.purge_from(client.get_channel(channelref), limit=1, check=None, before=None, after=None, around=None)
        await client.send_message(message.author,textmp)
        return

    if "!quit" in message.content and cRole in role_names and channeltyping == channelref:
        if message.author.nick in wlcrash:
            wlcrash.remove((message.author.nick))
            wlcrashid.remove((message.author))
            await client.send_message(client.get_channel(channelhisto),f"**{t.hour}:{t.minute:02}** : {name} a quitté la rocade :negative_squared_cross_mark:")
            
        if message.author.nick in wlplayer:
            wlplayer.remove((message.author.nick))
            wlplayerid.remove((message.author))
            await client.send_message(client.get_channel(channelhisto),f"**{t.hour}:{t.minute:02}** : {name} a quitté la rocade :negative_squared_cross_mark:")
            
        await client.purge_from(client.get_channel(channelbot), limit=100, check=None, before=None, after=None, around=None)
        await client.purge_from(client.get_channel(channelref), limit=1, check=None, before=None, after=None, around=None)
        
        t = datetime.datetime.now()                     #Défini la variable de temps
        
        await client.send_message(client.get_channel(channelbot),f"```markdown\n# Etat de la rocade à : {t.hour}:{t.minute:02}```")
        
        if len(wlcrash) == 0 and len(wlplayer) == 0:
            await client.send_message(client.get_channel(channelbot)," *Personne n'est dans la rocade* :grin: ")
   
        if len(wlcrash) > 0 :
            var2 = "\n- **Liste Prioritaire :**" 
            for k in range(len(wlcrash)):
                var = wlcrash[k]
                var2 = var2 + f"\n```{k+1} {var} P```"
            await client.send_message(client.get_channel(channelbot),var2)
                                       
        if len(wlplayer) > 0 :
            var3 = "\n **- Liste de Connexion :**" 
            for i in range(len(wlplayer)):
                var = wlplayer[i]
                var3 = var3 + f"\n```{i+1} {var}```"
            await client.send_message(client.get_channel(channelbot),var3)
        return

    if "!nbj" in message.content and channeltyping == channelweb:
        if nbplayer < nblimit :
            await client.change_presence(status=discord.Status.dnd, game= discord.Game(name=f"le péage ({nbplayer} joueurs)", type=3))
            return
        await client.change_presence(status=discord.Status.online, game= discord.Game(name=f"gérer la Rocade ({nbplayer} joueurs)", type=0))
        return
        
    if "!mp" in message.content and nbplayer < 31:
        if len(wlplayer) > 0 or len(wlcrash) > 0 :
            if len(wlcrash) > 0 :
                await client.send_message(wlcrashid[0],":wave: **Rappel** : Tu es premier de la File d'attente, tu peux te connecter ! Penses à envoyer un **!quit** dès que tu es connecté ! Merci bien :grin:")
                return
            await client.send_message(wlplayerid[0],":wave: **Rappel** : Tu es premier de la File d'attente, tu peux te connecter ! Penses à envoyer un **!quit** dès que tu es connecté ! Merci bien :grin:")
            print("oui")
            return

    if "!clear" in message.content and channeltyping == channelref :
        await client.purge_from(client.get_channel(channelbot), limit=100, check=None, before=None, after=None, around=None)
        await client.purge_from(client.get_channel(channelref), limit=1, check=None, before=None, after=None, around=None)
        await client.send_message(client.get_channel(channelbot),f"```markdown\n# Etat de la rocade à : {t.hour}:{t.minute:02}```")
        await client.send_message(client.get_channel(channelbot)," *Personne n'est dans la rocade* :grin: ")
        await client.send_message(client.get_channel(channelhisto),f"**{t.hour}:{t.minute:02}** : {name} a clear la rocade")
        del wlcrash[:]
        del wlcrashid[:]
        del wlplayer[:]
        del wlplayerid[:]
        return
        

    if "!variablechange" in message.content and channeltyping == channelref :
        var = re.findall(r'\d+',message.content)
        nbplayer = var[0]
        await client.purge_from(client.get_channel(channelref), limit=1, check=None, before=None, after=None, around=None)
        await client.send_message(message.author,f"Le nombre de joueur en ligne est bien passé à {var[0]}")
        print(var)
        return

    if channeltyping == channelref and "!nbjadmin" in message.content:
        print(nbplayer)
        await client.purge_from(client.get_channel(channelref), limit=1, check=None, before=None, after=None, around=None)
        await client.send_message(message.author,f"Il y a **{long} joueur(s)** en ligne")
        return
        

client.run(os.getenv('TOKEN'))
