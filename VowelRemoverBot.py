import telebot
import config
import random
import time

Vowels = [u"а", u"е", u"ё", u"и", u"о", u"у", u"э", u"ю", u"ы", u"я", "a", "e", "i", "o", "u", "y"]

bot = telebot.TeleBot(config.token)

OFFLINE = False
ONLINE = True

class Game:
    def __init__(self, ID):
        self.flag = OFFLINE
        self.playerIds = []
        self.MapPlayer1 = []
        self.MapPlayer2 = []

        self.playerIds.append(ID)
        for n in range(5):
            self.MapPlayer1.append([0]*5)
            self.MapPlayer2.append([0]*5)
    def __del__(self):
        for id in self.playerIds:
            bot.send_message(id, "Игра прервана!")
            idsStates[id] = OFFLINE
            del idsTokens[id]
        #del tokensGame[]
    def connect(self, id):
        self.playerIds.append(id)
        for id in self.playerIds:
            bot.send_message(id, "Соединение установлено!")
        self.flag = ONLINE
    def getPlayersIds(self):
        return self.playerIds
    def getOtherPlayerId(self, id):
        if self.playerIds[0] == id:
            return self.playerIds[1]
        elif self.playerIds[1] == id:
            return self.playerIds[0]
        return -1

idsStates = {}
idsTokens = {}
waitingForToken = []
waitingTokens = []
tokensGame = {}

def disconnect(token):
    del tokensGame[token]
    return

def generateToken():
    random.seed(time.time())
    token = random.randint(10000, 99999)
    while token in tokensGame:
        token = random.randint(10000, 99999)
    return token

def establishConnection(token, PlayerId):
    if token in waitingTokens:
        idsStates[PlayerId] = ONLINE
        idsTokens[PlayerId] = token
        # Joining the two players
        tokensGame[token].connect(PlayerId)
        # Deleting players from waitingForToken and waitingGames
        waitingTokens.remove(token)
        waitingForToken.remove(PlayerId)
    else:
        bot.send_message(PlayerId, "Такого токена не существует!")
    return

@bot.message_handler(commands=["create", "join", "exit"])
def ReactToCommands(message):
    PlayerId = message.chat.id
    if PlayerId in waitingForToken:
        waitingForToken.remove(PlayerId)
        bot.send_message(PlayerId, "Ожидание токена прерванно!")
    if idsStates.get(PlayerId) == ONLINE:
        disconnect(idsTokens[PlayerId])
    if message.text == "/create":
        token = generateToken()
        idsTokens[PlayerId] = token
        tokensGame[token] = Game(PlayerId)
        idsStates[PlayerId] = ONLINE
        waitingTokens.append(token)
        bot.send_message(PlayerId, "Ваш токен: " + str(token))
        bot.send_message(PlayerId, "Ожидание соперника...")
    if message.text == "/join":
        bot.send_message(PlayerId, "Пожалуйста, введите токен.")
        waitingForToken.append(PlayerId)
    if message.text == "/exit":
        pass

@bot.message_handler(content_types=["text"])
def ReactToText(message):
    PlayerId = message.chat.id
    #for game in GamesList:
    #    if message.chat.id in game.getPlayersIds():

    # Establishing a connection between two players
    if PlayerId in waitingForToken:
        try:
            token = int(message.text)
            establishConnection(token, PlayerId)
        except:
            bot.send_message(PlayerId, "Неверный токен!")
    elif idsStates.get(PlayerId) == ONLINE:
        if len(tokensGame[idsTokens[PlayerId]].playerIds) < 2:
            disconnect(idsTokens[PlayerId])
            return
        otherPlayer = tokensGame[idsTokens[PlayerId]].getOtherPlayerId(PlayerId)
        textMessage = message.text
        ToSend = ""
        for char in textMessage:
            if char.lower() not in Vowels:
                ToSend += char
        if ToSend != "":
            bot.send_message(otherPlayer, ToSend)

if __name__ == "__main__":
    bot.polling(none_stop=True)
