#!/usr/bin/python3

from flask import Flask
from flask_restful import Resource, Api, abort, reqparse, abort, fields, marshal_with
from flask_sqlalchemy import SQLAlchemy
import logging
import time
import cleanup

logging.basicConfig(filename='resourceAlloc.log', level=logging.DEBUG, format='%(asctime)s:%(levelname)s:%(message)s')

app = Flask(__name__)
api = Api(app)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class addToDb(db.Model):
    virtmach = db.Column(db.Integer, primary_key=True)
    hostname = db.Column(db.String(20), nullable=False) 
    ip = db.Column(db.String(20), nullable=False) 
    allocstatus = db.Column(db.String(20), nullable=False)
    user = db.Column(db.String(30), nullable=True)
    timestamp = db.Column(db.Integer, nullable=True)

    def __repr__(self):
        #return f"serverResources(hostname = {hostname}, ip = {ip}, allocstatus = {allocstatus})"
        return f"serverResources(hostname = {hostname}, ip = {ip}, allocstatus = {allocstatus}, user = {user}, timestamp = {timestamp})"

db.create_all()

resPutArgs = reqparse.RequestParser()
resPutArgs.add_argument('hostname', type=str, help="Hostname of the VM", required=True)
resPutArgs.add_argument('ip', type=str, help="IP of the VM", required=True)
resPutArgs.add_argument('allocstatus', type=str, help="Allocation status of the VM", required=True)
resPutArgs.add_argument('user', type=str, help="IP of the VM", required=False)
resPutArgs.add_argument('timestamp', type=str, help="IP of the VM", required=False)

resGetArgs = reqparse.RequestParser()
resGetArgs.add_argument('hostname', type=str, help="Hostname of the VM", required=False)
resGetArgs.add_argument('ip', type=str, help="IP of the VM", required=False)
resGetArgs.add_argument('allocstatus', type=str, help="Allocation status of the VM", required=False)
resGetArgs.add_argument('user', type=str, help="IP of the VM", required=True)
resGetArgs.add_argument('timestamp', type=str, help="IP of the VM", required=False)

resUpdateArgs = reqparse.RequestParser()
resUpdateArgs.add_argument('hostname', type=str, help='Hostname of the VM')
resUpdateArgs.add_argument('ip', type=str, help='IP of the VM')
resUpdateArgs.add_argument('allocstatus', type=str, help='Allocation status of the VM')
resUpdateArgs.add_argument('user', type=str, help="IP of the VM", required=True)
resUpdateArgs.add_argument('timestamp', type=str, help="IP of the VM", required=False)

resource_fields = {
        'virtmach': fields.Integer,
        'hostname': fields.String,
        'ip': fields.String,
        'allocstatus': fields.String,
        'user': fields.String,
        'timestamp': fields.Integer,
        }

resourceDict={}

class serverResources(Resource):
    @marshal_with(resource_fields)
    def get(self, vmid):
        gargs = resGetArgs.parse_args()
        #result = addToDb.query.filter_by(allocstatus="Available").first()
        result = addToDb.query.filter_by(allocstatus="Available").first()
        if not result:
            logging.debug('Got allocation request, but none of the VMs available')
            abort(404, message='VMs not available for assignment, either all are reserved or down for maintenance')
        result.allocstatus = "Allocated"
        result.user = gargs['user']
        result.timestamp = time.time()
        db.session.commit()
        s1 = "Machine with IP " + str(result.ip) + " is marked Allocated and assigned to customer at: \n" + str(time.ctime()) 
        logging.debug(s1)
        return result  

    @marshal_with(resource_fields)
    def put(self, vmid):
        args = resPutArgs.parse_args()
        if args['user'] != 'ADMINISTRATOR':
            abort(404, message='You do not have privilege to perform this activity')
        result = addToDb.query.filter_by(virtmach=vmid).first()
        if result:
            abort(409, message="VMID already exists")
        #print(args)
        poolEntry = addToDb(virtmach=vmid, hostname=args['hostname'], ip=args['ip'], allocstatus=args['allocstatus'])
        db.session.add(poolEntry)
        db.session.commit()
        return poolEntry, 201

    @marshal_with(resource_fields)
    def patch(self, vmid):
        uargs = resUpdateArgs.parse_args()
        result = addToDb.query.filter_by(ip=uargs['ip']).first()
        if not result:
            abort(404, message='the ip does not exist')
        if uargs['user'] != result.user:
            abort(404, message='You are not the same user whom machine was allocated')
        result.allocstatus = "Available"
        result.user = None
        usage_time = time.time() - result.timestamp
        result.timestamp = 0
        db.session.commit()
        s1 = "Machine with IP " + str(result.ip) +\
                " is added back to the VM Resource Pool and marked Available at: \n" + \
                str(time.ctime() +\
                "\nMachine was used for " + str(usage_time) + " seconds") 
        logging.debug(s1)
        cleanup.sshConn(str(result.ip))
        return result, 201

    @marshal_with(resource_fields)
    def delete(self, vmid):
        #args = resPutArgs.parse_args()
        result = addToDb.query.filter_by(virtmach=vmid).first()
        if result:
            db.session.delete(result)
            db.session.commit()
            #resultall = addToDb.query.filter_by(virtmach=vmid).all()
            #resultall = addToDb.query.order_by(addToDb.virtmach).all()
            resultall = addToDb.query.all()
            return resultall, 200
        else:
            abort(404, message="VMID does not exists")

api.add_resource(serverResources, "/virtualmachine/<int:vmid>")    

if __name__ == '__main__':
    app.run(debug=True)
