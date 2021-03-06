import discord
from discord.ext.commands import Bot
from discord.ext import commands
import asyncio
import datetime
import time
import requests
from threading import *
import random
import re
import os


client = discord.Client()
nbplayer = 18                                                   #Variable du nombre de joueurs connectés
nblimit = 62
mpcount = 0
wlplayer = []
wlcrash = []
wlplayerid = []
wlcrashid = []
channelbot = '569900898180923396' #rocade                       #Channel où le bot affiche les listes
channelref = '569900867105587221' #communication                #Channel de référence pour communiquer avec le bot
channelweb = '502510555618344960' #nb-joueur
channelhisto = '569901853815341067' #historique                 #Channel d'historique
channela = '554490520513019906' #accueil                        #Channel ou le !vote fonctionne
channelg = '568457642469752853' #général
channelo = '507120862831575040' #oui
channelbotlog = '569901853815341067' #log-bobby
cRole = "Citoyens"                                                #cRole (Common Role) Défini le role lambda qui interagit avec le Bot
textmp = "```markdown\n# Bonjour à toi, je suis Bobby, c'est moi qui gère la Rocade de Sandy Island.```\n\nComment m'utiliser : \n\n :one: Quand le serveur est complet tu dois m'envoyer le message : **!enter** via le channel spécial qui va te permettre de rejoindre la File d'attente. \n \n :two: Si tu étais sur le serveur mais que tu as crash ou time out tu peux m'envoyer : **!crash** via le channel spécial qui va te permettre de rejoindre la File d'attente **Prioritaire**.\n \n :three: Dès que tu as réussi à te connecter n'oublies surtout pas de m'envoyer : **!quit** via le channel spécial qui va permettre de libérer la File d'attente ! \n \n :warning: Vous ne pouvez vous connecter uniquement quand je vous le dis, tout **abus** sur l'utilisation de la rocade sera sévèrement **sanctionné**  :warning: \n \n ```Bonne journée à toi !```"
URL = "http://145.239.41.79:30120/players.json"
compteur = 0
gif = ['https://media.giphy.com/media/nb2kpw24iY8M0/giphy.gif','https://media.giphy.com/media/v3sPWJC4RmUgw/giphy.gif','https://tenor.com/We5F.gif','https://tenor.com/umXD.gif','https://tenor.com/RaNa.gif','https://gph.is/2chfxc6','https://gph.is/1vH0L1F','https://media.giphy.com/media/PMExYDVqIZ4RQigOZZ/giphy.gif','https://media.giphy.com/media/13Se61e5mhBwNW/giphy.gif','https://media.giphy.com/media/UNXI76SJ889A4/giphy.gif','https://media.giphy.com/media/HMSLfCl5BsXoQ/giphy.gif','https://media.giphy.com/media/e5s9AhceLnmfe/giphy.gif','https://media.giphy.com/media/xkCK3tAhDSUBa/giphy.gif','https://media.giphy.com/media/a34HjLEsKchWM/giphy.gif','https://media.giphy.com/media/ZlCsLIEg0okec/giphy.gif','https://media.giphy.com/media/TA0C7JvngEkr6/giphy.gif','https://media.giphy.com/media/quO0X65yj6gw0/giphy.gif','https://media.giphy.com/media/6y0KtNGlTyBRcj8GIy/giphy.gif','https://media.giphy.com/media/Ix9b4S1PPRkWY/giphy.gif']



async def printlist():
    global nbplayer

    t = datetime.datetime.now()
    
    await client.send_message(client.get_channel(channelbot),f"```markdown\n# Etat de la rocade à : {t.hour+1}:{t.minute:02}```")
    
    if len(wlcrash) > 0 :
        var2 = "# Liste Prioritaire :\n" 
        for k in range(len(wlcrash)):
            var = wlcrash[k]
            var2 = var2 + f"\n- {k+1} {var} P"
            var22 = f"```markdown\n{var2}```"
        await client.send_message(client.get_channel(channelbot),var22)
                                       
    if len(wlplayer) > 0 :
        var3 = "# Liste de Connexion :\n" 
        for i in range(len(wlplayer)):
            var = wlplayer[i]
            var3 = var3 + f"\n- {i+1} {var}"
            var33 = f"```markdown\n{var3}```"
        await client.send_message(client.get_channel(channelbot),var33)

    if len(wlcrash) == 0 and len(wlplayer) == 0:
            await client.send_message(client.get_channel(channelbot)," *Personne n'est dans la rocade* :grin: ")
            return
    return

