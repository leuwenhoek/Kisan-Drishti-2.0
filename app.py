from flask import Flask, render_template, request
import os
from werkzeug.utils import secure_filename
from myapi import get_plant_diagnosis

app = Flask(__name__)

# Configure upload folder
UPLOAD_FOLDER = os.path.join('static', 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif'}

# Ensure upload folder exists
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/kisan-bot', methods=['GET', 'POST'])
def kisan_bot():
    if request.method == 'POST':
        # Check if file and query are in the request
        if 'crop-image' not in request.files:
            return render_template('kisan_bot.html', diagnosis='Error: No image uploaded.')
        
        file = request.files['crop-image']
        query = request.form.get('query', '')

        if file.filename == '':
            return render_template('kisan_bot.html', diagnosis='Error: No file selected.')
        
        if file and allowed_file(file.filename):
            # Save the uploaded file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Get AI diagnosis
            diagnosis = get_plant_diagnosis(file_path, query)
            print(f"Diagnosis: {diagnosis}")  # Log for debugging
            
            # Set image_path for template
            image_path = os.path.join('uploads', filename)
            
            return render_template('kisan_bot.html', diagnosis=diagnosis, image_path=image_path)
        
        return render_template('kisan_bot.html', diagnosis='Error: Invalid file format. Please upload PNG, JPG, or GIF.')

    # GET request: Render the form
    return render_template('kisan_bot.html')

@app.route('/expert-desk')
def expert_desk():
    
    return render_template('expert.html')

@app.route('/history')
def history():
    return render_template('history.html')

@app.route('/team')
def about():
    return render_template('team.html')

if __name__ == "__main__":
    app.run(debug=True)