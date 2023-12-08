#encoding: utf8

# YOUR NAME: Diana Miranda
# YOUR NUMBER: 107457

# COLLEAGUES WITH WHOM YOU DISCUSSED THIS ASSIGNMENT (names, numbers):
# - ...
# - ...

from semantic_network import *
from constraintsearch import *

class MySN(SemanticNetwork):

    def __init__(self) :
        SemanticNetwork.__init__(self)
        # ADD CODE HERE IF NEEDED

    def query_local(self,user=None,e1=None,rel=None,e2=None):
        # IMPLEMENT HERE
        self.query_result = []
        for u, v in self.declarations.items():
            for (entity1, relation), entity2 in v.items():
                if (user is None or user == u) and (e1 is None or e1 == entity1) and (rel is None or rel == relation):
                    if isinstance(entity2, set):
                        for e in entity2:
                            if e2 is None or e2 == e:
                                if relation == 'subtype':
                                    self.query_result.append(Declaration(u, Subtype(entity1, e)))
                                elif relation == 'member':
                                    self.query_result.append(Declaration(u, Member(entity1, e)))
                                elif relation == 'association':
                                    self.query_result.append(Declaration(u, Association(entity1, relation, e)))
                                else:
                                    self.query_result.append(Declaration(u, AssocOne(entity1, relation, e)))
                    else:
                        if e2 is None or e2 == entity2:
                            if relation == 'subtype':
                                self.query_result.append(Declaration(u, Subtype(entity1, entity2)))
                            elif relation == 'member':
                                self.query_result.append(Declaration(u, Member(entity1, entity2)))
                            elif relation == 'association':
                                self.query_result.append(Declaration(u, Association(entity1, relation, entity2)))
                            else:
                                self.query_result.append(Declaration(u, AssocOne(entity1, relation, entity2)))
        return self.query_result

    def query(self,entity,assoc=None):
        # IMPLEMENT HERE

        pds = [
        self.query(entity2, assoc)
        for u, v in self.declarations.items()
        for (entity1, relation), entity2 in v.items()
        if relation in ['subtype', 'member'] and entity1 == entity
        ]

        pds_query = [d for sublist in pds for d in sublist]
        q = self.query_local(e1=entity, rel=assoc)
        
        lista = []
        for d in q:
            if d.relation.name == assoc:
                lista.append(d)

        return pds_query + lista

    def update_assoc_stats(self,assoc,user=None):
        # IMPLEMENT HERE
        pass


class MyCS(ConstraintSearch):

    def __init__(self,domains,constraints):
        ConstraintSearch.__init__(self,domains,constraints)
        # ADD CODE HERE IF NEEDED
        pass

    def search_all(self,domains=None,xpto=None):
        # If needed, you can use argument 'xpto'
        # to pass information to the function
        #
        # IMPLEMENTAR AQUI
        pass

