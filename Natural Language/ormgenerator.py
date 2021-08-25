class Generator():
    
    #Class defn contains fact types & entity vocab
    def __init__(self, fact_types=None, entity_vocab=None):
        self.fact_types = fact_types
        self.entity_vocab = entity_vocab
        self.unique_entities = self.get_unique_enities()
    
    #Pull the unique entities which are mentioned in UPPERCASE in the fact types
    def get_unique_enities(self):
        entities = []
        for i in self.fact_types:
            entities.append([j for j in i.split() if j.isupper()==True])
        unique_entities = list(np.unique([item for sublist in entities for item in sublist]))
        self.unique_entities = unique_entities
        return self.unique_entities
    
    #Random sampling with replacement (version 2 will have a different sampling method)
    def create_instance(self):
        vi = {k:np.random.choice(v) for k,v in self.entity_vocab.items()}
        return vi

    #Generate a single fact instance using fact types and entity vocab
    def generate_fact_instance(self):
        #generate an instance of the graph
        vi = create_instance(self.entity_vocab)
        fi = []
        di = []
        for fact_type in self.fact_types:
            #generating fact as natural language
            words = [str(i+' \''+vi.get(i)+'\'') 
                     if i in list(vi.keys()) else i for i in fact_type.split(' ')]
            generated_fact = ' '.join(words)
            fi.append(generated_fact)

            #generating dict version of the facts
            entities = [j for j in fact_type.split() if j.isupper()==True]
            dict_entities = {i:vi.get(i) for i in entities}
            di.append(dict_entities)
        return vi, fi, di
    
    #Calling generate_fact_instance function num times for multiple instances
    def generate_n_instances(self, num):
        vi_list = []
        fi_list = []
        di_list = []
        for i in range(num):
            vi, fi, di = self.generate_fact_instance()
            vi_list.append(vi)
            fi_list.append(fi)
            di_list.append(di)

        full_vi = vi_list
        full_fi = fi_list #np.array(fi_list).T.tolist()

        full_di = []
        new_di = np.array(di_list).T.tolist()
        for i in new_di:
            df = pd.DataFrame.from_dict(i)
            dd = df.to_dict(orient='list')
            full_di.append(dd)

        self.n_vi = full_vi
        self.n_fi = full_fi
        self.n_di = full_di
        #return self.n_vi, self.n_fi, self.n_di

        
    ##### HELPER Functions for manual user inputs
    def input_fact_types(self, n):
        inputs = []
        for i in range(n):
            print("-- Fact #(",i+1,'/',n,'):')
            inputs.append(input())
        self.fact_types = inputs
        self.unique_entities = self.get_unique_enities()
        
    def input_entity_vocab(self):
        vocab = {}
        for i in self.unique_entities:
            print('-- Entity:',i,'| input examples:')
            vocab[i] = [i.strip() for i in input().split(',')]
        self.entity_vocab = vocab
        

#instantiate and define
fact_types = ['The ACCOUNT_ID is associated with ACCOUNT_TYPE','The ACCOUNT_ID is associated with NAME','The ACCOUNT_ID is associated with AGE','The AGE belongs to CATEGORY','The ACCOUNT_TYPE belongs to COUNTRY']

entity_vocab = {'ACCOUNT_ID': ['1111', '2222', '3333', '4444', '5555', '6666', '7777', '8888'],'ACCOUNT_TYPE': ['Primary', 'Secondary'],'AGE': ['20', '21', '22', '23', '24', '25', '26', '27', '28', '29', '30'],'CATEGORY': ['Junior', 'Senior', 'Super Senior'],'COUNTRY': ['India', 'US', 'UK', 'Germany'],'NAME': ['Bill', 'Akshay', 'Sumit', 'Paritosh']}

a = Generator(fact_types, entity_vocab)

#generate instances
a.generate_n_instances(5)
print(a.n_vi)

