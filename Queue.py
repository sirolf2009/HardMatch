__author__ = 'gokhankacan'
import queue


queue = queue.Queue() # setup a queue
    for i in range(10):
        queue.add(pow, i, 2) # add Task()s to the queue

    for task in queue.finished: # itereate over the finished tasks
        print(task.result) # print the result


try:

except BaseException:
    print("hahahahaha")


"""
def worker():
    while True:
        item = q.get()
        do_work(item)
        q.task_done()

q = Queue()

for i in range(num_worker_threads):
    t = Thread(target=worker)
    t.deamon = True
    t.start()

for item in source():
    q.put(item)

q.join()

worker()"""