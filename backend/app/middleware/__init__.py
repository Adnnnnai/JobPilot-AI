"""Background Tasks - 异步任务执行"""


_background_tasks = []


def run_in_background(func, *args, **kwargs):
    """简易后台任务（后续可切换到 Celery）"""
    import threading
    t = threading.Thread(target=func, args=args, kwargs=kwargs, daemon=True)
    t.start()
    _background_tasks.append(t)
    return t
