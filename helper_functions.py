def defensive_while(function, *args):
    
    stop_looping = False
    while not stop_looping:
        returns = function(*args)
        if isinstance(returns, list):
            if returns[0]== True:
                stop_looping = True
                if len(returns) > 1:
                    return (*returns[1:],)
                else:
                    return
                