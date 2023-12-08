
class ConstraintSearch:

    # domains é um dicionário com o domínio de cada variável;
    # constaints e' um dicionário com a restrição aplicável a cada aresta;
    def __init__(self,domains,constraints):
        self.domains = domains
        self.constraints = constraints
        self.calls = 0

    # domains é um dicionário com os domínios actuais
    # de cada variável
    # ( ver acetato "Pesquisa com propagacao de restricoes
    #   em problemas de atribuicao - algoritmo" )
    def search(self,domains=None):
        self.calls += 1 
        
        if domains==None:
            domains = self.domains

        # se alguma variavel tiver lista de valores vazia, falha
        if any([lv==[] for lv in domains.values()]):
            return None

        # se nenhuma variavel tiver mais do que um valor possivel, sucesso
        if all([len(lv)==1 for lv in list(domains.values())]):
            # se valores violam restricoes, falha
            # ( verificacao desnecessaria se for feita a propagacao
            #   de restricoes )
            for (var1,var2) in self.constraints:
                constraint = self.constraints[var1,var2]
                if not constraint(var1,domains[var1][0],var2,domains[var2][0]):
                    return None 
            return { v:lv[0] for (v,lv) in domains.items() }
       
        # continuação da pesquisa
        # ( falta fazer a propagacao de restricoes )
        for var in domains.keys():
            if len(domains[var])>1:
                for val in domains[var]:
                    newdomains = dict(domains)
                    newdomains[var] = [val]
                    newdomains = self.propagate_constraints(newdomains, var, val)
                    solution = self.search(newdomains)
                    if solution != None:
                        return solution
        return None
    
    def propagate_constraints(self, domains, var, val):
        edges = [(v1,v2) for (v1,v2) in self.constraints if v2==var]
        while edges:
            var1, var2 = edges.pop(0)
            constraint = self.constraints[var1, var2]
            domain = [x for x in domains[var1] if any(constraint(var1, x, var2, y) for y in domains[var2])]

            if len(domain) < len(domains[var1]):
                domains[var1] = domain
                edges.extend((v1, v2) for (v1, v2) in self.constraints if v2 == var1)

        return domains
            
