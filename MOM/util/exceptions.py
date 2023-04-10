class DuplicatedQueueException(Exception):
    # Raised when trying to create a Queue that already exists
    pass

class DuplicatedUserException(Exception):
    #Raised when trying to create a User that already exists
    pass

class QueueIsNotEmptyException(Exception):
    #Raised when trying to delete a Queue that is not empty
    pass
