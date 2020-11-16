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
        choice = request.form["type"]
        if choice == "C":
            if ATMSimulation.idValidate(account_id):
                flash("Account ID Exists!")
            else:
                ATMSimulation.createAccount(account_id, ssn, name, pin, check, save)
                flash("Account Created")
        elif choice == "D":
            if ATMSimulation.idValidate(account_id):
                ATMSimulation.deleteAccount(account_id)
                flash("Account Deleted")
            else:
                flash("Account Doesn't Exist!")

    return render_template("debug.html")

@app.route("/", methods=["POST", "GET"])
def home():
    session.pop("account_id", None)
    session.pop("pin", None)

    return render_template("home.html")

@app.route("/login", methods=["POST", "GET"])
def login():
    if request.method == "POST":
        acc = request.form["acc"]
        if ATMSimulation.idValidate(acc):
            session["account_id"] = acc
            return redirect(url_for("pin"))
        else:
            flash("Invalid Account")
			
    return render_template("login.html")

@app.route("/pin", methods=["POST", "GET"])
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
            
    return render_template("pin.html")

@app.route("/account", methods=["POST", "GET"])
def account():
    if "account_id" in session:
        if "pin" in session:
            acc = session["account_id"]
            name = ATMSimulation.getName(acc)
            cbal, sbal = ATMSimulation.getBalances(acc)
            cbal = format(cbal, '.2f')
            sbal = format(sbal, '.2f')

    return render_template("options.html", name=name, cbal=cbal, sbal=sbal)

@app.route("/deposit_choice", methods=["POST", "GET"])
def deposit_choice():
    session.pop("typ", None)

    if "account_id" in session:
        if "pin" in session:
            acc = session["account_id"]
            name = ATMSimulation.getName(acc)
            if request.method == "POST":
                typ = request.form.get("choice", None)
                
                if typ != None:
                    session["typ"] = typ
                    return redirect(url_for("deposit"))

    return render_template("deposit_choice.html", name=name)

@app.route("/deposit", methods=["POST", "GET"])
def deposit():
    if "account_id" in session:
        if "pin" in session:
            if "typ" in session:
                acc = session["account_id"]
                name = ATMSimulation.getName(acc)
                typ = session["typ"]
                if request.method == "POST":
                    total = request.form["CustomNumber"]
                    try:
                        numTotal = 0
                        numTotal = float(total)
                    except ValueError:
                        return redirect(url_for("deposit")) # Invalid amount input
                    finally:
                        if numTotal <= 0:
                            numTotal = 0
                    
                    if (numTotal > 0):
                        ATMSimulation.deposit(acc, typ, numTotal)

    return render_template("deposit.html", name=name)

@app.route("/withdraw_choice", methods=["POST", "GET"])
def withdraw_choice():
    session.pop("typ", None)

    if "account_id" in session:
        if "pin" in session:
            acc = session["account_id"]
            name = ATMSimulation.getName(acc)
            if request.method == "POST":
                typ = request.form.get("choice", None)
                
                if typ != None:
                    session["typ"] = typ
                    return redirect(url_for("withdraw"))

    return render_template("withdraw_choice.html", name=name)

@app.route("/withdraw", methods=["POST", "GET"])
def withdraw():
    if "account_id" in session:
        if "pin" in session:
            if "typ" in session:
                acc = session["account_id"]
                name = ATMSimulation.getName(acc)
                typ = session["typ"]
                if request.method == "POST":
                    total = request.form["CustomNumber"]
                    try:
                        numTotal = 0
                        numTotal = float(total)
                    except ValueError:
                        return redirect(url_for("withdraw")) # Invalid amount input
                    finally:
                        if numTotal <= 0:
                            numTotal = 0
                    
                    if (numTotal > 0):
                        if not ATMSimulation.withdraw(acc, typ, numTotal):
                            redirect(url_for("withdraw")) # Insufficient Funds

    return render_template("withdraw.html", name=name)

@app.route("/transfer_choice", methods=["POST", "GET"])
def transfer_choice():
    session.pop("typ", None)

    if "account_id" in session:
        if "pin" in session:
            acc = session["account_id"]
            name = ATMSimulation.getName(acc)
            if request.method == "POST":
                typ = request.form.get("choice", None)
                
                if typ != None:
                    session["typ"] = typ
                    return redirect(url_for("transfer"))

    return render_template("transfer_choice.html", name=name)

@app.route("/transfer", methods=["POST", "GET"])
def transfer():
    if "account_id" in session:
        if "pin" in session:
            if "typ" in session:
                acc = session["account_id"]
                name = ATMSimulation.getName(acc)
                typ = session["typ"]
                if request.method == "POST":
                    total = request.form["CustomNumber"]
                    try:
                        numTotal = 0
                        numTotal = float(total)
                    except ValueError:
                        return redirect(url_for("transfer")) # Invalid amount input
                    finally:
                        if numTotal <= 0:
                            numTotal = 0
                    
                    if (numTotal > 0):
                        if not ATMSimulation.transfer(acc, typ, numTotal):
                            redirect(url_for("transfer")) # Insufficient Funds

    return render_template("home.html")

if __name__ == "__main__":
	app.run()