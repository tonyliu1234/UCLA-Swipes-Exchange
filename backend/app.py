from flask import Flask

app = Flask(__name__)



@app.route('/register', methods=['POST'])
def register():
  pass

@app.route('/login', methods=['POST'])
def login():
  pass

@app.route('/orders', methods=['GET'])
def get_orders():
  pass

@app.route('/orders', methods=['POST'])
def create_order():
  pass

if __name__ == '__main__':
  app.run(debug=True)
  