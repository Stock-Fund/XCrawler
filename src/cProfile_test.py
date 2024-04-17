import cProfile, pstats, io

def cProfile_test(func,*args,**kwargs): 
    pr = cProfile.Profile()
    pr.enable()
    func(*args,**kwargs)
    pr.dump_stats("pipeline.prof")
    pr.disable()
    s = io.StringIO()
    sortby = "cumtime"  # 仅适用于 3.6, 3.7 把这里改成常量了
    ps = pstats.Stats(pr, stream=s).sort_stats(sortby)
    ps.print_stats()
    print(s.getvalue())