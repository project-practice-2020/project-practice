from flask import Flask, render_template, request
import pandas as pd
import numpy as np
import string


# Формирование и вывод датасета (из формы для опроса)

df = pd.read_csv('Qualities.csv')
df.columns = ['time', 'qualities', 'unions', 'age']
df = df.drop('time', axis=1)

df['qualities'] = df['qualities'].str.replace(', ', ';')
df['qualities'] = df['qualities'].str.replace(',', ';')
df['qualities'] = df['qualities'].str.lower()
df['unions'] = df['unions'].str.replace(', ', ';')
df['unions'] = df['unions'].str.replace(',', ';')
df['unions'] = df['unions'].str.strip(';')
df['unions'] = df['unions'].str.lower()


# Вывод датасета со всеми объединениями

uniset = pd.read_excel('uniset.xlsx')
uniset['Unions_lower'] = uniset['Unions'].str.lower()


# Объединение данных датасета со всеми объединениями и данных формы для опроса

for n in range(df.shape[0]):
    qualities = df['qualities'][n].split(';')
    age = df['age'][n]
    unions = df['unions'][n].split(';')

    for union in unions:
        inxs = uniset.index[(uniset['Unions_lower'].str.contains(union)) & (uniset['Age'] == age)]
        for inx in inxs:
            for quality in qualities:
                if quality in uniset.columns:
                    uniset.at[inx, quality] += 1
                else:
                    uniset.insert(uniset.shape[1], quality, 0)
                    uniset.at[inx, quality] = 1

uniset.iloc[:, 4:] = round(uniset.iloc[:, 4:].div(uniset.iloc[:, 4:].sum(axis=1),axis=0).multiply(100), 2)
uniset = uniset.fillna(0)


# ### Flask: WEB

app = Flask(__name__)


@app.context_processor
def utility_processor():
    def form_query(data, qualities, qualities_num, age):
	    if qualities_num == 1:
	        return data[(data.Age == age) & (
	            (data[qualities[0]] != 0)
	        )][['Unions', 'Link'] + qualities].reset_index(drop=True)
	    if qualities_num == 2:
	        return data[(data.Age == age) & (
	            (data[qualities[0]] != 0) |
	            (data[qualities[1]] != 0)
	        )][['Unions', 'Link'] + qualities].reset_index(drop=True)
	    if qualities_num == 3:
	        return data[(data.Age == age) & (
	            (data[qualities[0]] != 0) | 
	            (data[qualities[1]] != 0) | 
	            (data[qualities[2]] != 0)
	        )][['Unions', 'Link'] + qualities].reset_index(drop=True)
	    if qualities_num == 4:
	        return data[(data.Age == age) & (
	            (data[qualities[0]] != 0) | 
	            (data[qualities[1]] != 0) | 
	            (data[qualities[2]] != 0) |
	            (data[qualities[3]] != 0)
	        )][['Unions', 'Link'] + qualities].reset_index(drop=True)
	    if qualities_num == 5:
	        return data[(data.Age == age) & (
	            (data[qualities[0]] != 0) | 
	            (data[qualities[1]] != 0) | 
	            (data[qualities[2]] != 0) |
	            (data[qualities[3]] != 0) |
	            (data[qualities[4]] != 0)
	        )][['Unions', 'Link'] + qualities].reset_index(drop=True)
	    if qualities_num == 6:
	        return data[(data.Age == age) & (
	            (data[qualities[0]] != 0) | 
	            (data[qualities[1]] != 0) | 
	            (data[qualities[2]] != 0) |
	            (data[qualities[3]] != 0) |
	            (data[qualities[4]] != 0) |
	            (data[qualities[5]] != 0)
	        )][['Unions', 'Link'] + qualities].reset_index(drop=True)
	    if qualities_num == 7:
	        return data[(data.Age == age) & (
	            (data[qualities[0]] != 0) | 
	            (data[qualities[1]] != 0) | 
	            (data[qualities[2]] != 0) |
	            (data[qualities[3]] != 0) |
	            (data[qualities[4]] != 0) |
	            (data[qualities[5]] != 0) |
	            (data[qualities[6]] != 0)
	        )][['Unions', 'Link'] + qualities].reset_index(drop=True)
	    if qualities_num == 8:
	        return data[(data.Age == age) & (
	            (data[qualities[0]] != 0) | 
	            (data[qualities[1]] != 0) | 
	            (data[qualities[2]] != 0) |
	            (data[qualities[3]] != 0) |
	            (data[qualities[4]] != 0) |
	            (data[qualities[5]] != 0) |
	            (data[qualities[6]] != 0) |
	            (data[qualities[7]] != 0)
	        )][['Unions', 'Link'] + qualities].reset_index(drop=True)
	    if qualities_num == 9:
	        return data[(data.Age == age) & (
	            (data[qualities[0]] != 0) | 
	            (data[qualities[1]] != 0) | 
	            (data[qualities[2]] != 0) |
	            (data[qualities[3]] != 0) |
	            (data[qualities[4]] != 0) |
	            (data[qualities[5]] != 0) |
	            (data[qualities[6]] != 0) |
	            (data[qualities[7]] != 0) |
	            (data[qualities[8]] != 0)
	        )][['Unions', 'Link'] + qualities].reset_index(drop=True)
	    if qualities_num == 10:
	        return data[(data.Age == age) & (
	            (data[qualities[0]] != 0) | 
	            (data[qualities[1]] != 0) | 
	            (data[qualities[2]] != 0) |
	            (data[qualities[3]] != 0) |
	            (data[qualities[4]] != 0) |
	            (data[qualities[5]] != 0) |
	            (data[qualities[6]] != 0) |
	            (data[qualities[7]] != 0) |
	            (data[qualities[8]] != 0) |
	            (data[qualities[9]] != 0)
	        )][['Unions', 'Link'] + qualities].reset_index(drop=True)
    return dict(form_query=form_query)


