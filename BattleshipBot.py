import telebot
import config
import random
import time

bot = telebot.TeleBot(config.token)

OFFLINE = False
ONLINE = True

class Game:
    waitingForCoord = []
    shipLimit = 5
    def __init__(self, ID):
        self.flag = OFFLINE
        self.shipCounter = [0, 0]
        self.ready = [False, False]
        self.playerIds = []
        self.MapPlayer = []
        self.playerIds.append(ID)
        for i in range(2):
            TempMatrix = []
            for n in range(5):
                TempMatrix.append([0]*5)
            self.MapPlayer.append(TempMatrix)

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
        self.waitingForCoord.append(self.playerIds[0])
        self.waitingForCoord.append(self.playerIds[1])

    def getPlayersIds(self):
        return self.playerIds

    def getOtherPlayerId(self, id):
        if self.playerIds[0] == id:
            return self.playerIds[1]
        elif self.playerIds[1] == id:
            return self.playerIds[0]
        return -1

    def getIndexOfPlayer(self, PlayerId):
        if self.playerIds[0] == PlayerId:
            return 0
        elif self.playerIds[1] == PlayerId:
            return 1

    def createOneSquareShip(self, PlayerId, x, y):
        PlayerIndex = self.getIndexOfPlayer(PlayerId)
        if self.ready[PlayerIndex]:
            bot.send_message(PlayerId, "Вы уже расставили все возможные корабли!")
        elif self.shipCounter[PlayerIndex] < self.shipLimit:
            if x >= 0 and x < 5 and y >= 0 and y < 5:
                if self.MapPlayer[PlayerIndex][x][y] != 1:
                    self.MapPlayer[PlayerIndex][x][y] = 1
                    self.shipCounter[PlayerIndex] += 1
                else:
                    bot.send_message(PlayerId, "Там уже стоит корабль!")

            if self.shipCounter[PlayerIndex] == self.shipLimit:
                self.ready[PlayerIndex] = True
                bot.send_message(self.getOtherPlayerId(PlayerId), "Ваш соперник готов!")
        return

    def GetFormattedMap(self, PlayerId):
        resultText = ""
        for y in range(5):
            line = self.MapPlayer[self.getIndexOfPlayer(PlayerId)][y]
            for square in line:
                if square == 1:
                    resultText += "#"
                else:
                    resultText += "~"
            resultText += "\n"
        return resultText

idsStates = {}
idsTokens = {}
waitingForToken = []
waitingTokens = []
tokensGame = {}

def disconnect(id):
    token = idsTokens[id]
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
        disconnect(PlayerId)
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
def Battleships(message):
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
        if PlayerId in Game.waitingForCoord:
            for s in message.text.split(" "):
                if len(s) > 2:
                    bot.send_message(PlayerId, "Неверный ввод!")
                    return
                x = ord(s[0]) - 65
                if x < 0 or x > 4:
                    x -= 25
                    if x < 0 or x > 4:
                        bot.send_message(PlayerId, "Неверный ввод!")
                        return
                y = int(s[1]) - 1
                if y < 0 or y > 4:
                    bot.send_message(PlayerId, "Неверный ввод!")
                    return
                tokensGame[idsTokens[PlayerId]].createOneSquareShip(PlayerId, x, y)
            bot.send_message(PlayerId, tokensGame[idsTokens[PlayerId]].GetFormattedMap(PlayerId))


if __name__ == "__main__":
    bot.polling(none_stop=True)
