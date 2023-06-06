import file_info
from werkzeug.serving import make_server
from flask import Flask, render_template, request, send_file

app = Flask(__name__)
SIZE_UNITS = ['Bytes','KB','MB','GB']

@app.route("/")
def index():
    file_data = file_info.get()
    if len(file_data)<=0:
        return render_template('nofile.html')
    return render_template('download.html',data=file_data)

@app.route('/get-file')
def get_file():
    return send_file(request.args.get('path'),as_attachment=True)

## API ##
def serve_file():   
    # app.run(debug=True,host='0.0.0.0',port=8080)
    server = make_server('0.0.0.0', 8080, app)
    server.serve_forever()