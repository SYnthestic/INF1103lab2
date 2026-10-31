from abc import ABC, abstractmethod


class CanBeShipped(ABC):
    @abstractmethod
    def calculate_shipping_cost():
        '''Implementing classes must find a way to calculate shipping costs'''
        #This does the interface