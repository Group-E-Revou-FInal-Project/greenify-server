from enum import Enum

class Gender(Enum):
    MALE = 'male'
    FEMALE = 'female'
    
class OrderStatus(Enum):
    PENDING = 'pending'
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'
    
class TransactionStatus(Enum):
    CANCELLED = 'cancelled'
    COMPLETED = 'completed'