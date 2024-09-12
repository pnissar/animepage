import pandas as pd 
import numpy as np
import pickle
import sys
from flask import Flask, render_template, request, redirect, url_for, flash
from form import Search  

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

df = pd.read_csv('hianime1.csv')
new_df = pd.read_csv('animetag.csv')
sim = pickle.load(open('sim.pkl', 'rb'))
dict=pickle.load(open('dic.pkl','rb'))
pl=pickle.load(open('List.pkl','rb'))


# Home page 
@app.route('/', methods=['GET', 'POST'])
def index():
    form = Search()
    if form.validate_on_submit():
        entered_text = form.search.data
        return redirect(url_for('recommendlist', name=entered_text))
    return render_template('index.html', form=form)



# Recomendation Link
@app.route('/recommend/<name>')
def recommendlist(name):
    rec = recommend(name)
    if rec is None:
        flash(f"No anime found with the name '{name}'", 'danger')
        return redirect(url_for('index'))
    return render_template('Recomend.html', name=name, rec=rec,dict=dict,pl=pl)


# Recommendation function
def recommend(anime):
    ani_match = new_df[new_df['Name'].str.lower() == anime.lower()]
    if ani_match.empty: 
        print(f"No anime found with the name '{anime}'")
        return None
    
    ani_in = ani_match.index[0]
    dis = sim[ani_in]
    ani_list = sorted(list(enumerate(dis)), reverse=True, key=lambda x: x[1])[1:15]
    
    recommendations = []
    recommendations.append(ani_in)
    for i in ani_list:
        recommendations.append(i[0])
    
    return recommendations

if __name__ == '__main__':
    app.run(debug=True)
