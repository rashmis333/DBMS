from django.shortcuts import render
from django.http import HttpResponse
from django.http import HttpRequest
from . import auto2,cars
import json
import re

def hi(request):
    return render(request,'frontend/first.html')
# Create your views here.

def output(request):
    url_list = request.GET.get('urls_list', '')
    InputList = request.GET.get('InputList', '').split(',')
    InputList = [ele for ele in InputList if ele.strip()]
    context = {}

    if url_list == 'autotrader':
        #if len(request.GET.get('whereClause', '').split(',')) > 0:
        #if len(request.GET.get('whereClause', '').split('AND'))>0 and 'zip' in request.GET.get('whereClause', ''):
        if 'zip' in request.GET.get('whereClause', ''):
            search_keywords = re.split('AND| AND | AND| and |and | and|OR | OR| OR |or | or| or ',request.GET.get('whereClause', ''))
            test_dup =list(re.split(r"<=|>=|[=><]",r.strip())[0] for r in search_keywords)
            dup_val= list(map(lambda x: x[1] + str(test_dup[:x[0]].count(x[1]) + 1) if test_dup.count(x[1]) > 1 else x[1],enumerate(test_dup)))
            val_list = list(re.split(r"<=|>=|[=><]",k.strip())[1] for k in search_keywords)

            Inputdictionary = dict(zip(dup_val, val_list))

            #Inputdictionary = dict(re.split(r"<=|>=|[=><]",k.strip()) for k in search_keywords)
            bool_check =[]
            for z in search_keywords:
                if '>' in z or '<' in z or '>=' in z or '<=' in z:
                    bool_check.append(z)
            x = auto2.parse_auto(Inputdictionary,bool_check)

            final_list =[]
            final_dict= {}

            if len(InputList) <3:
                for j,i in enumerate(InputList):
                    i = i.lstrip()
                    if i == InputList[-1].lstrip() and len(InputList)>1:
                        print("break")
                        break
                    else:
                        print(i)
                        index = 0
                        if len(InputList)==1:
                            while index < len(x):
                                final_dict= {i: x[index][i]}
                                final_list.append(final_dict)
                                index = index +1
                        else:
                            while index < len(x):
                                final_dict= {i: x[index][i],InputList[j+1].lstrip():x[index][InputList[j+1].lstrip()]}
                                final_list.append(final_dict)
                                index = index +1

                            print('inside loop', final_list)
                context['auto_data'] = final_list
            else:
                context['auto_data'] = x
            return render(request, 'frontend/output.html', context)
        else:
            context['auto_data'] = 'For Autotrader, zipcode is mandatory!!!'
            return render(request, 'frontend/output.html', context)
    elif url_list == 'cars':
        if 'zip' in request.GET.get('whereClause', ''):
            search_keywords = re.split('AND| AND | AND| and |and | and|OR | OR| OR |or | or| or ',
                                       request.GET.get('whereClause', ''))
            test_dup = list(re.split(r"<=|>=|[=><]", r.strip())[0] for r in search_keywords)
            dup_val = list(
                map(lambda x: x[1] + str(test_dup[:x[0]].count(x[1]) + 1) if test_dup.count(x[1]) > 1 else x[1],
                    enumerate(test_dup)))
            val_list = list(re.split(r"<=|>=|[=><]", k.strip())[1] for k in search_keywords)

            Inputdictionary = dict(zip(dup_val, val_list))

            # Inputdictionary = dict(re.split(r"<=|>=|[=><]",k.strip()) for k in search_keywords)
            bool_check = []
            for z in search_keywords:
                if '>' in z or '<' in z or '>=' in z or '<=' in z:
                    bool_check.append(z)

            x = cars.parse_cars(Inputdictionary, bool_check)
            context = {'x': x}

        return render(request,'frontend/output.html',context)
    else:
        return render(request, 'frontend/output.html',context)

#def url_list(request):
#    message = request.GET.get('urls_list', '')
#    print(message)
    #return render(request,'frontend/url_list.html')