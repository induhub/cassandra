from pycassa.system_manager import *
from pycassa.pool import ConnectionPool
from pycassa.columnfamily import ColumnFamily
import os

def setup_keyspace(keyspace):
    col_families = ['profile'            
                    ]
    sys = SystemManager()
    sys.create_keyspace(keyspace, SIMPLE_STRATEGY, {'replication_factor': '1'})
    for each in col_families:
        sys.create_column_family(keyspace, each)
    sys.close()


try:
   setup_keyspace('minions')
   setup_keyspace('chinions')
except:
   print 'keyspace minions and chinions already created'
pool = ConnectionPool('minions')
col_fam = ColumnFamily(pool, 'profile')

from flask import Flask
from flask import render_template
from flask import request



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')


@app.route('/getprofile', methods=['GET'])
def search():
    if request.method == 'GET':
        myvar = request.args.get("q")
        
       
        return result
	
        
@app.route('/profile', methods=['GET','POST'])
def data():
    if request.method == 'GET':
		#cassandra se nikalo
        result = (col_fam.get('user_id'))
        context = {'name': result['name'], 'profile_pic': result['profile_pic']}

        return render_template('profile.html',**context)


    if request.method == 'POST':
        try:
            doc = request.form
            #print str(request.files['profile_pic'])
            try:


                img_file = request.files['profile_pic']
            except Exception as ex:
                print ex
           
            #print installation_dir
            path = os.path.join('/home/indu/pro/cassandra/static', doc['profile_pic'])
            print path
            img_file.save(path)
            col_fam.insert('user_id',doc)           
  	    return "added"
        except Exception as ex:
            return str(ex)
    	
#res = es.search(index="pagemango", body={"query": {"match_all": {}}})
#print res

if __name__ == '__main__':
    app.run(debug=True)
