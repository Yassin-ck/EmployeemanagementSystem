from django.shortcuts import redirect


def unauthenticated_user(view_func):
    def wrapper(request, *args, **kwargs):
        if  hasattr(request.user, 'last_login') and request.user.is_authenticated:
            return redirect('home')
        elif request.user.is_authenticated:    
            return view_func(request, *args, **kwargs)
        else:
            return view_func(request, *args, **kwargs)
 
    return wrapper





def allowed_users(allowed_roles=[]):
    def decorators(view_func):
        def wrappers(request,*args,**kwargs):
            
            group = None
            if request.user.groups.exists():
                group = request.user.groups.all()[0].name
            
            if group in allowed_roles:
                return view_func( request,*args,**kwargs)
            else:
                return redirect('home')
                     
        return wrappers
    return decorators





def dashboard_authentication(view_func):
    def wrapper(request, *args, **kwargs):
        if request.user.is_authenticated:
            print('decorator')
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')
    return wrapper
