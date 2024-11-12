class Posting:
    #Make sure data is always in format (doc_id, f_count, positions, fields, priority)

    #Tokens need to have prio dependant on where in the html it is found (aka: <b> <title> etc)
    def __init__(self):
        self._list = []

    def __repr__(self):
        return f"Posting({self._list})"

    def insert(self, doc_id, f_count, positions=None, fields=None, priority=0):
        data = (doc_id, f_count, positions, fields, priority)
        self._list.append(data)
