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


if __name__ == '__main__':
    traningset=get_data_from_arff('UPDOWN134_6_6.arff')
    testset=get_data_from_arff('AbudUpDown35_6_6.arff')
    # clf=MLPClassifier(max_iter=100000,batch_size=100,learning_rate='constant',solver='sgd', alpha=1e-5,hidden_layer_sizes=(38,),random_state=1,momentum=0.3,verbose=True)
    clf=MLPClassifier(hidden_layer_sizes=100,tol=0.00001,activation='logistic',max_iter=2000,learning_rate='constant',solver='lbfgs',momentum=0.3)
 #    clf = MLPClassifier(activation='tanh', solver='adam', learning_rate='constant',
 # alpha=1e-4, hidden_layer_sizes=(15,), random_state=1, batch_size=1,verbose= True,
 # max_iter=1, warm_start=True)
    F=traningset['UP']+traningset['DOWN']
    Y=[[1,0] for i in traningset['UP']]+[[0,1] for i in traningset['DOWN']]
    clf.learning_rate_init=0.15
    clf.fit(F,Y)
    print '[1,0]wrong #UP',
    upP=clf.predict(testset['UP'])
    print ( len (list((a for a in upP if not compareArray(a,[1,0])))))
    print (upP)

    print "[0,1]wrong #down",
    downP=clf.predict(testset['DOWN'])
    print ( len (list((a for a in downP if not compareArray(a,[0,1])))))
    print (downP)
