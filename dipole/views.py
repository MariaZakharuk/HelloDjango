from django.shortcuts import render
from django.core.serializers import serialize
import pandas as pd
import json
from django.forms.models import modelform_factory
import numpy as np
import math
from dipole.forms import PointForm
import statsmodels.api as sm
from statsmodels.tsa.api import VAR
from .models import point
from django.http import HttpResponse


# Create your views here.
def dipole (request):
    coefficient_df = pd.read_json('data.json')
	# coefficient_df = coefficient_df.transpose()
    #print('coefficient_df=', coefficient_df)
    fin_df = pd.DataFrame()
    
    for row, field in coefficient_df.iteritems():
        year = coefficient_df[row][0]
        g10 = coefficient_df[row][1]
        g11 = coefficient_df[row][2]
        h11 = coefficient_df[row][3]

        zn = math.sqrt((g11*g11) + (h11*h11))

        tg_x = g10/zn
        tg_y = h11/g11

        x = math.atan(tg_x)
        y = math.atan(tg_y)

        x = math.degrees(x)
        y = math.degrees(y)
        # print(x)
        #fin_df = fin_df.append(pd.DataFrame({'Year':year, 'X':x, 'Y':y},  index=[i]))
        
        if (point.objects.filter(x=x, y=y)):
            pass
        else:
            point.objects.create(name=str(int(year)), x=x, y=y)


  #  print(fin_df)

    # coefficient_df = coefficient_df.transpose()
	# for row, field in MOList_df.iteritems():
	# 	g10 = coefficient_df[row].
	# 	g11 = coefficient_df[2]
	# 	h11 = coefficient_df[3]
# 	print(g10)
# 	print(coefficient_df)

   # fin_df = pd.read_json('../dipole/templates/fin_df.json')
    points = point.objects.all()
    i=0
    for marker in points:
        fin_df = fin_df.append(pd.DataFrame({'Year':int(marker.name), 'X':marker.x, 'Y':marker.y},  index=[i]))
        i+=1
    print(fin_df)
    model = VAR(fin_df)
    model_fit = model.fit()
    pred = model_fit.forecast(model_fit.y, steps=3)
    
    i = len(fin_df)
    for row in pred:    
        print(row)
        fin_df = fin_df.append(pd.DataFrame({'Year':int(round(row[0])), 'X':row[1], 'Y':row[2]}, index=[i]))
        i+=1

    fin_df.to_json('../dipole/templates/fin_df.json')

    return render(request,'dipole/dipole.html', {})#'fin_df':fin_df})
    

#fin_df = pd.DataFrame()

    
def fin_df (request):
    return render(request,'fin_df.json',{})

def icon(request):
    with open('../dipole/templates/dipole/icon.png', 'rb') as f:
        return HttpResponse(f.read(), content_type='image/png')
    