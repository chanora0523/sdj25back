from flask import Flask,request,jsonify,abort
import dbm
from janome.tokenfilter import Tokenizer
from flask_cors import CORS

app = Flask( __name__)
CORS(app)

@app.route('/')
def root():
    return 'robotics and design'

@app.route('/greet/<name>')
def greet(name):
    return f'hello, {name}'

def wakachi(s):
    t = Tokenizer()
    words = t.tokenize(s,wakati=True)
    ret = ""
    for w in words:
        ret += w + '/'
    return ret
    
@app.route('/v1/messages',methods=['POST'])
def post():
    data = request.get_json()
    print(data['message'])
    id = -1
    with dbm.open('message.dbm','c') as db:
        if 'id' not in db:
            db['id'] = str(0)
        id = int(db['id'])
        id += 1
        db['id'] = str(id)
        db[str(id)] = data['message']
        

    return jsonify({"id": id} )

@app.route('/v1/messages',methods=['GET'])
def get_all():

    msgs = []
    with dbm.open('messeage.dbm','c') as db:
        for k in db.keys():
            if str(k) == b'id': continue
            msgs.append(k,db[k].decode('utf-8'))
    print(msgs)
    return jsonify(msgs),200


if __name__ == '__main__':
    app.run(host='0.0.0.0',debug = True)#外からのアクセスのため
