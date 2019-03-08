# -*-  coding: utf-8 -*-

import telebot
import config
import random
import time

bot = telebot.TeleBot(config.token)

# State for Game.flag
OFFLINE = 0
CONNECT = 1
INGAME = 2

class Game:
    waitingForCoord = []
    shipLimit = 5
    # Initializer
    def __init__(self, ID):
        self.flag = OFFLINE
        self.turn = 0
        self.shipCounter = [0, 0]
        self.ready = [False, False]
        self.playerIds = []
        self.MapPlayer = []
        self.GameMap = []
        self.playerIds.append(ID)
        #self.playerIndexes = {ID : 0}
        for i in range(2):
            TempMatrix = []
            for n in range(5):
                TempMatrix.append([0]*5)
            self.MapPlayer.append(TempMatrix)
        for i in range(2):
            TempMatrix = []
            for n in range(5):
                TempMatrix.append([0]*5)
            self.GameMap.append(TempMatrix)

    # Destructor
    def __del__(self):
        for id in self.playerIds:
            bot.send_message(id, "Игра прервана!")
            idsStates[id] = OFFLINE
            del idsTokens[id]
        #del tokensGame[]

    # Used to connect two players
    def connect(self, id):
        self.playerIds.append(id)
        for id in self.playerIds:
            bot.send_message(id, "Соединение установлено!")
        self.flag = CONNECT
        # Begin waiting for them to send the ship coordinates in
        self.waitingForCoord.append(self.playerIds[0])
        self.waitingForCoord.append(self.playerIds[1])

    # Obatain, using an id, the id of the other player
    def getOtherPlayerId(self, id):
        if self.playerIds[0] == id:
            return self.playerIds[1]
        elif self.playerIds[1] == id:
            return self.playerIds[0]
        return -1

    # Using an id, obtain their index in all the Game class arrays
    def getIndexOfPlayer(self, id):
        if self.playerIds[0] == id:
            return 0
        elif self.playerIds[1] == id:
            return 1

    # Using an id, obtain their index in all the Game class arrays
    def getIndexOfOtherPlayer(self, id):
        if self.playerIds[0] == id:
            return 1
        elif self.playerIds[1] == id:
            return 0

    # Used to place one one-deck ship on the MapPlayer at the beginning of the game
    def createOneSquareShip(self, id, x, y):
        PlayerIndex = self.getIndexOfPlayer(id)
        if self.ready[PlayerIndex]:
            bot.send_message(id, "Вы уже расставили все возможные корабли!")
        elif self.shipCounter[PlayerIndex] < self.shipLimit:
            if self.MapPlayer[PlayerIndex][y][x] != 1:
                self.MapPlayer[PlayerIndex][y][x] = 1
                self.shipCounter[PlayerIndex] += 1
            else:
                bot.send_message(id, "Там уже стоит корабль!")

            if self.shipCounter[PlayerIndex] == self.shipLimit:
                self.ready[PlayerIndex] = True
                self.waitingForCoord.remove(id)
                bot.send_message(self.getOtherPlayerId(id), "Ваш соперник готов!")
                if self.ready[self.getIndexOfPlayer(self.getOtherPlayerId(id))] == True:
                    bot.send_message(id, "Игра началась!")
                    bot.send_message(self.getOtherPlayerId(id), "Игра началась!")
                    self.flag = INGAME
                    bot.send_message(self.playerIds[self.turn], self.GetFormattedShotsMap(self.playerIds[self.turn]))
        return

    # Used to shoot at a square on GameMap and record whether it hit a ship or not (return -1 when square has already been hit by player)
    def Shoot(self, id, x, y):
        PlayerIndex = self.getIndexOfPlayer(id)
        # If the square has never been shot:
        if self.GameMap[PlayerIndex][x][y] == 0:
            # If the player hit a ship:
            if self.MapPlayer[self.getIndexOfOtherPlayer(id)][x][y] == 1:
                self.GameMap[PlayerIndex][x][y] = 2
            # If the player didn't hit a ship:
            else:
                self.GameMap[PlayerIndex][x][y] = 1
            self.SwitchTurn()
        # If the square has already been shot:
        else:
            bot.send_message(id, "Вы уже стреляли в эту клетку!")
            return -1

    # Change player's turn
    def SwitchTurn(self):
        if self.turn == 0:
            self.turn = 1
        else:
            self.turn == 0

    # Obtain a string representing the ship positionment map
    def GetFormattedMap(self, id):
        resultText = ""
        resultText += "•ABCDE"
        for y in range(5):
            resultText += "\n"
            line = self.MapPlayer[self.getIndexOfPlayer(id)][y]
            resultText += str(y+1)
            for square in line:
                # There's a ship there:
                if square == 1:
                    resultText += "#"
                # There's no ship there:
                else:
                    resultText += "~"
        return resultText

    # Obtain a string representing the squares shot by the player
    def GetFormattedShotsMap(self, id):
        resultText = ""
        resultText += "•ABCDE"
        for y in range(5):
            resultText += "\n"
            line = self.GameMap[self.getIndexOfPlayer(id)][y]
            resultText += str(y+1)
            for square in line:
                # There was a ship there:
                if square == 2:
                    resultText += "#"
                # There was no ship there:
                elif square == 1:
                    resultText += "∙"
                # The tile has never been shot at:
                else:
                    resultText += "~"
        return resultText

