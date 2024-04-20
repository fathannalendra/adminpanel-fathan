from ntpath import join
import os
from posixpath import dirname
from flask import Flask, redirect, url_for, render_template, request
from pymongo import MongoClient
from bson import ObjectId
from werkzeug.utils import secure_filename

MONGODB_URL = os.environ.get("MONGODB_URL")
DB_NAME =  os.environ.get("DB_NAME")

client = MongoClient('mongodb+srv://fathannalendra:nalendra1@cluster0.zewp6nd.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0')
db = client.dbfruits

import os

app = Flask(__name__)

@app.route('/', methods=["GET", "POST"])
def home():
    fruit = list(db.fruits.find({}))
    return render_template('dashboard.html', fruit=fruit)

@app.route('/fruit', methods=["GET"])
def fruit():
    fruit = list(db.fruits.find({}))
    return render_template('fruit.html', fruit=fruit)

@app.route('/addFruit', methods=["GET", "POST"])
def addFruit():
    if request.method == 'POST':
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        gambar = request.files['image']
        
        if gambar:
            nama_file_asli = gambar.filename
            nama_file_gambar = secure_filename(nama_file_asli)
            file_path = f'./static/assets/imgFruit/{nama_file_gambar}'
            gambar.save(file_path)
        else:
            nama_file_gambar = None
            
        doc = {
            'nama': nama,
            'harga': harga,
            'gambar': nama_file_gambar,
            'deskripsi': deskripsi
        }
        
        db.fruits.insert_one(doc)
        return redirect(url_for("fruit"))
        
    return render_template('AddFruit.html')



@app.route('/editFruit/<string:_id>', methods=["GET", "POST"])
def editFruit(_id):
    if request.method == 'POST':
        nama = request.form['nama']
        harga = request.form['harga']
        deskripsi = request.form['deskripsi']
        gambar = request.files['image']
        
        doc = {
            'nama': nama,
            'harga': harga,
            'deskripsi': deskripsi  
        }
        if gambar:
            nama_file_asli = gambar.filename
            nama_file_gambar = secure_filename(nama_file_asli)
            file_path = f'./static/assets/imgFruit/{nama_file_gambar}'
            gambar.save(file_path)
            doc['gambar'] = nama_file_gambar
        
        db.fruits.update_one({'_id': ObjectId(_id)}, {'$set': doc})
        return redirect(url_for('fruit'))
    
    data = db.fruits.find_one({'_id': ObjectId(_id)})
    return render_template('EditFruit.html', data=data)


@app.route('/deleteFruit/<string:_id>', methods=["GET", "POST"])
def deleteFruit(_id):
    db.fruits.delete_one({'_id': ObjectId(_id)})
    return redirect(url_for('fruit'))


if __name__ == '__main__':
    app.run('0.0.0.0', port=5000, debug=True)