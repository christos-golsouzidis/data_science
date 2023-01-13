import time
import numpy as np
import os

tm0 = np.array([[1.00000000e+00, 0.00000000e+00, 0.00000000e+00, 0.00000000e+00,
        0.00000000e+00],
       [3.90040607e-01, 1.28232528e-03, 2.22697158e-01, 1.90425305e-01,
        1.95554606e-01],
       [5.36747759e-01, 2.71446863e-02, 0.00000000e+00, 2.19206146e-01,
        2.16901408e-01],
       [4.98828583e-01, 2.37992971e-01, 1.36860601e-01, 5.85708708e-04,
        1.25732136e-01],
       [2.50932339e-01, 3.23654768e-01, 2.72775706e-01, 1.52370804e-01,
        2.66382525e-04]])

all_states = ['checkout','dairy','drinks','fruits','spices']


class Customer:

    def __init__(self, id, state):#, active):
        self.id = id
        self.state = state
        self.status = 'new'
        
    def next_state(self, trans_matrix):
        self.state = np.random.choice(all_states, p=trans_matrix[all_states.index(self.state)])
        return self.state


class Supermarkt:

    def __init__(self):
        self.customerlist = []

    def add_customer(self, id):
        c = Customer(id, np.random.choice(all_states[1:]))
        self.customerlist.append(c)

    def rm_customer(self, obj):
        self.customerlist.remove(obj)
        del obj


def addCustomers(cid, supermarket):
    for n in range(int(np.random.normal(1,1))):
        supermarket.add_customer(cid)
        cid += 1
    return cid

def rmCustomers(supermarket):
    for n in supermarket.customerlist:
        if n.status == 'out':
            supermarket.rm_customer(n)


def draw(id,state):
    if state == 'checkout':
        print(f'\t{id}')
    elif state == 'dairy':
        print(f'\t\t{id}')
    elif state == 'drinks':
        print(f'\t\t\t{id}')
    elif state == 'fruits':
        print(f'\t\t\t\t{id}')
    elif state == 'spices':
        print(f'\t\t\t\t\t{id}')
        



doodl = Supermarkt()
custid = 0
while True:
    os.system('cls')
    print('\tchkout\tdairy\tdrinks\tfruits\tspices')
    
    rmCustomers(doodl)
    custid = addCustomers(custid, doodl)
    
    for obj in doodl.customerlist:
        if obj.status == 'out':
            continue
        if obj.status == 'new':
            draw(obj.id , obj.state)
            obj.status = 'cur'
            continue
        obj.next_state(tm0)
        if obj.state == 'checkout':
            obj.status = 'out'
        draw(obj.id , obj.state)

    pass
    time.sleep(1)

