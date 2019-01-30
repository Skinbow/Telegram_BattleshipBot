import telebot
import config
import random

bot = telebot.TeleBot(config.token)

OFFLINE = False
ONLINE = True

class Game:
    flag = OFFLINE
    playerIds = []
    MapPlayer1 = []
    MapPlayer2 = []
    ShipsToBePlaced1 = []
    ShipsToBePlaced2 = []
    # 1 - waiting for player to place the ships; 2 - player's turn; 3 - other player's turn
    playerStates = [0, 0]
    def __init__(self, ID):
        self.playerIds.append(ID)
        for n in range(5):
            self.MapPlayer1.append([0]*5)
            self.MapPlayer2.append([0]*5)
        self.ShipsToBePlaced1 = [2]
        self.ShipsToBePlaced2 = [2]
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
            bot.send_message(id, "Введите местоположения кораблей. (X Y)")
            self.playerStates = [1, 1]
        self.flag = ONLINE
    def getPlayersIds(self):
        return self.playerIds
    def createShip(self, id, x, y):
        if id == self.playerIds[0]:
            self.MapPlayer1[y][x] = True
            self.ShipsToBePlaced1[1 - 1] -= 1

            noneLeft = True
            for shipsLeft in self.ShipsToBePlaced1:
                if noneLeft
        else if id == self.playerIds[1]:
            self.MapPlayer2[y][x] = True
            self.ShipsToBePlaced2[1 - 1] -= 1

idsStates = {}
idsTokens = {}
waitingForToken = []
waitingTokens = []
tokensGame = {}

def disconnect(token):
    del tokensGame[token]
    return

def generateToken():
    token = random.randint(10000, 99999)
    while tokensGame.get(token) != None:
        token = random.randint(10000, 99999)
    return token

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
def Battleships(message):
    PlayerId = message.chat.id
    if idsTokens[PlayerId] in tokensGame:
        CurrentGame = tokensGame[idsTokens[PlayerId]];
        try:
            x = ""
            y = ""
            recordingX = True
            for c in message.text:
                if c == " ":
                    recordingX = False
                else:
                    if recordingX:
                        x += c
                    else:
                        y += c
            try:
                ix = int(x)
                iy = int(y)
            except:
                bot.send_message(PlayerId, "Неверный ввод! (X Y)")
            CurrentGame.createShip(PlayerId, x, y)
    else:
        try:
            token = int(message.text)
            if PlayerId in waitingForToken:
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
            else:
                bot.send_message(PlayerId, "Неверная команда!")
        except:
            bot.send_message(PlayerId, "Неверный токен!")
    #for game in GamesList:
    #    if message.chat.id in game.getPlayersIds():

    # Establishing a connection between two players

if __name__ == "__main__":
    bot.polling(none_stop=True)
