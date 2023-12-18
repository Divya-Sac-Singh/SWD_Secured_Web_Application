from flask import Flask, render_template, request, redirect, url_for
import getpass
from prettytable import PrettyTable

app = Flask(__name__)
#game = None
users = {}


class DiceGame:
    def __init__(self):
        self.users = {'admin': 'admin123'}
        self.players = {}
        self.player_choices = {'Play': {}, 'Quit': {}}
        self.registered_users = {'admin': 'admin123'}
        self.current_player = None
game = DiceGame()

@app.route('/')
def home():
    return render_template('home.html')


@app.route('/admin', methods=['GET', 'POST'])
def admin():
    global game
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username == 'admin' and password == game.users['admin']:
            return redirect(url_for('admin_menu'))
        else:
            return render_template('admin_login.html', message="Invalid credentials. Please try again.")
    return render_template('admin_login.html', message="")


@app.route('/admin/menu', methods=['GET', 'POST'])
def admin_menu():
    global game
    if request.method == 'POST':
        choice = request.form['choice']

        if choice == 'view_all_players':
            return redirect(url_for('view_all_players'))
        elif choice == 'add_player':
            return redirect(url_for('add_player'))
        elif choice == 'delete_player':
            return redirect(url_for('delete_player'))
        elif choice == 'update_player':
            return redirect(url_for('update_player'))
        elif choice == 'logout':
            return redirect(url_for('home'))

    return render_template('admin_menu.html', players=game.players, player_choices=game.player_choices)


@app.route('/view_all_players')
def view_all_players():
    table = PrettyTable()
    table.field_names = ['ID', 'Username', 'Password', 'Play', 'Quit']

    for i, (username, password) in enumerate(game.players.items(), start=1):
        play_choice = 'Yes' if game.player_choices['Play'].get(username) else '-'
        quit_choice = 'Yes' if game.player_choices['Quit'].get(username) else '-'
        table.add_row([i, username, password, play_choice, quit_choice])

    return render_template('view_all_players.html', table=table, players=game.players, choices=game.player_choices)

@app.route('/admin/add_player', methods=['GET', 'POST'])
def add_player():
    global game
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        game.players[username] = password
        return redirect(url_for('view_all_players'))
    return render_template('add_player.html')


@app.route('/admin/delete_player', methods=['GET', 'POST'])
def delete_player():
    global game
    if request.method == 'POST':
        username = request.form['username']
        if username in game.players:
            del game.players[username]
        return redirect(url_for('view_all_players'))
    return render_template('delete_player.html')


@app.route('/admin/update_player', methods=['GET', 'POST'])
def update_player():
    global game
    if request.method == 'POST':
        username = request.form['username']
        new_password = request.form['new_password']
        if username in game.players:
            game.players[username] = new_password
        return redirect(url_for('view_all_players'))
    return render_template('update_player.html')


@app.route('/admin/logout')
def logout():
    return redirect(url_for('home'))


@app.route('/player', methods=['GET', 'POST'])
def player():
    global game
    if request.method == 'POST':
        player_choice = request.form['player_choice']
        if player_choice == 'sign_up':
            return redirect(url_for('sign_up'))
        elif player_choice == 'login':
            return redirect(url_for('login'))
        else:
            return render_template('player.html', message="Invalid choice. Please try again.")
    return render_template('player.html', message="")


@app.route('/signup', methods=['GET', 'POST'])
def sign_up():
    global game
    global users
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username is already taken
        if username in users:
            return render_template('sign_up.html', message='Username already taken. Please choose another.')

        # Add the new user to the dictionary
        users[username] = password

        # Redirect to the login page after successful signup
        return redirect(url_for('login'))

    return render_template('sign_up.html', message="")


@app.route('/login', methods=['GET', 'POST'])
def login():
    global game
    global users
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        # Check if the username and password match any user in the dictionary
        if username in users and users[username] == password:
            # Redirect to the dice game page after successful login
            return redirect(url_for('gameplay', username=username))
        else:
            return render_template('login.html', message='Invalid username or password. Please try again.')

    return render_template('login.html', message="")


@app.route('/gameplay', methods=['GET', 'POST'])
def gameplay():
    global game
    if request.method == 'POST':
        game_option = request.form.get('game_option')

        # Placeholder for gameplay logic
        if game_option == 'play':
            # Do something when the user chooses to play
            pass
        elif game_option == 'quit':
            # Do something when the user chooses to quit
            # Redirect the player to the home page
            return redirect(url_for('home'))

    # Render the gameplay page for GET requests
    return render_template('gameplay.html', username=request.args.get('username'))


if __name__ == '__main__':
    game = DiceGame()
    app.run(debug=True)
