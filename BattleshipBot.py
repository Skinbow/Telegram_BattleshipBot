import telebot
import config
import random

bot = telebot.TeleBot(config.token)

waitingForToken = []

class User:
    id = 0


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

waitingList = {}
GamesList = []

@bot.message_handler(commands=["create", "join", "exit"])
def ReactToCommands(message):
    if message.text == "/create":
        token = random.randint(10000, 99999)
        while token in waitingList:
            token = random.randint(10000, 99999)
        waitingList[token] = message.chat.id
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
                bot.send_message(ids[1], "Игра прерванна!")
                GamesList.remove(game)
                break

@bot.message_handler(content_types=["text"])
def Battleships(message):
    #for game in GamesList:
    #    if message.chat.id in game.getPlayersIds():

    # Establishing a connection between two players
    if message.chat.id in waitingForToken:
        try:
            if int(message.text) in waitingList:
                # Joining the two players
                AGame = Game(waitingList[int(message.text)], message.chat.id)
                GamesList.append(AGame)
                print(AGame.getPlayersIds())
                # Deleting players from waitingForToken and waitingList
                #
                print(waitingForToken)
                print(waitingList)
                #
                waitingForToken.remove(message.chat.id)
                del waitingList[int(message.text)]
                #
                print(waitingForToken)
                print(waitingList)
                #
                bot.send_message(message.chat.id, "Соеденинение установлено!")
            else:
                bot.send_message(message.chat.id, "Такого токена не существует!")
        except:
            bot.send_message(message.chat.id, "Токен не действительный! Токен должен содержать 5 цифр.")


if __name__ == "__main__":
    bot.polling(none_stop=True)
