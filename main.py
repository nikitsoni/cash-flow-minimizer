import time
from heapq import heappush, heappop

def time_decorator(func):
    def wrapper(*args, **kwargs):
        start_time = time.time()
        result = func(*args, **kwargs)
        end_time = time.time()
        print(f"Execution time: {end_time - start_time:.6f} seconds")
        return result
    return wrapper

class Cash_Flow_Minimizer:
    
    def __init__(self, cash_flow_graph) -> None:
        self.graph = cash_flow_graph
        self.amount = [0] * len(self.graph)
    
    def get_max(self, arr):
        return arr.index(max(arr))
    
    def get_min(self, arr):
        return arr.index(min(arr))
    
    def min_cash_flow_rec(self):
        max_credit = self.get_max(self.amount)
        max_debit = self.get_min(self.amount)
        
        # If all amounts are settled
        if self.amount[max_credit] == 0 and self.amount[max_debit] == 0:
            return
        
        # Find the minimum of max_debt and max_credit
        min_transfer = min(-self.amount[max_debit], self.amount[max_credit])
        self.amount[max_credit] -= min_transfer
        self.amount[max_debit] += min_transfer
        
        print(f"Person {max_debit} pays {min_transfer} to Person {max_credit}")
        
        self.min_cash_flow_rec()
    
    def calculate_net_amounts(self):
        for p in range(len(self.graph)):
            for i in range(len(self.graph)):
                self.amount[p] += self.graph[i][p] - self.graph[p][i]
    
    @time_decorator
    def min_cash_flow_greedy(self):
        
        # Array to store net amount to be credited/debited by each person.
        # Net Amount is calculated by subtracting all debts (amounts to pay) from all credits (amounts to be paid).
        self.calculate_net_amounts()
        
        # Recursively find the minimum of maxDebit and maxCredit, 
        # and update the net amount array by subtracting from the creditor and adding to the debtor.
        self.min_cash_flow_rec()
        print("Greedy Algorithm: ")
    
    @time_decorator
    def minimize_cash_flow_heap(self):
        
        # Array to store net amount to be credited/debited by each person.
        # Net Amount is calculated by subtracting all debts (amounts to pay) from all credits (amounts to be paid).
        self.calculate_net_amounts()
        
        # Heaps can help to efficiently get the maximum and minimum net amounts at each step.
        # Create max heap for credits and min heap for debits
        credit_heap = []
        debit_heap = []
        
        for i in range(len(self.amount)):
            if self.amount[i] > 0:
                heappush(credit_heap, (-self.amount[i], i))
            elif self.amount[i] < 0:
                heappush(debit_heap, (self.amount[i], i))
        
        while credit_heap and debit_heap:
            credit = heappop(credit_heap)
            debit = heappop(debit_heap)
            
            # Minimum of credit and debit
            transfer_amount = min(-credit[0], -debit[0])
            creditor = credit[1]
            debtor = debit[1]
            
            print(f"Person {debtor} pays {transfer_amount} to Person {creditor}")
            
            # Update heaps with remaining amounts
            new_credit_amount = -credit[0] - transfer_amount
            new_debit_amount = -debit[0] - transfer_amount
            
            if new_credit_amount > 0:
                heappush(credit_heap, (-new_credit_amount, creditor))
            if new_debit_amount > 0:
                heappush(debit_heap, (-new_debit_amount, debtor))
        print("Using Heap Data Structure:")


cash_flow_graph = [
    [0, 1000, 2000],
    [0, 0, 5000],
    [0, 0, 0]
]
cash_flow_graph = [
    [2, 63, 0, 85, 49],
    [0, 76, 0, 0, 27],
    [0, 0, 0, 17, 0],
    [73, 32, 50, 6, 71],
    [0, 86, 0, 0, 10]
]
app_instance = Cash_Flow_Minimizer(cash_flow_graph)
app_instance.min_cash_flow_greedy()
app_instance.minimize_cash_flow_heap()