@client.event
async def on_ready():
    print("Bobby is ready!")
    
    global nbplayer
    global compteur
    global gif
    
    while True :
        for i in range(0,5):
            
            r = requests.get(url = URL)                                 #Récupère toutes les infos "joueur" du serveur FiveM
            data = r.json()                                             #On garde que les infos
            long = len(data)                                            #Mise dans une liste des infos
            nbplayer = long                                             #On Change la variable nbplayer par la taille de la liste
           
            
            if nbplayer < nblimit :
                await client.change_presence(status=discord.Status.dnd, game= discord.Game(name=f"le péage ({nbplayer}/64 joueurs)", type=3))
                client.send_message(await client.send_message(client.get_channel(channelweb),f"{i}"))
                await asyncio.sleep(3)
            else :
                await client.change_presence(status=discord.Status.online, game= discord.Game(name=f"gérer la Rocade ({nbplayer}/64 joueurs)", type=0))
                await asyncio.sleep(3)
                
        r = requests.get(url = URL)                                 #Récupère toutes les infos "joueur" du serveur FiveM
        data = r.json()                                             #On garde que les infos
        long = len(data)                                            #Mise dans une liste des infos
        nbplayer = long
        t = datetime.datetime.now()
        
        if nbplayer < 64 :
            if len(wlplayer) > 0 or len(wlcrash) > 0 :
                if len(wlcrash) > 0 :
                    secure_random = random.SystemRandom()
                    await client.send_message(wlcrashid[0],f":wave: **Rappel** : Tu es premier de la File d'attente, tu peux te connecter ! Penses à envoyer un **!quit** dès que tu es connecté ! Merci bien :grin: {secure_random.choice(gif)}")
                    client.send_message(await client.send_message(client.get_channel(channelweb),f"{wlcrash[0]} à reçu son mp"))
                    compteur = compteur + 1
                    if compteur == 5 :
                        secure_random = random.SystemRandom()
                        await client.send_message(wlcrashid[0],f":warning: Tu as dépassé le délai de connexion. Tu as été kick de la rocade, tu dois refaire un !enter {secure_random.choice(gif)}")
                        await client.send_message(client.get_channel(channelhisto),f"**{t.hour+1}:{t.minute:02}** : {wlcrash[0]} a été kick de la rocade :arrow_forward: ")
                        del wlcrash[0]
                        del wlcrashid[0]
                        await client.purge_from(client.get_channel(channelbot), limit=10, check=None, before=None, after=None, around=None)
                        await printlist()
                        compteur = 0
                    await asyncio.sleep(30)

                else :
                    secure_random = random.SystemRandom()
                    await client.send_message(wlplayerid[0],f":wave: **Rappel** : Tu es premier de la File d'attente, tu peux te connecter ! Penses à envoyer un **!quit** dès que tu es connecté ! Merci bien :grin: {secure_random.choice(gif)}")
                    client.send_message(await client.send_message(client.get_channel(channelweb),f"{wlplayer[0]} à reçu son mp"))
                    compteur = compteur + 1
                    if compteur == 4 :
                        secure_random = random.SystemRandom()
                        await client.send_message(wlplayerid[0],f":warning: Tu as dépassé le délai de connexion. Tu as été kick de la rocade, tu dois refaire un !enter {secure_random.choice(gif)}")
                        await client.send_message(client.get_channel(channelhisto),f"**{t.hour+1}:{t.minute:02}** : {wlplayer[0]} a été kick de la rocade :arrow_forward: ")
                        del wlplayer[0]
                        del wlplayerid[0]
                        await client.purge_from(client.get_channel(channelbot), limit=10, check=None, before=None, after=None, around=None)
                        await printlist()
                        compteur = 0
                    await asyncio.sleep(30)
            
   
