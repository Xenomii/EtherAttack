from flask import Flask, abort, render_template, send_file
from flask import request, redirect
import os

app = Flask(__name__)
app.config["FILE_UPLOADS"] = "uploaded_files"

@app.route('/')
def hello_world():  # put application's code here
    return render_template("index.html")


@app.route("/upload-file", methods=["GET", "POST"], defaults={'req_path': ''})
@app.route("/upload-file/<path:req_path>")
def upload_file(req_path):

    if request.method == "POST":
        if request.files:
            file = request.files["file"]

            filetype = file.filename.split('.')[-1]

            if filetype == 'sol':
                file.save(os.path.join(app.config["FILE_UPLOADS"], file.filename))
                print("File saved")
            
            return redirect(request.url)
    else:
        BASE_DIR = 'uploaded_files'

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


if __name__ == '__main__':
    app.run()
