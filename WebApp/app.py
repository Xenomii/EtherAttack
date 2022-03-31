import glob
from flask import Flask, abort, render_template, send_file, flash, url_for
from flask import request, redirect
from werkzeug.utils import secure_filename
import os
import analyse

app = Flask(__name__)
app.config["FILE_UPLOADS"] = "TempStore"


@app.route('/')
def index():
    files = glob.glob('TempStore/*.sol', recursive=True)
    for f in files:
        try:
            os.remove(f)
        except OSError as e:
            print('Error %s : %s' % (f, e.strerror))
    return render_template("index.html")

@app.context_processor
def handle_context():
    return dict(os=os)

@app.route("/upload-file", methods=["GET", "POST"], defaults={'req_path': ''})
@app.route("/upload-file/<path:req_path>")
def upload_file(req_path):
    if request.method == "POST":
        if request.files:
            file = request.files["file"]
            filetype = file.filename.split('.')[-1]

            if filetype == 'sol':
                filename = secure_filename(file.filename)

                file.save(os.path.join(app.config["FILE_UPLOADS"], "temp_contract_file.sol"))
                file.save(os.path.join(app.config["FILE_UPLOADS"], file.filename))

                analyse.analyse(filename)

            elif file.filename == "":
                flash("No file selected!")

            else:
                flash("Only sol files are accepted!")

            return redirect(url_for('content', filename=filename))
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
    CONTRACT_DIR = "Contracts"
    abs_path = os.path.join(CONTRACT_DIR, filename[:size - 4])
    rm_path = os.path.join(abs_path, "msg_" + filename[:size-4] + ".txt")
    status = ""
    message = "No vulnerabilities detected or vulnerabilities does not fall under our approved attacks."

    c = open(f"Contracts/{filename[:size - 4]}/contract_{filename[:size - 4]}.sol"
             , 'r')
    d = open(f"Contracts/{filename[:size - 4]}/dependency_{filename[:size - 4]}.txt"
             , 'r')
    a = open(f"Contracts/{filename[:size - 4]}/analysis_{filename[:size - 4]}.txt"
             , 'r')
    s = open(f"Contracts/{filename[:size - 4]}/summary_{filename[:size - 4]}.txt"
             , 'r')
    f = open(f"Contracts/{filename[:size - 4]}/functionsummary_{filename[:size - 4]}.txt"
             , 'r')

    for file in os.listdir(abs_path):
        try:
            attack = open(f"Contracts/{filename[:size - 4]}/attack_{filename[:size - 4]}.sol"
                          , 'r')
            if file.startswith("attack"):
                status = attack.read()
                break

            elif not file.startswith("attack"):
                continue

            else:
                attack.close()

        except FileNotFoundError:
            attack = open(f"Contracts/{filename[:size - 4]}/msg_{filename[:size - 4]}.txt"
                          , 'w+')
            attack.write(message)

            attack = open(f"Contracts/{filename[:size - 4]}/msg_{filename[:size - 4]}.txt"
                          , 'r')
            status = attack.read()

            os.remove(rm_path)
            continue

    return render_template('content.html', original=c.read(), dependency=d.read(), analysis=a.read(),
                           summary1=s.read(), function=f.read(), attack=status, filename=filename, abs_path=abs_path)

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
    elif (type == "attack"):
        path = f"Contracts/{filename[:size - 4]}/attack_{filename[:size - 4]}.sol"
    else:
        path = f"Contracts/{filename[:size - 4]}/functionsummary_{filename[:size - 4]}.txt"

    return send_file(path, as_attachment=True)

if __name__ == '__main__':
    app.secret_key = b'_5#y2L"F4Z8z\n\xec]/'
    app.run(debug=True)