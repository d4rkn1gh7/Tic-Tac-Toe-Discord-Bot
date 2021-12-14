import discord
from discord.ext.commands.converter import ColourConverter

BLANK = "BLANK"
pos_1 = 0
pos_2 = 1
pos_3 = 2
pos_4 = 3
pos_5 = 4
pos_6 = 5
pos_7 = 6
pos_8 = 7
pos_9 = 8

REACTION_EMOJI = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","❗"]

async def LoadGame(ctx,bot):
    embed =  discord.Embed(
        title = "Welcome to Tic-Tac-Toe Game! Play and have some fun!",
        description = "Press ✅ to play and ❌ to exit"
    )
    await ctx.channel.purge(limit=1)
    msg = await ctx.send(embed=embed)
    await msg.add_reaction('✅')
    await msg.add_reaction('❌')
    
    def checkReaction(reaction,user):
        return user != bot.user and (str(reaction)=='✅' or str(reaction)=='❌')

    reaction,user = await bot.wait_for("reaction_add",timeout=30.0, check = checkReaction)

    if str(reaction) == '✅':
        await tictactoe(ctx,bot)
    elif str(reaction) == '❌':
        await ctx.send("Thank you!. Come again!")


async def tictactoe(ctx,bot):

    emojilist = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","❗"]
    board = [BLANK,BLANK,BLANK,
            BLANK,BLANK,BLANK,
            BLANK,BLANK,BLANK]
    
    currentPlayer = 2
    player_1 = await getUserChar(ctx,bot,currentPlayer-1)
    player_2 = await getUserChar(ctx,bot,currentPlayer)
    await ctx.channel.purge(limit=3)
    def checkNotBot(reaction,user):
        return user != bot.user   
    turn = 1
    while CheckWin(player_1,player_2,board) == BLANK and turn <= 9:
        await ctx.send(f"Player {currentPlayer%2 + 1}'s turn")
        msg = await ctx.send(printboard(player_1,player_2,board))
        for i in range(len(emojilist)):
            await msg.add_reaction(emojilist[i])
        reaction,user = await bot.wait_for("reaction_add",timeout=30.0,check=checkNotBot)
        print(str(reaction.emoji))
        if str(reaction.emoji) == "❗":
            print("Closed")
            turn = 100
            await ctx.channel.purge(limit=2)
        else:
            if currentPlayer%2==0:
                makemove(reaction.emoji,emojilist,player_1,board)
            else:
                makemove(reaction.emoji,emojilist,player_2,board)
            await ctx.channel.purge(limit=2)
        
        winner =CheckWin(player_1,player_2,board)
        if winner != BLANK:
            await ctx.send(f"Player {currentPlayer%2 + 1} has won! \n Do you want to play again?")
            msg = await ctx.send(printboard(player_1,player_2,board))
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
            reaction,user = await bot.wait_for("reaction_add",timeout=30.0,check=checkNotBot)
            if (str(reaction.emoji)=="✅"):
                emojilist = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","❗"]
                board = [BLANK,BLANK,BLANK,
                        BLANK,BLANK,BLANK,
                        BLANK,BLANK,BLANK]
                turn = 0
                currentPlayer = 1
                await ctx.channel.purge(limit=2)
            
            else:
                await ctx.channel.purge(limit=2)
                await ctx.send("Thank You for Playing Tic-Tac-Toe with this bot ❤️")
        elif turn>=9:
            await ctx.send("It's a tie !")
            msg = await ctx.send(printboard(player_1,player_2,board))
            await msg.add_reaction("✅")
            await msg.add_reaction("❌")
            reaction,user = await bot.wait_for("reaction_add",timeout=30.0,check=checkNotBot)
            if (str(reaction.emoji)=="✅"):
                emojilist = ["1️⃣","2️⃣","3️⃣","4️⃣","5️⃣","6️⃣","7️⃣","8️⃣","9️⃣","❗"]
                board = [BLANK,BLANK,BLANK,
                        BLANK,BLANK,BLANK,
                        BLANK,BLANK,BLANK]
                turn = 0
                currentPlayer = 1
                await ctx.channel.purge(limit=2)
            
            else:
                await ctx.channel.purge(limit=2)
                await ctx.send("Thank You for Playing Tic-Tac-Toe with this bot ❤️")


        currentPlayer += 1
        turn += 1        

def makemove(emoji,emojilist,player,board):
    for index in range(len(REACTION_EMOJI)):
        if REACTION_EMOJI[index] == emoji:
            board[index] = player
            emojilist.remove(emoji)
            break


def CheckWin(player_1,player_2,board):
    lineHOne = CheckDirection(pos_1,pos_2,pos_3,player_1,player_2,board)
    if lineHOne != BLANK:
        return lineHOne
    lineHTwo = CheckDirection(pos_4,pos_5,pos_6,player_1,player_2,board)
    if lineHTwo != BLANK:
        return lineHTwo
    lineHThree = CheckDirection(pos_7,pos_8,pos_9,player_1,player_2,board)
    if lineHThree != BLANK:
        return lineHThree
    lineVOne = CheckDirection(pos_1,pos_4,pos_7,player_1,player_2,board)
    if lineVOne != BLANK:
        return lineVOne
    lineVTwo = CheckDirection(pos_2,pos_5,pos_8,player_1,player_2,board)
    if lineVTwo != BLANK:
        return lineVTwo
    lineVThree = CheckDirection(pos_3,pos_6,pos_9,player_1,player_2,board)
    if lineVThree != BLANK:
        return lineVThree
    lineDOne = CheckDirection(pos_1,pos_5,pos_9,player_1,player_2,board)
    if lineDOne != BLANK:
        return lineDOne
    lineDTwo = CheckDirection(pos_3,pos_5,pos_7,player_1,player_2,board)
    if lineDTwo != BLANK:
        return lineDTwo
    return BLANK

def CheckDirection(pos1,pos2,pos3,player_1,player_2,board):
    if (board[pos1] == board[pos2] == board[pos3]) and (board[pos3] != BLANK):
        if board[pos1] == player_1:
            return player_1
        elif board[pos1] == player_2:
            return player_2
    else:
        return BLANK

def printboard(player_1,player_2,board):
    blank_char = "⬜"
    board_message = ""
    tile = 1
    for x in range(len(board)):
        if board[x] == BLANK:
            if tile%3==0:
                board_message += blank_char + "\n"
            else:
                board_message += blank_char
        if board[x] == player_1:
            if tile%3 == 0:
                board_message += player_1 + "\n"
            else:
                board_message += player_1
        if board[x] == player_2:
            if tile%3 == 0:
                board_message += player_2 + "\n"
            else:
                board_message += player_2
        tile += 1
    return board_message



async def getUserChar(ctx,bot,currentPlayer):
    await ctx.send("Player " + str(currentPlayer)+ " Pick your charecter! (React with an emoji)")
    def checkNotBot(reaction,user):
        return user != bot.user
    
    reaction,user = await bot.wait_for("reaction_add",timeout=30.0, check=checkNotBot)

    return str(reaction.emoji)








                                   