idsStates = {}
idsTokens = {}
waitingForToken = []
waitingTokens = []
tokensGame = {}

# Destroy game by id
def disconnect(id):
    token = idsTokens[id]
    del tokensGame[token]
    return

# Generate a random token between 10000 and 99999
def generateToken():
    random.seed(time.time())
    token = random.randint(10000, 99999)
    while token in tokensGame:
        token = random.randint(10000, 99999)
    return token

# Called when the player trying to join a game enters a token
def establishConnection(token, PlayerId):
    if token in waitingTokens:
        # Marking player as connected
        idsStates[PlayerId] = CONNECT
        # Assigning this token to the player's id
        idsTokens[PlayerId] = token
        # Joining the two players
        tokensGame[token].connect(PlayerId)
        # Deleting players from waitingForToken and waitingGames
        waitingTokens.remove(token)
        waitingForToken.remove(PlayerId)
    else:
        # Executed if there is no player with this token is waiting for another player
        bot.send_message(PlayerId, "Такого токена не существует!")
    return

# From a two-character input, such as, for example, "A3", get the corresponding x and y coordinates in an array [x,y]
def GetXYFromInput(s, PlayerId):
    if len(s) > 2:
        bot.send_message(PlayerId, "Неверный ввод!")
        return -1
    x = ord(s[0]) - 65
    # Checking for characters outside of the A-E interval
    if x < 0 or x > 4:
        x -= 25
        # Checking for characters outside of the a-e interval
        if x < 0 or x > 4:
            bot.send_message(PlayerId, "Неверный ввод!")
            return -1
    y = int(s[1]) - 1
    # Checking for numbers outside of the 1-5 interval
    if y < 0 or y > 4:
        bot.send_message(PlayerId, "Неверный ввод!")
        return -1
    return [x, y]

@bot.message_handler(commands=["create", "join", "exit"])
def ReactToCommands(message):
    PlayerId = message.chat.id

    # Stop the game joining process if the player enters a new command
    if PlayerId in waitingForToken:
        waitingForToken.remove(PlayerId)
        bot.send_message(PlayerId, "Ожидание токена прерванно!")

    # Delete the player from the waiting games queue if they enter a new command
    if idsStates.get(PlayerId) == CONNECT:
        disconnect(PlayerId)

    # The creation of a new game
    if message.text == "/create":
        token = generateToken()
        idsTokens[PlayerId] = token
        tokensGame[token] = Game(PlayerId)
        idsStates[PlayerId] = CONNECT
        waitingTokens.append(token)
        bot.send_message(PlayerId, "Ваш токен: " + str(token))
        bot.send_message(PlayerId, "Ожидание соперника...")

    # Lets a player join another player through their token
    if message.text == "/join":
        bot.send_message(PlayerId, "Пожалуйста, введите токен.")
        waitingForToken.append(PlayerId)

    # Cancels all previously entered commands
    if message.text == "/exit":
        pass

@bot.message_handler(content_types=["text"])
def Battleships(message):
    PlayerId = message.chat.id

    # Players aren't connected yet
    if PlayerId in waitingForToken:
        # Establishing a connection between two players
        try:
            token = int(message.text)
            establishConnection(token, PlayerId)
        except:
            bot.send_message(PlayerId, "Неверный токен!")

    # Players are already connected
    elif idsStates.get(PlayerId) == CONNECT:
        CurrentGame = tokensGame[idsTokens[PlayerId]]
        # We are waiting for the player to enter the ship coordinates
        if PlayerId in Game.waitingForCoord:
            for s in message.text.split(" "):
                l = GetXYFromInput(s, PlayerId)
                if l == -1: return
                x = l[0]
                y = l[1]
                # Place one single-decked ship on the game field
                CurrentGame.createOneSquareShip(PlayerId, x, y)
            # Print the resulting map of the player's ships
            bot.send_message(PlayerId, CurrentGame.GetFormattedMap(PlayerId))

        # The player is currently playing the game
        elif CurrentGame.flag == INGAME:
            if CurrentGame.playerIds[CurrentGame.turn] == PlayerId:
                # check is used for checking if the player has entered correct coordinates
                check = -1
                while check == -1:
                    l = GetXYFromInput(message.text, PlayerId)
                    if l == -1: return
                    x = l[0]
                    y = l[1]
                    check = CurrentGame.Shoot(PlayerId, x, y)
            else:
                bot.send_message(PlayerId, "Сейчас не ваш ход!")


if __name__ == "__main__":
    bot.polling(none_stop=True)
