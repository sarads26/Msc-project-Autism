from flask import Flask,render_template,request,json,jsonify,session,redirect,send_file,url_for,flash,Response
import os
from werkzeug.utils import secure_filename
import recommendation
#import video_input_recommendation
import base64

app=Flask(__name__)
app.secret_key="secure"
app.config['UPLOAD_FOLDER'] = str(os.getcwd())+'/static/uploads'

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif', "mp4"])
def allowed_file(filename):
	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

image_name = ""
image_filename = "app_image.jpg"

# @app.route('/img',methods=["post","get"])
# def first_page_img():
#     if request.method=="POST":
#         global image_name, image_filename

#         print("IMG POST received")

#         file = request.json

#         print(file)

#         file = file['body']['image']

#         imgdata = base64.b64decode(file)
#         image_name = app.config['UPLOAD_FOLDER']+"/"+image_filename
#         filename = image_name # I assume you have a way of picking unique filenames
#         with open(filename, 'wb') as f:
#             f.write(imgdata)

#         # file = request.files['file']
#         if filename == '':
#             flash('No image selected for uploading')
#             return redirect(request.url)

#         if file and allowed_file(filename):
#             print("Filename:", filename)
     
#             return "/mob_home"

#         else:
#             print('Allowed image types are -> png, jpg, jpeg, gif')
#             flash('Allowed image types are -> png, jpg, jpeg, gif')
#             return redirect(request.url)
#     else:
#         return "/mob_home"


# @app.route("/mob_questions",methods=["post","get"])
# def index2():
#     global image_name, image_filename
#     if request.method=="POST": 
        
#         A1 = request.form['A1']
#         A2 = request.form['A2']
#         A3 = request.form['A3']
#         A4 = request.form['A4']
#         A5 = request.form['A5']
#         A6 = request.form['A6']
#         A7 = request.form['A7']
#         A8 = request.form['A8']
#         A9 = request.form['A9']
#         A10 = request.form['A10']

#         result = recommendation.model_prediction(image_name,(A1,A2,A3,A4,A5,A6,A7,A8,A9,A10))
#         print("IMGNAME:", image_name)
#         return render_template("response.html", autism_detect=result, filename = image_filename )
        
#     else:
#         return render_template("form_page2.html", filename = image_name)

# @app.route("/mob_home")
# def mobile_home():
#     return render_template("mobile_home.html")

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/questions",methods=["post","get"])
def index():
    if request.method=="POST": 
        
        file = request.files['file']
        A1 = request.form['A1']
        A2 = request.form['A2']
        A3 = request.form['A3']
        A4 = request.form['A4']
        A5 = request.form['A5']
        A6 = request.form['A6']
        A7 = request.form['A7']
        A8 = request.form['A8']
        A9 = request.form['A9']
        A10 = request.form['A10']

        if file.filename == '':
            flash('No image selected for uploading')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            global saved_file_path
            saved_file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(saved_file_path)
            file_extension = saved_file_path[-3:]
            #if file_extension.lower()=="mp4" or file_extension.lower()=="gif":
                #result = video_input_recommendation.model_prediction(saved_file_path,(A1,A2,A3,A4,A5,A6,A7,A8,A9,A10))
            #else:
            result = recommendation.model_prediction(saved_file_path,(A1,A2,A3,A4,A5,A6,A7,A8,A9,A10))
            
            return render_template("response.html", autism_detect=result, filename = filename, file_extension = file_extension )
        else:
            flash('Allowed file types are -> png, jpg, jpeg, gif, mp4')
            return redirect(request.url)
        
    else:
        return render_template("form_page.html")

 
if "__main__" == __name__:
    app.run(debug=True, port=8080, host="0.0.0.0")