import telebot
import config
import random

bot = telebot.TeleBot(config.token)

OFFLINE = 0
WAIT = 1
ONLINE = 2

class Game:
    flag = 0
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
    def __init__(self, log1, log2):
        self.playerIds.append(log1)
        self.playerIds.append(log2)
        for n in range(5):
            self.MapPlayer1.append([0]*5)
            self.MapPlayer2.append([0]*5)
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

waitingGames = {}
state = {}
idsTokens = {}
waitingForToken = []
GamesList = []

def makeOffline(id):
    state[id] = OFFLINE
    waitingGames.pop(idsTokens[id])
    idsTokens.pop(id)
    return

@bot.message_handler(commands=["create", "join", "exit"])
def ReactToCommands(message):
    if state.get(message.chat.id) == WAIT:
        bot.send_message(message.chat.id, "Ожидание прерванно!")
        makeOffline(message.chat.id)
    if state.get(message.chat.id) == ONLINE:
        bot.send_message(message.chat.id, "Игра прерванна!")
        makeOffline(message.chat.id)
    if message.text == "/create":
        token = random.randint(10000, 99999)
        while token in waitingGames:
            token = random.randint(10000, 99999)
        state[message.chat.id] = WAIT
        idsTokens[message.chat.id] = token
        waitingGames[token] = message.chat.id
        bot.send_message(message.chat.id, "Ваш токен: " + str(token))
        bot.send_message(message.chat.id, "Ожидание соперника...")
    if message.text == "/join":
        bot.send_message(message.chat.id, "Пожалуйста, введите токен.")
        waitingForToken.append(message.chat.id)
    if message.text == "/exit":
        for game in GamesList:
            ids = game.getPlayersIds()
            if message.chat.id in ids:
                bot.send_message(ids[0], "Игра прерванна!")
                makeOffline(ids[0])
                bot.send_message(ids[1], "Игра прерванна!")
                makeOffline(ids[1])
                GamesList.remove(game)
                break

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
    if message.chat.id in waitingForToken:
        #try:
            if waitingGames.get(int(message.text)) != None:
                state[message.chat.id] = ONLINE
                idsTokens[message.chat.id] = int(message.text)
                # Joining the two players
                AGame = Game(waitingGames[int(message.text)], message.chat.id)
                GamesList.append(AGame)
                state[waitingGames[int(message.text)]] = ONLINE
                bot.send_message(message.chat.id, "Соеденинение установлено!")
                bot.send_message(waitingGames[int(message.text)], "Соеденинение установлено!")
                # Deleting players from waitingForToken and waitingGames
                waitingForToken.remove(message.chat.id)
                del waitingGames[int(message.text)]

            else:
                bot.send_message(message.chat.id, "Такого токена не существует!")
        #except:
            #bot.send_message(message.chat.id, "Токен не действительный! Токен должен содержать 5 цифр.")

if __name__ == "__main__":
    bot.polling(none_stop=True)
