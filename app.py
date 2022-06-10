import csv
from flask import Flask, jsonify, request
from flask_restful import Api
from helperfunctions import predi, filePredict
from flask_cors import CORS, cross_origin
import pymysql as mdb
app = Flask(__name__)
api = Api(app)
# CORS(app)

def inse(text, res):
	res = str(res)
	mydb = mdb.connect(host="127.0.0.1", user="root", passwd="", database="tms")
	mycursor = mydb.cursor()
	sql = "INSERT into review2(post,res) values(%s,%s)"
	val = (text, res)
	mycursor.execute(sql, val)
	mydb.commit()
	mydb.close()
# cors = CORS(app, resources={r"/predict": {"origins": "*"}})
# app.config['CORS_HEADERS'] = 'Content-Type'

@app.route('/', methods=['POST','GET'])
@cross_origin()
def helloworld():
	# data = [{"data": "Hello World","id" : "1"},{"data": "Hello from me","id" : "2"},{"data": "Hello","id" : "3"}]
	if(request.method=='POST'):
		fileName = request.args.get("file")
		file = open(r'D:/xampp/htdocs/fakereview/upload/' + fileName)
		csvreader = csv.reader(file)
		header = csvreader
		print(header)
		rows = []
		for row in csvreader:
			rows.append(row[0])
		print(rows)
		file.close()

		rows = filePredict(rows)
		print(rows)
		f = open(r'D:/xampp/htdocs/fakereview/upload/' + fileName, "w+")
		f.close()

		with open(r'D:/xampp/htdocs/fakereview/upload/' + fileName, 'w') as file:
			for row in rows:
				for x in row:
					file.write(str(x) + ', ')
				file.write('\n')
			file.close()
		return jsonify(rows)

	if(request.method=='GET'):
		review = request.args.get("review")
		res = predi(str(review))
		print(res)
		inse(str(review), res)
		di = {"result": res}
		return jsonify(di)


# @app.route("/<string:rtext>",methods=['GET'])
# @cross_origin()
# def predict(rtext):
#     #text = "It was worst experience"
# 	res =  predi(str(rtext))
# 	inse(str(rtext),res)
# 	di = {"result":res}
# 	return jsonify(di)

if __name__=="__main__":
  app.run(debug=True,port=5000)
        