import nltk
import json
from nltk.corpus import wordnet
synonymALL, value = [], []

array_topics = {}

def synonymsFunction(word):
  synonyms = []
  #print("Bienvenido a la funcion")
  for syn in wordnet.synsets(word):
    
    for l in syn.lemmas():
          synonyms.append(l.name())
  return synonyms

with open('/home/ernesto/Proyectos/CloneProjects/Synonyms/data/subjects.json') as f:
  data = json.load(f)

for line in range(0,len(data),1):
  #print(line)
   #print(line)
  topics=data[line]["topics"]
  
  

  if len(topics)==0:
      continue
    #print("There aren't anything")
  else:
       
    for each_topic in range(0,len(topics),1):
      #Ejecutar funcion para buscar synonimos
      value.append(topics[each_topic])
      synonyms= synonymsFunction(topics[each_topic])
      synonymALL.append(list(synonyms[:5])) 

    


array_topics = [{"value": t, "synonyms": s} for t, s in zip(value, synonymALL)]
print (array_topics)
# Printing in JSON format
print (json.dumps(array_topics))
with open('/home/ernesto/Proyectos/CloneProjects/Synonyms/topics-synonyms_ONLY.json', 'w') as file:
    json.dump(array_topics, file, indent=len(topics))  