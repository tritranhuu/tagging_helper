from flask import Flask, render_template, redirect, url_for, request, session
import json
import codecs
import os

PATH = ""

app = Flask(__name__, static_folder='templates/static')
app.secret_key = 'super secret key'
app.config['SESSION_TYPE'] = 'filesystem'

data = {}


@app.route('/next', methods=['GET', 'POST'])
def resultGUI():
    error = None
    
    # data = session['data']
    global data
    file_name = session["file_name"]
    if request.method == 'GET':
        return redirect('/')
    else:
        origin = session['origin']
        tag = int(request.form['submit_button'])
        i = session['sent']
        session['sent'] += 1
        data['hits'][i]["relate_q_q"] = tag
        if session['sent']<10:                
            return render_template('index.html', error=error, file_name=file_name, dat=data["hits"][i+1]["question"], ori=origin, num=(i+2))
        else:
            path = PATH + "done/"
            if not os.path.exists(path):
                os.makedirs(path)
            file_save = path + file_name
            f = codecs.open(file_save, 'w', encoding='utf-8')
            json.dump(data, f, indent=4, ensure_ascii=False)
            os.remove(PATH + file_name) 
            session['sent'] = 0
            return redirect('/tag')


@app.route('/', methods=['GET'])
def begin():
    session['sent'] = 0
    return render_template('users.html')
 
@app.route('/getpath', methods=['POST'])
def path():
    global PATH
    prefix = request.form['pre']
    suffix = request.form['suf']
    PATH = prefix + suffix
    return redirect('/tag')
 



@app.route('/tag', methods=['GET'])
def findGUI():
    session['sent'] = 0
    error = None
    global data
    if request.method == 'POST':
        if int(request.form['price']) < 500:
            error = 'Invalid Credentials. Please try again.'
        else:
            return redirect(url_for('home'))
    if session['sent'] == 0:
        file_names = os.listdir(PATH)
        file_name = file_names[0]
        session['file_name'] = file_name
        data = json.load(open(PATH + file_name, encoding='utf-8'), encoding='utf-8')
        origin = data["origin_question"]
        session['origin'] = origin
        # session['data'] = data
        print(session['file_name'])
    return render_template('index.html', error=error, file_name=file_name, dat=data["hits"][0]["question"], ori=origin, num=1)
 
 
if __name__ == '__main__':
    
    app.run(host='0.0.0.0', port=5000, debug=True)