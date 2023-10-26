from threading import Thread


class ThreadWithReturnValue(Thread):
    _target = None
    _return = None
    _args = ()
    _kwargs = {}

    def run(self):
        if self._target is not None:
            self._return = self._target(*self._args, **self._kwargs)

    def join_(self):
        super().join()
        return self._return
