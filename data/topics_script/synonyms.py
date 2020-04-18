import nltk
import json
from nltk.corpus import wordnet
#nltk.download('wordnet')
#syns = wordnet.synsets("dog")
#Funcion que devuelve sinonimos de las palabras.  
def synonymsFunction(word):
  synonyms = []
  #print("Bienvenido a la funcion")
  for syn in wordnet.synsets(word):
    
    for l in syn.lemmas():
          synonyms.append(l.name())
  
  #print("**************    "+word+"    **************************")
  #print("**************Estos son los sinonimos encontrados****************")
  #print(synonyms)
  return synonyms


antonyms = []
#json_data=json.dumps()
with open('/home/ernesto/Proyectos/CloneProjects/Synonyms/data/subjects.json') as f:
  data = json.load(f)
#
#my_data_file = open('/home/ernesto/Proyectos/CloneProjects/Synonyms/topics-synonyms.json', 'a')
array_topics = []


i=0
for line in range(0,len(data),1):
  #print(line)
  topics=data[line]["topics"]
  id_subjects=data[line]["name"]
  
  #print(topics)
  #print("************  i  *********")
  #print(id_subjects)
  i=i+1
  if len(topics)==0:
    print("There aren't anything")
  else:
       
    for each_topic in range(0,len(topics),1):
      #Ejecutar funcion para buscar synonimos
      
      synonyms= synonymsFunction(topics[each_topic])
      #Aqui se hace el Json de cada topic
      array_topics.append({
          'value':'{}'.format(topics[each_topic]),
          "synonyms": list(synonyms[:5])         
        })  
      
  #print(array_topics)    
  with open('/home/ernesto/Proyectos/CloneProjects/Synonyms/topics-synonyms-name.json', 'w') as file:
    json.dump(array_topics, file, indent=len(topics))   


#with open('/home/ernesto/Proyectos/CloneProjects/Synonyms/topics-synonyms.json', 'w') as outfile:
#   json.dump(array_topics, outfile)

#my_data_file.close()

#for syn in wordnet.synsets("good"):topics_json = (json.loads('/home/ernesto/Proyectos/CloneProjects/Synonyms/data/subjects.json'))


 #   for l in syn.lemmas():
  #      synonyms.append(l.name())
        

#print(set(synonyms))topics_json = (json.loads('/home/ernesto/Proyectos/CloneProjects/Synonyms/data/subjects.json'))


#print(set(antonyms))topics_json = (json.loads('/home/ernesto/Proyectos/CloneProjects/Synonyms/data/subjects.json'))