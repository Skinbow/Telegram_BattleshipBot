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
    def __init__(self, log1, log2):
        self.playerIds.append(log1)
        self.playerIds.append(log2)
        for n in range(5):
            self.MapPlayer1.append([0]*5)
            self.MapPlayer2.append([0]*5)
    def getPlayersIds(self):
        return self.playerIds

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
