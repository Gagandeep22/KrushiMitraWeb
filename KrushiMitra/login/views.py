from django.shortcuts import render, redirect
from django.contrib import auth
import pyrebase

# Initialize Firebase
config = {
    'apiKey': "AIzaSyBGMF2M470QtGBAUx8_EyaD7v1NyTFSXbs",
    'authDomain': "krushimitra-efe8b.firebaseapp.com",
    'databaseURL': "https://krushimitra-efe8b.firebaseio.com",
    'projectId': "krushimitra-efe8b",
    'storageBucket': "krushimitra-efe8b.appspot.com",
    'messagingSenderId': "624448021426",
}

firebase = pyrebase.initialize_app(config)
authen = firebase.auth()
database = firebase.database()


# Create your views here.

def login(request):
    return render(request, 'login/login.html')


def postlogin(request):
    email = request.POST.get('email')
    password = request.POST.get('password')
    try:
        user = authen.sign_in_with_email_and_password(email, password)
    except:
        messg = 'Invalid Credentials'
        return render(request, 'login/login.html', {'mess': messg})
    request.session['uid'] = str(user['localId'])
    return redirect('login:admin')


def admin(request):
    if not request.session.get('uid'):
        return render(request, 'login/login.html')
    if database.child('unresolved').shallow().get().val() is None:
        farmers = False
        num = 0
    else:
        farmers = list(database.child('unresolved').shallow().get().val())
        farm = []
        for farmer in farmers:
            farm.append((farmer, database.child('Farmers').child(farmer).child('name').get().val(),  database.child('Farmers').child(farmer).child('address').get().val()))
        num = len(farmers)

    experts = list(database.child('expert').shallow().get().val())
    expert_details = []
    for expert in experts:
        expert_details.append((expert, database.child('expert').child(expert).child('name').get().val()))

    if not farmers:
        return render(request, 'login/admin.html', {'farmers': False, 'experts': expert_details, 'num': str(num)})

    main_message = []
    for farmer in farmers:
        print(farmer)
        queries = database.child('chats').child(farmer).get().val()

        messages = []
        for query in list(queries):
            if 'photoUrl' in queries[query]:
                messages.append((str(queries[query]['name']), str(queries[query]['photoUrl']), True))
            else:
                messages.append((str(queries[query]['name']), str(queries[query]['text']), False))
        main_message.append(messages)

    return render(request, 'login/admin.html', {'farmers': farm, 'main_message': zip(farmers, main_message), 'experts': expert_details, 'num': str(num)})


def logout(request):
    auth.logout(request)
    return render(request, 'login/login.html')


def expertassign(request):
    if not request.session.get('uid'):
        return render(request, 'login/login.html')
    farmerId = str(request.POST.get('farmerId'))
    if farmerId != 'No_Farmer':
        data = {farmerId[0:7]: farmerId}
        expertId = str(request.POST.get('expertSelected'))
        database.child('allocated').child(expertId).set(data)
        database.child('unresolved').child(farmerId).remove()
    return redirect('login:admin')


def addexpert(request):
    return render(request, 'login/user-profile.html')

def postaddexpert(request):
    if not request.session.get('uid'):
        return render(request, 'login/login.html')

    name = request.POST.get('name')
    email = request.POST.get('email')
    password = request.POST.get('pwd')
    try:
        user = authen.create_user_with_email_and_password(email,password)
    except:
        messg = 'Error!! Cannot create a user. Try again'
        return render(request, 'login/user-profile.html', {'messg': messg})

    uid = user['localId']
    data = {'name': name}
    database.child('expert').child(uid).set(data)

    return render(request, 'login/user-profile.html', {'messg': 'Expert account created!!'})

