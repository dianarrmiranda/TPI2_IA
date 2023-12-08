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
        self.assoc_stats = {}

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
            if relation in ['subtype', 'member', 'association'] and entity1 == entity
        ]

        pds_query = [d for sublist in pds for d in sublist]
        q = self.query_local(e1=entity, rel=assoc)
        
        lista = []
        for d in q:
            if d.relation.name == assoc:
                lista.append(d)

        return pds_query + lista

    def update_assoc_stats(self,assoc,user=None):

        stats_assoc_e1 = []
        stats_assoc_e2 = []


        q = self.query_local(user=user, rel=assoc)

        qmember = self.query_local(user=user, rel='member')


        N = len(q)
        K = 0
        for d in q:
            for d2 in qmember:
                if d.relation.entity1 == d2.relation.entity1:
                    if d2.relation.entity2 not in stats_assoc_e1:
                        stats_assoc_e1.append(d2.relation.entity2)
                        for s in self.predecessor_path(user, d2.relation.entity2):
                            if s not in stats_assoc_e1:
                                stats_assoc_e1.append(s)
                
                if d.relation.entity2 == d2.relation.entity1:
                    if d2.relation.entity2 not in stats_assoc_e2:
                        stats_assoc_e2.append(d2.relation.entity2)
                        for s in self.predecessor_path(user, d2.relation.entity2):
                            if s not in stats_assoc_e2:
                                stats_assoc_e2.append(s)

                if len(self.query_local(user=d2.user, e1=d.relation.entity1)) == 0:
                    K += 1
                                
        k1 = {}
        for x in stats_assoc_e1:
            count = 0
            for decl in q:
                for s in self.query_local(user=user, e1=decl.relation.entity1):
                    if s.relation.entity2 == x:
                        count += 1

            for p in self.predecessor_path(user, x):
                if p not in k1:
                    k1[p] = 0
                k1[p] = k1[p] + count
            

        k1 = {k: v / (N-K+K**2)  for k, v in k1.items()}
            

        k2 = {}
        for x in stats_assoc_e2:
            count = 0
            for decl in q:
                for s in self.query_local(user=user, e1=decl.relation.entity2):
                    if s.relation.entity2 == x:
                        count += 1

            for p in self.predecessor_path(user, x):
                if p not in k2:
                    k2[p] = 0
                k2[p] = k2[p] + count
        
        k2 = {k: v / (N-K+K**2) for k, v in k2.items()}

        self.assoc_stats[(assoc, user)] = (k1, k2)
    
    def predecessor_path(self,user, c):
            decl = self.query_local(user=user, e1=c, rel='subtype')
            if len(decl) == 0:
                return [c]
            for d in decl:
                if res:= self.predecessor_path(user, d.relation.entity2):
                    return res + [c]


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
        if domains==None:
            domains = self.domains

        if any([lv==[] for lv in domains.values()]):
            return None

        if all([len(lv)==1 for lv in list(domains.values())]):
            return [{ v:lv[0] for (v,lv) in domains.items() }]
       
        for var in domains.keys():
            if len(domains[var])>1:
                solutions = []
                for val in domains[var]:
                    newdomains = dict(domains)
                    newdomains[var] = [val]
                    newdomains = self.propagate_constraints(newdomains, var, val)
                    solution = self.search_all(newdomains)
                    if solution is not None and solution not in solutions:
                        solutions += solution
                return solutions
        return None



