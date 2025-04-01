from flask import Flask, render_template, request, jsonify, make_response
import json
import random
import pandas as pd
from faker import Faker

app = Flask(__name__)
fake = Faker('id_ID')

# Load datasets
global_names = pd.read_csv('data/global_names.csv').to_dict('records')
local_names = pd.read_csv('data/local_names.csv').to_dict('records')
with open('data/categories.json') as f:
    categories = json.load(f)
    category_names = [cat['name'] for cat in categories]

def generate_name(name_type):
    if name_type == 'global':
        name = random.choice(global_names)
        return f"{name['first_name']} {name['last_name']}"
    else:
        name = random.choice(local_names)
        return f"{name['first_name']} {name['last_name']}"

def generate_user(user_id, name_type):
    name = generate_name(name_type)
    username = f"{name.split()[0].lower()}{user_id}"
    email = f"{username}@example.com"
    
    return {
        "id": user_id,
        "name": name,
        "username": username,
        "email": email,
        "password": "password123",
        "avatar": f"/images/avatar{user_id}.png",
        "nomorhp": fake.phone_number()[:12],
        "alamat": fake.street_address() + ", " + fake.city(),
        "preferences": random.sample(category_names, k=random.randint(1,3)),
        "purchase_history": [random.randint(100, 200) for _ in range(3)]
    }

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/generate', methods=['POST'])
def generate():
    name_type = request.form.get('name_type', 'lokal')
    jumlah = int(request.form.get('jumlah', 5))
    
    data = [generate_user(i+1, name_type) for i in range(jumlah)]
    json_data = json.dumps(data, indent=2, ensure_ascii=False)
    
    return render_template('result.html', 
        json_data=json_data,
        name_type=name_type,
        jumlah=jumlah
    )

if __name__ == '__main__':
    app.run(debug=True)