@app.context_processor
def utility_processor():
	def form_result(data, qualities_num):
	    L = []
	    for zeros_num in range(qualities_num):
	        unions = []
	        for union in list(data.Unions):
	            if np.count_nonzero(data[data.Unions == union].values[0][1:] == 0) == zeros_num:
	                unions.append(union)
	        a = data[data.Unions.isin(unions)]
	        a['sum'] = a.sum(axis=1)
	        a = a.sort_values(by='sum', ascending=False)
	        L.append(a)
	    return pd.concat(L).reset_index(drop=True)
	return dict(form_result=form_result)


@app.context_processor
def utility_processor():
	def lower_qualities_names(q_names):
		for i in range(len(q_names)):
		    q_names[i] = q_names[i].lower()
		return q_names
	return dict(lower_qualities_names=lower_qualities_names)


@app.context_processor
def utility_processor():
	def remove_empty_strings(q_names):
		new = []
		for i in q_names:
			if i != '':
				new.append(i)
		return new
	return dict(remove_empty_strings=remove_empty_strings)


@app.context_processor
def utility_processor():
	def length(L):
		return len(L)
	return dict(length=length)


@app.route("/", methods=["GET", "POST"])
def choose():
    return render_template('unions_form.html', table=uniset)


@app.route("/recs", methods=["GET", "POST"])
def show():
    return render_template('actual_recommendations.html', table=uniset, 
    	age=request.form['age'],
    	q1=request.form['qual1'], 
    	q2=request.form['qual2'], 
    	q3=request.form['qual3'], 
    	q4=request.form['qual4'], 
    	q5=request.form['qual5'], 
    	q6=request.form['qual6'], 
    	q7=request.form['qual7'], 
    	q8=request.form['qual8'], 
    	q9=request.form['qual9'], 
    	q10=request.form['qual10']
    )


if __name__ == "__main__":
	app.run(host='127.0.0.1', port='8000', debug=True)
