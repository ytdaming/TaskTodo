from flask import Flask
app = Flask(__name__)
# print(super.__name__)
print(app.__dict__)
@app.route('/')
def index():
    return 'Hello World'
if __name__ == '__main__':
    app.debug = True # 调试模式，生产模式关掉debug
    app.run()