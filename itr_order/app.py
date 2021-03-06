from flask import Flask, jsonify, abort, request, make_response, url_for
from flask.ext.httpauth import HTTPBasicAuth
import config as cf
import mailer
#import requests

app = Flask(__name__, static_url_path = "")
auth = HTTPBasicAuth()

@auth.get_password
def get_password(username):
    if username == cf.username:
        return cf.password    
    return None

@auth.error_handler
def unauthorized():
    return (make_response(jsonify( { 'error': 'Unauthorized access' } ), 403))
    # return 403 instead of 401 to prevent browsers from displaying the default auth dialog
    
@app.errorhandler(400)
def not_found(error):
    return (make_response(jsonify( { 'error': 'Bad request' } ), 400))

@app.errorhandler(503)
def unavail(error):
    return (make_response(jsonify( { 'error': 'Service Unavailable' } ), 503))


@app.errorhandler(404)
def not_found(error):
    return (make_response(jsonify( { 'error': 'Not found' } ), 404))

def validate_line(line, el):
        if(len(str(line[0])) == 0):
                el.append("NameError: The item name field is blank")
        if(len(str(line[3])) == 0):
                el.append("VendorError: The vendor field is blank")
        if(len(str(line[4])) == 0):
                el.append("QuantityError: The quantity field is blank")
        if(len(str(line[5])) == 0):
                el.append("UnitCostError: The unit cost field is blank")
        if(len(str(line[6])) == 0):
                el.append("CostError: The total cost field is blank")
        if(len(str(line[7])) == 0):
                el.append("ShippingCostError: The shipping cost field is required, if the shipping cost is unavailable, please use the value 'unknown'")
        if(len(str(line[10])) == 0):
                el.append("NoApprovalError: The request must be approved")
        if(type(line[0]) != str):
                el.append("NameValueError: The item name field does not contain a text string")
        if(type(line[3]) != str):
                el.append("VendorValueError: The vendor field does not contain a text string")
        if(type(line[10]) != str):
                el.append("ApprovalValueError: The approver field must contain text")
        return el

def validate_line2(line, el):
        unit = 0.0
        total = 0.0
        ship = 0.0
        try:
                unit = float(str(line[5]).strip('$'))
        except ValueError:
                el.append("UnitCostValueError: The unit cost field must be numeric")
        try:
                total = float(str(line[6]).strip('$'))
        except ValueError:
                el.append("CostValueError: The total cost field must be numeric")
        try:
                ship = float(str(line[7]).strip('$'))
                if not(((unit*int(line[4])) + ship) == total):
                        el.append("MathError: The unit price times the quantity, plus the shipping cost does not equal the total cost")
        except ValueError:
                pass
        
        return el

def validate_line3(line, el):
        if(len(line[2]) > 0):
                #Is URL valid?
                try:
                    r = requests.get(line[2])
                    if r.status_code != 200:
                        el.append("URLError: The supplied URL is not a valid link, please either fix the URL or leave the field blank")
                except:
                        raise
                        el.append("URLError: The supplied URL is not a valid link, please either fix the URL or leave the field blank")
        return el

def handle_errors(req, el):
    message = '  --  '.join(el)
    return(jsonify( { 'status' : 'false' , 'message' : message} ), 400)

def handle_success(req):
    message = "An item on the ITR order sheet has been changed or added:\n\n"
    message += "Item Name: %s\n Vendor: %s\n Total Price: %s\n Requestor:%s\n Approver:%s" % (req[0],req[3],req[6],req[9],req[10])
    message += '\n\nRegards,\nThe ITR order list robot'
    mailer.mail(cf.success_rcpts,'ITR Order list Change/Request',message)



@app.route('/api/v1/itr_order', methods = ['POST'])
@auth.login_required
def handle_order():
        if not (request.json and (len(request.json) == 12)):
            abort(400)
        el = []
        #1st level validation
        el = validate_line(request.json,el)
        if(len(el) > 0):
            return handle_errors(request.json,el)
        #2nd tier of checks
        el = validate_line2(request.json,el)
        if(len(el) > 0):
            return handle_errors(request.json,el)
        #3rd tier of checks
        #el = validate_line3(request.json,el)
        #if(len(el) > 0):
        #    handle_errors(request.json,el)
        #    abort(400)

        handle_success(request.json)
        return(jsonify( { 'status' : 'true' , 'message' : 'Order list change being processed automatically'} ), 201)

@app.route('/api/v1/itr_lookup', methods = ['GET'])
@auth.login_required
def lookup_name():
    #if len(task) == 0:
    #    abort(404)
    #if not request.json:
    #    abort(400)
    #if 'title' in request.json and type(request.json['title']) != str:
    #    abort(400)
    #if 'description' in request.json and type(request.json['description']) is not str:
    #    abort(400)
    #if 'done' in request.json and type(request.json['done']) is not bool:
    #    abort(400)
    return(jsonify( { 'status' : 'true' } ), 200)
if __name__ == '__main__':
    app.run(host='0.0.0.0',port=8080, debug = True)
