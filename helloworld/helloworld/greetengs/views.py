from django.shortcuts import  render

def hello_en(request):
    return render(request, 'hello.html',
                  {'message' : 'Hello, Word!'})
def hello_fr(request):
    return render(request, 'hello.html',
                  {'message': 'Bonjour, le Monde!'})
def hello_de(request):
    return render(request, 'hello.html',
                  {'message': 'Hallo, Welt!'})
def hello_es(request):
    return render(request, 'hello.html',
                  {'message': 'Hola, Mundo!'})