from flask import Flask, redirect, url_for, render_template, request, session, flash
import ATMSimulation

app = Flask(__name__)
app.secret_key = "Fool me once...shame on you. Fool me...won't get fooled again"

@app.route("/debug", methods=["POST", "GET"])
def debug():
    if request.method == "POST":
        account_id = request.form["acc_id"]
        ssn = request.form["ssn"]
        name = request.form["name"]
        pin = request.form["pin"]
        check = request.form["check"]
        save = request.form["save"]
        if ATMSimulation.idValidate(account_id):
            flash("Account ID Exists!")
        else:
            ATMSimulation.createAccount(account_id, ssn, name, pin, check, save)
    return render_template("debug.html")

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
            flash("Invalid Account")
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

            flag = True
            try:
                int(pin)
            except ValueError:
                flash("Invalid PIN")
                flag = False
            
            if flag:
                if ATMSimulation.pinValidate(acc, int(pin)):
                    session["pin"] = pin
                    return redirect(url_for("account"))
                else:
                    flash("The PIN you inputted does not match this account's PIN.")
            
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