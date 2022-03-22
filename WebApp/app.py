from flask import Flask, abort, render_template, send_file, flash
from flask import request, redirect
from werkzeug.utils import secure_filename
import os
import analyse

app = Flask(__name__)
app.config["FILE_UPLOADS"] = "TempStore"
@app.route('/')
def index():
    return render_template("index.html")

@app.route('/dashboard')
def dashboard():
    return render_template("dashboard.html")

@app.route("/upload-file", methods=["GET", "POST"], defaults={'req_path': ''})
@app.route("/upload-file/<path:req_path>")
def upload_file(req_path):

    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            filetype = file.filename.split('.')[-1]

            if filetype == 'sol':
                filename = secure_filename(file.filename)
                print(filename)
                file.save(os.path.join(app.config["FILE_UPLOADS"], "temp_contract_file.sol"))
                file.save(os.path.join(app.config["FILE_UPLOADS"], file.filename))
                print("File saved")
                analyse.analyse(filename)
            elif file.filename == "":
    
                
                    flash("No file selected!")
            else:
                    flash("Only sol files are accepted!")
                  
            

           

    

            return redirect(request.url)
    else:
        BASE_DIR = 'TempStore'

        # Joining the base and the requested path
        abs_path = os.path.join(BASE_DIR, req_path)

        # Return 404 if path doesn't exist
        if not os.path.exists(abs_path):
            return abort(404)

        # Check if path is a file and serve
        if os.path.isfile(abs_path):
            return send_file(abs_path)

        # Show directory contents
        files = os.listdir(abs_path)

    return render_template("upload_file.html", files=files)


@app.route('/content.html/<filename>') 
def content(filename): 
    size = len(filename)
    print(filename)
    c=open(f"Contracts/{filename[:size - 4]}/contract_{filename[:size - 4]}.sol"
    , 'r')
    d=open(f"Contracts/{filename[:size - 4]}/dependency_{filename[:size - 4]}.txt"
    , 'r') 
    a=open(f"Contracts/{filename[:size - 4]}/analysis_{filename[:size - 4]}.txt"
    , 'r') 
    s=open(f"Contracts/{filename[:size - 4]}/summary_{filename[:size - 4]}.txt"
    , 'r') 
    f=open(f"Contracts/{filename[:size - 4]}/functionsummary_{filename[:size - 4]}.txt"
    , 'r') 
    return render_template('content.html', original=c.read(),dependency=d.read(),analysis=a.read(),summary1=s.read(),function=f.read(),filename=filename) 


@app.route('/download', methods=['GET', 'POST'])
def download():
    # Appending app path to upload folder path within app root folder
    filename = request.args.get('filename')
    type = request.args.get('type')

    size = len(filename)
    path = ""

    if (type == "analysis"):
        path = f"Contracts/{filename[:size - 4]}/analysis_{filename[:size - 4]}.txt"
    elif (type == "dependency"):
        path = f"Contracts/{filename[:size - 4]}/dependency_{filename[:size - 4]}.txt"
    elif (type == "summary"):
        path = f"Contracts/{filename[:size - 4]}/summary_{filename[:size - 4]}.txt"
    else:
        path = f"Contracts/{filename[:size - 4]}/functionsummary_{filename[:size - 4]}.txt"

    return send_file(path, as_attachment=True)


   

if __name__ == '__main__':
    app.secret_key = b'_5#y2L"F4Z8z\n\xec]/'
    app.run(debug=True)
