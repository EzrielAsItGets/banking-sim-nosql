from flask import Flask, redirect, url_for, render_template, request, session
import ATMSimulation
# from datetime import timedelta

app = Flask(__name__)
app.secret_key = "Fool me once...shame on you. Fool me...won't get fooled again"
# app.permanent_session_lifetime = timedelta(minutes=5)

@app.route("/")
def home():
    if "account_id" in session:
        if "pin" in session:
            return redirect(url_for("account"))
        else:
            return redirect(url_for("pin"))
    else:
        return redirect(url_for("login"))

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        acc = request.form["acc"]
        if ATMSimulation.idValidate(acc):
            session["account_id"] = acc
            return redirect(url_for("pin"))
        else:
            return redirect(url_for("login")) # Invalid Account
    else:
        if "account_id" in session:
            return redirect(url_for("pin"))
        
        return render_template("login.html")
    
@app.route("/pin", methods = ["POST", "GET"])
def pin():
    if "account_id" in session:
        acc = session["account_id"]
        if request.method == "POST":
            pin = request.form["pin"]
            try:
                int(pin)
            except ValueError:
                return redirect(url_for("pin")) # Invalid PIN
            
            if ATMSimulation.pinValidate(acc, int(pin)):
                session["pin"] = pin
                return redirect(url_for("account"))
            else:
                return redirect(url_for("pin")) # Incorrect PIN
            
        else:
            if "pin" in session:
                return redirect(url_for("account"))
            
            return render_template("pin.html")
        
    else:
        return redirect(url_for("login"))

@app.route("/account", methods = ["POST", "GET"])    
def account():
    if "account_id" in session:
        if "pin" in session:
            acc = session["account_id"]
            name = ATMSimulation.getName(acc)
            cbal, sbal = ATMSimulation.getBalances(acc)
            if request.method == "POST":
                typ = request.form["type"]
                trans = request.form["trans"]
                total = request.form["total"]
                try:
                    numTotal = 0
                    numTotal = float(total)
                except ValueError:
                    return redirect(url_for("account")) # Invalid amount input
                finally:
                    if numTotal <= 0:
                        numTotal = 0
                    
                if (numTotal > 0):
                    if trans == "D":
                        ATMSimulation.deposit(acc, typ, numTotal)
                    elif trans == "W":
                        if not ATMSimulation.withdraw(acc, typ, numTotal):
                            redirect(url_for("account")) # Insufficient Funds
                    else:
                        if not ATMSimulation.transfer(acc, typ, numTotal):
                            redirect(url_for("account")) # Insufficient Funds
                    
                    return redirect(url_for("account"))
                else:
                    return redirect(url_for("account")) # Invalid transaction amount
                
            else:
                return render_template("type.html", name=name, cbal=cbal, sbal=sbal)
            
        else:
            return redirect(url_for("pin"))
        
    else:
        return redirect(url_for("login"))
            

# TEST (Remove later)
@app.route("/user")
def user():
	if "account_id" in session:
		acc = session["account_id"]
		return f"<h1>{acc}</h1>"
	else:
		return redirect(url_for("login"))

@app.route("/logout")
def logout():
    session.pop("account_id", None)
    session.pop("pin", None)
    return redirect(url_for("login"))

if __name__ == "__main__":
	app.run()