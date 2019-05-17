from flask import Flask, render_template, session, redirect, url_for
from flask_session import Session
from tempfile import mkdtemp

app = Flask(__name__)

app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

app = Flask(__name__)
app.secret_key = "super secret key"

@app.route("/")
def index():
    if not "board" in session:
        session["board"] = [[None,None,None],
                            [None,None, None],
                            [None,None, None]]
        session["turn"] = "X"    
    ans = CheckWinner(session["board"])
    if(ans[0] == True):
        return render_template("index.html",game=session["board"],turn=session["turn"],ans=f"{ans[1]} Player is Won!")
    elif(ans[0] == False and ans[1] == "Draw"):
        return render_template("index.html",game=session["board"],turn=session["turn"],ans="Its a Draw!")
    else:
        return render_template("index.html",game=session["board"],turn=session["turn"])

@app.route("/play/<int:row>/<int:col>")
def play(row,col):
    session["board"][row][col] = session["turn"] 
    if session["turn"] == "X":
        session["turn"] = "O"
    else:
        session["turn"] = "X"
    return redirect(url_for("index"))

@app.route("/clear")
def clear():
    session["board"] = [[None,None,None],
                            [None,None, None],
                            [None,None, None]]
    session["turn"] = "X"
    return redirect(url_for("index"))
    
def CheckWinner(board):
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

     #Checking if its draw..
    for i in range(3):
        for j in range(3):
            if(board[i][j] == None):
                return [False, board[0][0]]  

    # Its Draw!
    return [False, "Draw"]
    
if __name__ == '__main__':
    app.debug = True
    app.run()