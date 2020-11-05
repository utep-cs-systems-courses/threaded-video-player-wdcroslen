import threading

class PCQueue:#producer consumer queue
    def __init__(self):
        self.Q = []
        self.q_lock = threading.Lock()
        self.full = threading.Semaphore(0);
        self.emptyCell = threading.Semaphore(10);
    def put(self,item):
        self.emptyCell.acquire()
        self.q_lock.acquire()
        self.Q.append(item)
        self.q_lock.release()
        self.full.release() #There is at least one item to get
    def get(self):
        self.full.acquire()
        self.q_lock.acquire()
        if len(self.Q)==0:
            print("What the hell")
        item = self.Q.pop(0)
        self.q_lock.release()
        self.emptyCell.release() #there is at least one empty cell
        return item
