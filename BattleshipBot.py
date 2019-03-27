# -*-  coding: utf-8 -*-

import telebot
import config
import random
import time
#from Game import *

bot = telebot.TeleBot(config.token)

idsStates = {}
idsTokens = {}
waitingForToken = []
waitingTokens = []
tokensGame = {}

# State for Game.flag and idsStates
OFFLINE = 0
CONNECT = 1
INGAME = 2

class Game:
    waitingForCoord = []
    shipLimit = 5
    # Initializer
    def __init__(self, ID):
        self.boardSize = [5, 5]
        self.flag = OFFLINE
        self.turn = 0
        self.shipCounter = [0, 0]
        self.sunkShips = [0, 0]
        self.ready = [False, False]
        self.playerIds = []
        self.MapPlayer = []
        self.GameMap = []
        self.playerIds.append(ID)
        for i in range(2):
            TempMatrix = []
            for n in range(self.boardSize[1]):
                TempMatrix.append([0]*self.boardSize[0])
            self.MapPlayer.append(TempMatrix)
        for i in range(2):
            TempMatrix = []
            for n in range(self.boardSize[1]):
                TempMatrix.append([0]*self.boardSize[0])
            self.GameMap.append(TempMatrix)

    # Destructor
    def __del__(self):
        for id in self.playerIds:
            if self.sunkShips[0] < self.shipLimit and self.sunkShips[0] < self.shipLimit:
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

    # Obtain, using an id, the id of the other player
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
            bot.send_message(id, "Максимальное количество кораблей: {0}".format(sel.shipLimit))
            bot.send_message(id, "Вы уже расставили все возможные корабли!")
            bot.send_message(id, "Ждите своего соперника!")
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
        return

    def CheckIfBothPlayersAreReady(self):
        if self.ready[0] and self.ready[1]:
            bot.send_message(self.playerIds[0], "Игра началась!")
            bot.send_message(self.playerIds[1], "Игра началась!")
            self.flag = INGAME
            return True
        return False

    # Used to shoot at a square on GameMap and record whether it hit a ship or not (return -1 when square has already been hit by player)
    def Shoot(self, id, x, y):
        PlayerIndex = self.getIndexOfPlayer(id)
        # If the square has never been shot:
        if self.GameMap[PlayerIndex][y][x] == 0:
            # If the player hit a ship:
            if self.MapPlayer[self.getIndexOfOtherPlayer(id)][y][x] == 1:
                self.GameMap[PlayerIndex][y][x] = 2
                self.sunkShips[self.getIndexOfPlayer(id)] += 1;
            # If the player didn't hit a ship:
            else:
                self.GameMap[PlayerIndex][y][x] = 1
            return 0
        # If the square has already been shot:
        else:
            bot.send_message(id, "Вы уже стреляли в эту клетку!")
            return -1

    # Change player's turn
    def SwitchTurn(self, PlayerId):
        if self.turn == 0:
            self.turn = 1
        else:
            self.turn = 0
        bot.send_message(PlayerId, "Ход вашего соперника.")
        bot.send_message(PlayerId, self.GetFormattedMap(PlayerId, "Ваша карта:\n\n"))
        bot.send_message(PlayerId, self.GetFormattedShotsMap(self.getOtherPlayerId(PlayerId), "Места куда стрелял ваш соперник:\n\n"))
        bot.send_message(self.getOtherPlayerId(PlayerId), "Ваш ход!")
        bot.send_message(self.getOtherPlayerId(PlayerId), self.GetFormattedShotsMap(self.getOtherPlayerId(PlayerId)))

    # Obtain a string representing the ship positionment map
    def GetFormattedMap(self, id, beginningMessage=""):
        resultText = beginningMessage + "• "
        for i in range(self.boardSize[0]):
            resultText += chr(i + 65)
        for y in range(self.boardSize[1]):
            resultText += "\n"
            line = self.MapPlayer[self.getIndexOfPlayer(id)][y]
            resultText += str(y+1) + " "
            for square in line:
                # There's a ship there:
                if square == 1:
                    resultText += "#"
                # There's no ship there:
                else:
                    resultText += "~"
        return resultText

    # Obtain a string representing the squares shot by the player
    def GetFormattedShotsMap(self, id, beginningMessage=""):
        resultText = beginningMessage + "• "
        for i in range(self.boardSize[0]):
            resultText += chr(i + 65)
        for y in range(self.boardSize[1]):
            resultText += "\n"
            line = self.GameMap[self.getIndexOfPlayer(id)][y]
            resultText += str(y+1) + " "
            for square in line:
                # There was a ship there:
                if square == 2:
                    resultText += "#"
                # There was no ship there:
                elif square == 1:
                    resultText += "⊙"
                # The tile has never been shot at:
                else:
                    resultText += "~"
        return resultText


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
    AGame = tokensGame[idsTokens[PlayerId]]
    if len(s) > 2:
        bot.send_message(PlayerId, "Неверный ввод: {0}".format(s))
        return -1
    x = ord(s[0]) - 65
    # Checking for characters outside of the A-E interval
    if x < 0 or x >= AGame.boardSize[0]:
        x -= 32
        # Checking for characters outside of the a-e interval
        if x < 0 or x >= AGame.boardSize[0]:
            bot.send_message(PlayerId, "Неверный ввод: {0}".format(s))
            return -1
    y = int(s[1]) - 1
    # Checking for numbers outside of the 1-5 interval
    if y < 0 or y >= AGame.boardSize[1]:
        bot.send_message(PlayerId, "Неверный ввод: {0}".format(s))
        return -1
    return [x, y]

