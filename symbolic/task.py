from pyDatalog import pyDatalog 

class Character(pyDatalog.Mixin): # --> Employee inherits the pyDatalog capability

    def __init__(self, name, mother, father, house): 

        super(Character, self).__init__()

        self.name = name

        self.mother = mother
        self.father = father     

        self.house=house       

    def __repr__(self):

        return self.name

# read from file    
pyDatalog.load('got.csv')
pyDatalog.create_terms('X, Y, Z')
pyDatalog.create_terms('mother, father, house, sibling, cousin, uncle, aunt, grandparent, ancestor')
pyDatalog.create_terms('is_sibling, is_cousin, is_uncle, is_aunt, is_grandparent, is_ancestor')
is_sibling(X, Y) <= sibling(X, Y)
is_cousin(X, Y) <= cousin(X, Y)
is_uncle(X, Y) <= uncle(X, Y)
is_aunt(X, Y) <= aunt(X, Y)
is_grandparent(X, Y) <= grandparent(X, Y)
is_ancestor(X, Y) <= ancestor(X, Y)



