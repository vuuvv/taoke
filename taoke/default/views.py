from vuuvv.utils.decorators import template

@template
def index(request):
    return {"msg": "Hello World"}
