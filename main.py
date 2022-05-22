from flask import Flask
from flask_restful import Resource,Api

app=Flask(__name__)
api=Api(app)

import pandas as pd
df = pd.read_csv("ins.csv")
    # To fit data in standardization we need to encode string data into integer or flot so we map
df['gender'] = df['gender'].map({'male': 1, 'female': 0})
df['smoker'] = df['smoker'].map({'yes': 1, 'no': 0})
df['region'] = df['region'].map({'southeast': 1, 'southwest': 2, 'northeast': 3, 'northwest': 4})

    ##seperate input output

x = df.drop(columns="charges")
y = df.charges

from sklearn.ensemble import GradientBoostingRegressor
gr = GradientBoostingRegressor()
gr.fit(x.values, y.values)


class Insurance(Resource):
    def get(self,age,gen,bmii,child,smoke,reg):

        return float(gr.predict([[age,gen,bmii,child,smoke,reg]]))

api.add_resource(Insurance,'/insurance/<int:age>/<int:gen>/<int:bmii>/<int:child>/<int:smoke>/<int:reg>')
app.run()