# Send the end game messages
def EndGameMessage(AGame):
    bot.send_message(AGame.playerIds[0], "Игра окончена!")
    bot.send_message(AGame.playerIds[1], "Игра окончена!")
    for PlayerId in AGame.playerIds:
        if AGame.sunkShips[AGame.getIndexOfPlayer(PlayerId)] == AGame.shipLimit:
            bot.send_message(PlayerId, "Вы выиграли!")
        else:
            bot.send_message(PlayerId, "Вы проиграли!")
    return

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
        AGame = tokensGame[idsTokens[PlayerId]]
        # We are waiting for the player to enter the ship coordinates
        if PlayerId in Game.waitingForCoord:
            for s in message.text.split(" "):
                l = GetXYFromInput(s, PlayerId)
                if l == -1: continue
                x = l[0]
                y = l[1]
                # Place one single-decked ship on the game field
                AGame.createOneSquareShip(PlayerId, x, y)
                # If the player is ready and can't place any other ships, break
                if AGame.ready[AGame.getIndexOfPlayer(PlayerId)]:
                    break
            # Print the resulting map of the player's ships
            bot.send_message(PlayerId, AGame.GetFormattedMap(PlayerId))
            # Check if both players are ready
            if AGame.CheckIfBothPlayersAreReady():
                bot.send_message(AGame.playerIds[AGame.turn], "Ваш ход!")
                bot.send_message(AGame.playerIds[AGame.turn], AGame.GetFormattedShotsMap(AGame.playerIds[AGame.turn]))

        # The player is currently playing the game
        elif AGame.flag == INGAME:
            if AGame.playerIds[AGame.turn] == PlayerId:
                # check is used for checking if the player has entered correct coordinates
                check = -1
                while check == -1:
                    l = GetXYFromInput(message.text, PlayerId)
                    if l == -1: return
                    x = l[0]
                    y = l[1]
                    check = AGame.Shoot(PlayerId, x, y)
                bot.send_message(PlayerId, AGame.GetFormattedShotsMap(PlayerId))
                if AGame.sunkShips[0] == AGame.shipLimit or AGame.sunkShips[1] == AGame.shipLimit:
                    EndGameMessage(AGame)
                    disconnect(PlayerId)
                    exit()
                AGame.SwitchTurn(PlayerId)
            else:
                bot.send_message(PlayerId, "Сейчас не ваш ход!")


if __name__ == "__main__":
    bot.polling(none_stop=True)
