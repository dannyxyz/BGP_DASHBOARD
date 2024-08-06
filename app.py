from flask import Flask, render_template, request
import netmiko
from datetime import datetime

app = Flask(__name__)

def fetch_bgp_peer_status(host, username, password):
    # The same code as before
    # ...

def parse_bgp_summary_output(output):
    # The same code as before
    # ...

def parse_bgp_prefix_output(output):
    # The same code as before
    # ...

def display_peer_status_table(peer_status_data):
    # The same code as before
    # ...

def display_prefix_routing_table(prefix_routing_data):
    # The same code as before
    # ...

@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        host = request.form['host']
        username = request.form['username']
        password = request.form['password']

        peer_status_data, prefix_routing_data = fetch_bgp_peer_status(host, username, password)

        return render_template('index.html',
                               peer_status_data=peer_status_data,
                               prefix_routing_data=prefix_routing_data)
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)