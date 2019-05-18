from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp
import math 


app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/game")
def game():
    if not "board" in session:
        session["board"] = [[None,None,None],
                            [None,None, None],
                            [None,None, None]]
        session["turn"] = "Alice"    
    ans = CheckWinner(session["board"])
    if(ans[0] == True):
        return render_template("finish.html",ans=f"{ans[1]} Player is Won!")
    elif(ans[0] == False and ans[1] == "Draw"):
        return render_template("finish.html",ans="Its a Draw!")
    else:
        return render_template("game.html",game=session["board"],turn=session["turn"])

@app.route("/play/<int:row>/<int:col>")
def play(row,col):
    session["board"][row][col] = session["turn"] 
    if session["turn"] == "Alice":
        session["turn"] = "Bob"
    else:
        session["turn"] = "Alice"
    return redirect(url_for("game"))

@app.route("/clear")
def clear():
    session["board"] = [[None,None,None],
                        [None,None, None],
                        [None,None, None]]
    session["turn"] = "Alice"
    return redirect(url_for("game"))
    
def CheckWinner(board): # [x,y] for x iff game is finished with winner and y = "Draw" if the game is draw, else, the winner (["Alice","Y"])
    # Checking the rows..
    for i in range(3):
        for j in range(3):
            if(board[i][0] == None):
                break
            if(board[i][0] == board[i][1] and board[i][1] == board[i][2]):
                return [True, board[i][0]]

    # Checking the columns..
    for i in range(3):
        for j in range(3):
            if(board[0][i] == None):
                break
            if(board[0][i] == board[1][i] and board[1][i] == board[2][i]):
                return [True, board[0][i]]

    # Checking the diagonals..
    if(board[0][0] == board[1][1] and board[1][1] == board[2][2]):
         if(board[0][0] != None):
             return [True, board[0][0]]

     # Checking the diagonals..
    if(board[2][0] == board[1][1] and board[1][1] == board[0][2]):
         if(board[1][1] != None):
             return [True, board[1][1]] 

    for i in range(3):
        for j in range(3):
            if(board[i][j] == None):
                return [False, board[0][0]]  # Its Return somthing, never mind[1]. 

    # Its Draw!
    return [False, "Draw"]
  
@app.route("/help")
def help():
    ans = minimax(session["board"],session["turn"])
    if ans[1] is not None:
        return redirect(url_for('play', row=ans[1][0], col=ans[1][1]))
    
    
def minimax(board,turn):
    ans = CheckWinner(board)
    if(ans[0] == True and ans[1] == "Alice"):
        return (1,None)
    elif(ans[0] == True and ans[1] == "Bob"):
        return (-1,None)
    elif(ans[0] == False and ans[1] == "Draw"):
        return (0,None)
    else: # Next Step of Recursion
        moves = []
        for i in range(3):
            for j in range(3):
                if(board[i][j] == None):
                    moves.append((i,j))
        # All Moves that avaliabe are now at moves
        if turn == "Alice":
            value = -2
            for i,j in moves:
                board[i][j] = "Alice"
                result = minimax(board,"Bob")[0]
                if(value < result):
                    value = result
                    step = (i,j)
                board[i][j] = None
        elif turn == "Bob": # turn is "Bob"
            value = 2
            for i,j in moves:
                board[i][j] = "Bob"
                result = minimax(board,"Alice")[0]
                if(value > result):
                    value = result
                    step = (i,j)
                board[i][j] = None
        return (value,step)    

if __name__ == '__main__':
    app.debug = True
    app.run()