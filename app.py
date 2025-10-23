from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/kisan-bot')
def kisan_bot():
    return render_template('kisan_bot.html')

@app.route('/expert-desk')
def expert_desk():
    return render_template('expert.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/team')
def about():
    return render_template('team.html')

if __name__ == "__main__":
    app.run(debug=True)