@client.event
async def on_message(message):
    global nbplayer

    if message.author == client.user:
        return
    
    #role_names = [role.name for role in message.author.roles]  #Vérifie les roles d'un utilisateur
    channeltyping = message.channel.id                          #channel où est posté le message
    bot_status = discord.Status.idle                            #Initialise l'état du bot
    r = requests.get(url = URL)                                 #Récupère toutes les infos "joueur" du serveur FiveM
    data = r.json()                                             #On garde que les infos
    long = len(data)                                            #Mise dans une liste des infos
    nbplayer = long                                             #On Change la variable nbplayer par la taille de la liste
    t = datetime.datetime.now()
    var2 = ""
    var3 = ""
    
    if "!enter" in message.content and channeltyping == channelref:
        name = message.author.nick
        if name == None :
            name = message.author
        if message.author.nick not in wlplayer:
            wlplayer.append((name))
            wlplayerid.append((message.author))
            await client.send_message(client.get_channel(channelhisto),f"**{t.hour+1}:{t.minute:02}** : {name} est entré dans la rocade :white_check_mark: ")
            await client.purge_from(client.get_channel(channelbot), limit=10, check=None, before=None, after=None, around=None)
            await client.purge_from(client.get_channel(channelref), limit=1, check=None, before=None, after=None, around=None)
            t = datetime.datetime.now()
        
            if nbplayer < 64 :
                await client.send_message(wlplayerid[0],":wave: **Rappel** : Tu peux te connecter ! Penses à envoyer un **!quit** dès que tu es connecté ! Merci bien :grin:")
            
            await printlist()
            return
            
        else :
            await client.purge_from(client.get_channel(channelref), limit=1, check=None, before=None, after=None, around=None)
            return
       
    
    if "!crash" in message.content and channeltyping == channelref:
        name = message.author.nick
        if name == None :
            name = message.author
        if message.author.nick not in wlcrash:
            wlcrash.append((name))
            wlcrashid.append((message.author))
            await client.send_message(client.get_channel(channelhisto),f"**{t.hour}:{t.minute:02}** : {name} est entré dans la rocade (*Crash*) :warning:")

            if nbplayer < 64 :
                await client.send_message(wlcrashid[0],":wave: **Rappel** : Tu peux te connecter ! Penses à envoyer un **!quit** dès que tu es connecté ! Merci bien :grin:")
        
            if len(wlplayer) > 0 and len(wlcrash) == 1:
                await client.send_message(wlplayerid[0],f":warning: C'est désormais **{wlcrash[0]}** qui est prioritaire à cause de son crash, tu dois attendre qu'il se connecte :grin:")

            await client.purge_from(client.get_channel(channelbot), limit=10, check=None, before=None, after=None, around=None)
            await client.purge_from(client.get_channel(channelref), limit=1, check=None, before=None, after=None, around=None)
            await printlist()
            return
        await client.purge_from(client.get_channel(channelref), limit=1, check=None, before=None, after=None, around=None)
        return

    if "!quit" in message.content and channeltyping == channelref:
        r = requests.get(url = URL)                                 #Récupère toutes les infos "joueur" du serveur FiveM
        data = r.json()                                             #On garde que les infos
        long = len(data)                                            #Mise dans une liste des infos
        nbplayer = long
        t = datetime.datetime.now()
        name = message.author.nick
        global compteur
        if name == None :
            name = message.author
        if name in wlcrash:
            if len(wlcrashid) > 1 and nbplayer < 31 :
                await client.send_message(wlcrashid[1],":wave: **Rappel** : Tu peux te connecter ! Penses à envoyer un **!quit** dès que tu es connecté ! Merci bien :grin:")
            wlcrash.remove((name))
            wlcrashid.remove((message.author))
            await client.send_message(client.get_channel(channelhisto),f"**{t.hour}:{t.minute:02}** : {name} a quitté la rocade :x:")
  
        if name in wlplayer:
            if len(wlplayerid) > 1 and nbplayer < 31 :
                await client.send_message(wlplayerid[1],":wave: **Rappel** : Tu peux te connecter ! Penses à envoyer un **!quit** dès que tu es connecté ! Merci bien :grin:")
            wlplayer.remove((name))
            wlplayerid.remove((message.author))
            await client.send_message(client.get_channel(channelhisto),f"**{t.hour+1}:{t.minute:02}** : {name} a quitté la rocade :x:")
    
        await client.purge_from(client.get_channel(channelbot), limit=10, check=None, before=None, after=None, around=None)
        await client.purge_from(client.get_channel(channelref), limit=1, check=None, before=None, after=None, around=None)
   
        await printlist()
        compteur = 0
        return
    
    if message.content.startswith("!bbt"):
        if channeltyping == channelo :
            if "1" in message.content :
                msgcp = await client.wait_for_message(author=message.author)
                msgcp1 = msgcp.content
                await client.send_message(client.get_channel(channela),msgcp1)
                return
            
            if "2" in message.content :
                msgcp = await client.wait_for_message(author=message.author)
                msgcp2 = msgcp.content
                await client.send_message(client.get_channel(channelg),msgcp2)
                return

    if "Bonne nuit" in message.content or "bonne nuit" in message.content or "Bonne Nuit" in message.content or "Bonne soirée" in message.content:
        if channeltyping == channela :
            x = "\U0001F4A4"
            await client.add_reaction(message, x)
            return
        return
    
    if "Bonjour" in message.content or "salut" in message.content or "bonjour" in message.content or "Salut" in message.content:
        if channeltyping == channela :
            x = "\U0001F44B"
            await client.add_reaction(message, x)
            return
        return

    if "!kick c" in message.content and channeltyping == channelbotlog :
        name = message.author.nick
        if name == None :
            name = message.author
        var = re.findall(r'\d+',message.content)
        print(var)
        kick = var[0]
        kick = int(kick)
        print(kick)
        kick = kick - 1
        await client.purge_from(client.get_channel(channelbotlog), limit=1, check=None, before=None, after=None, around=None)
        await client.purge_from(client.get_channel(channelbot), limit=10, check=None, before=None, after=None, around=None)
        await client.send_message(client.get_channel(channelhisto),f"**{t.hour+1}:{t.minute:02}** : {name} a kick {wlplayer[kick]} :rage:")
        await client.send_message(wlplayerid[kick],"Tu as été kick de la rocade par un admin :rage:")
        del wlplayer[kick]
        del wlplayerid[kick]
        await printlist()
        return

    if "!kick p" in message.content and channeltyping == channelbotlog :
        name = message.author.nick
        if name == None :
            name = message.author
        var = re.findall(r'\d+',message.content)
        kick = var[0]
        kick = int(kick)
        kick = kick - 1
        await client.purge_from(client.get_channel(channelbot), limit=10, check=None, before=None, after=None, around=None)
        await client.purge_from(client.get_channel(channelbotlog), limit=1, check=None, before=None, after=None, around=None)
        await client.send_message(client.get_channel(channelhisto),f"**{t.hour+1}:{t.minute:02}** : {name} a kick {wlcrash[kick]} :rage:")
        await client.send_message(wlcrashid[kick],"Tu as été kick de la rocade par un admin :rage:")
        del wlcrash[kick]
        del wlcrashid[kick]
        await printlist()
        return


    if "!vote" in message.content and channeltyping == channela :
         name = message.author.nick
         if name == None :
            name = message.author
         await client.purge_from(client.get_channel(channela), limit=1, check=None, before=None, after=None, around=None)
         await client.send_message(client.get_channel(channela),"Votez pour soutenir le serveur ! :smiley_cat:  \n https://gta.top-serveurs.net/nostra-island")
         await client.send_message(client.get_channel(channelhisto),f"**{t.hour+1}:{t.minute:02}** : {name} a lancer le lien de vote ")
         return
    
    if "!radio" in message.content and channeltyping == channelg :
         name = message.author.nick
         if name == None :
            name = message.author
         await client.purge_from(client.get_channel(channelg), limit=1, check=None, before=None, after=None, around=None)
         await client.send_message(client.get_channel(channelg),"La présence radio est obligatoire lorsque vous êtes présent en ville ! Le channel «En ville» est présent pour ne pas être dérangé. :grin: ")
         await client.send_message(client.get_channel(channelhisto),f"**{t.hour+1}:{t.minute:02}** : {name} a appelé la radio ")
         return
    
    if "!service" in message.content and channeltyping == channelg :
         name = message.author.nick
         if name == None :
            name = message.author
         await client.purge_from(client.get_channel(channelg), limit=1, check=None, before=None, after=None, around=None)
         await client.send_message(client.get_channel(channelg),"Si vous occupez un métier de service et que vous êtes le seul en ville de disponible, merci de RESTER EN SERVICE ! #reglement :grin: ")
         await client.send_message(client.get_channel(channelhisto),f"**{t.hour+1}:{t.minute:02}** : {name} a appelé le service ")
         return

    #if "!help" in message.content and channeltyping == channelref:
    #    if message.author == client.user:
    #        return
    #    name = message.author.nick
    #    if name == None :
    #        name = message.author
    #   await client.purge_from(client.get_channel(channelref), limit=1, check=None, before=None, after=None, around=None)
    #    await client.send_message(message.author,textmp)
    #    return


    if "!clear" in message.content and channeltyping == channelbotlog :
        name = message.author.nick
        if name == None :
            name = message.author
        await client.purge_from(client.get_channel(channelbot), limit=10, check=None, before=None, after=None, around=None)
        await client.purge_from(client.get_channel(channelref), limit=1, check=None, before=None, after=None, around=None)
        await client.send_message(client.get_channel(channelbot),f"```markdown\n# Etat de la rocade à : {t.hour}:{t.minute:02}```")
        await client.send_message(client.get_channel(channelbot)," *Personne n'est dans la rocade* :grin: ")
        await client.send_message(client.get_channel(channelhisto),f"**{t.hour+1}:{t.minute:02}** : {name} a clear la rocade")
        del wlcrash[:]
        del wlcrashid[:]
        del wlplayer[:]
        del wlplayerid[:]
        return
    
client.run((os.getenv('TOKEN')))
