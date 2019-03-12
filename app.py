from flask import Flask, render_template,request
from web_crawler import do

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('front.html') 

@app.route('/Search',methods = ['POST', 'GET'])
def Search():
	if request.method == 'POST':
	    result = request.form['keyword']
	    
	    fo=open("input.txt","w")
	    fo.write(result)
	    fo.close()
	    do()

	return render_template('front.html') 

    	

if __name__ == '__main__':
    app.run(host='127.0.0.1', port=8080, debug=True)

    
