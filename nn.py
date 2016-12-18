import arff
from sklearn.neural_network import MLPClassifier

def get_data_from_arff(path):
    data=arff.load(open(path,'rb'))
    classes= data['attributes'][0][1]
    da=data['data']
    result={}
    for ca in classes:
        result[ca]=(list(a for a in da if a[0]==ca))
        for x in result[ca]:
            del x[0]
    return result

def compareArray(arr1,arr2):
    for x ,i in enumerate(arr1):
        if arr1[i]!=arr2[i]:
            return False
    return True

params = [{'solver': 'sgd', 'learning_rate': 'constant', 'momentum': 0,
           'learning_rate_init': 0.2},
          {'solver': 'sgd', 'learning_rate': 'constant', 'momentum': .9,
           'nesterovs_momentum': False, 'learning_rate_init': 0.2},
          {'solver': 'sgd', 'learning_rate': 'constant', 'momentum': .9,
           'nesterovs_momentum': True, 'learning_rate_init': 0.2},
          {'solver': 'sgd', 'learning_rate': 'invscaling', 'momentum': 0,
           'learning_rate_init': 0.2},
          {'solver': 'sgd', 'learning_rate': 'invscaling', 'momentum': .9,
           'nesterovs_momentum': True, 'learning_rate_init': 0.2},
          {'solver': 'sgd', 'learning_rate': 'invscaling', 'momentum': .9,
           'nesterovs_momentum': False, 'learning_rate_init': 0.2},
          {'solver': 'adam', 'learning_rate_init': 0.01},
          {'solver':'sgd','learning_rate':'constant','learning_rate_init':0.01,'activation':'logistic' },
           {'solver':'sgd','learning_rate':'constant','learning_rate_init':0.3,'activation':'tanh' ,'momentum':0.2},  {'solver':'sgd','learning_rate':'constant','learning_rate_init':0.3,'activation':'identity' ,'momentum':0.2},
           {'solver': 'adam', 'learning_rate_init': 0.01,'activation':'identity'},
           {'solver': 'sgd', 'learning_rate_init': 0.01,'activation':'identity','momentum':0.9}
           ,{'solver': 'adam', 'learning_rate_init': 0.09,'activation':'identity','momentum':0.9},
           {'solver': 'adam', 'learning_rate_init': 0.01,'activation':'identity',"alpha":0.3},
             {'solver': 'adam', 'learning_rate_init': 0.01,'activation':'logistic',"alpha":0.3}
           ]

def test1():
    traningset=get_data_from_arff('UPDOWN134_6_6.arff')
    # testset=get_data_from_arff('testUPDOWN42_6_6.arff'),
    testset=get_data_from_arff('omarTest19_6_6.arff')
    clf=MLPClassifier(max_iter=100000,batch_size=100,learning_rate='constant',solver='sgd', alpha=1e-5,hidden_layer_sizes=(38,),random_state=1,momentum=0.3,verbose=True)
    clf=MLPClassifier(hidden_layer_sizes=100,tol=0.00001,activation='logistic',max_iter=2000,learning_rate='constant',solver='lbfgs',momentum=0.3)
 #    clf = MLPClassifier(activation='tanh', solver='adam', learning_rate='constant',
 # alpha=1e-4, hidden_layer_sizes=(15,), random_state=1, batch_size=1,verbose= True,
 # max_iter=1, warm_start=True)
    F=traningset['UP']+traningset['DOWN']
    Y=[[1,0] for i in traningset['UP']]+[[0,1] for i in traningset['DOWN']]
    # clf.learning_rate_init=0.15
    for i  in range(len( params)):
        clf=MLPClassifier(hidden_layer_sizes=(38,),random_state=0,max_iter=1000,**params[i])
        clf.fit(F,Y)
        print i
        print '[1,0]wrong #UP',
        upP=clf.predict(testset['UP'])
        print ( len (list((a for a in upP if not compareArray(a,[1,0])))))
        # print (upP)
        print "[0,1]wrong #down",
        downP=clf.predict(testset['DOWN'])
        print ( len (list((a for a in downP if not compareArray(a,[0,1])))))
        # print (downP)
clf1=MLPClassifier(warm_start=True,hidden_layer_sizes=(38,),random_state=0,max_iter=1000,**params[13])
clf2=MLPClassifier(warm_start=True,hidden_layer_sizes=(38,),random_state=0,max_iter=1000,**params[14])
def init():
    global clf1,clf2
    dataset=[
    "data_repo/arff/UPDOWN134_6_6.arff",
    # "data_repo/arff/50_6_6train.arff",
    # "data_repo/arff/AbudUpDown24_6_6.arff",
    # "data_repo/arff/AbudUpDown35_6_6.arff",
    # "data_repo/arff/UPDOWN22_6_6.arff",
    # "data_repo/arff/50_6_6train.arff",
    # "data_repo/arff/Omar46_6_6.arff",
    # "data_repo/arff/omarTest19_6_6.arff"
    ]

    for i in range(3):
        for data in dataset:
            traningset=get_data_from_arff(data)
            F=traningset['UP']+traningset['DOWN']
            Y=[[1,0] for i in traningset['UP']]+[[0,1] for i in traningset['DOWN']]
            clf1.fit(F,Y)
            clf2.fit(F,Y)
def classfiy1(array):
    global clf1
    result =clf1.predict(array)[0]
    if compareArray(result,[1,0]):
        return 'UP'
    elif compareArray(result,[0,1]):
        return 'down'
    else:
        return "i don't know"

def classfiy2(array):
    global clf2
    result =clf2.predict(array)[0]
    if compareArray(result,[1,0]):
        return 'UP'
    elif compareArray(result,[0,1]):
        return 'down'
    else:
        return "i don't know"

if __name__ == '__main__':
    init()
    x=[1.048,     0.853,     1.314,     0.958,     1.925,     3.667,     2.622,     1.380,     0.652,     0.259,     0.818,     1.221,     0.894,     1.125,     0.485,     0.150,     0.499,     0.705,     0.500,     0.537,     0.418,     0.484,     0.178,     0.078,     0.243,     0.122,     0.051,     0.075,     0.007,     0.078,     0.186,     0.068,     0.092,     0.037,     0.107,     0.031,     0.074,     0.070,     0.106,     0.126,     0.048,     0.082,     0.026,     0.127,     0.105,     0.177,     0.138,     0.026,     0.103,     0.074,     0.172,     0.104,     0.222,     0.180,     0.156,     0.117,     0.057,     0.077,     0.117,     0.064,     0.214,     0.060,     0.128,     0.025,     0.148,     0.096,     0.103,     0.020,     0.073,     0.026,     0.125,     0.086,     0.150,     0.129]
    print classfiy1([x])
    print classfiy2([x])
