
import xmltodict
import pprint
with open(fileName, 'r', encoding='utf-8') as file:
    my_xml = file.read()

my_dict = xmltodict.parse(my_xml)

pprint.pprint(my_dict, indent=2)


try:
    newDict = open('xmlDictionary.txt', 'wt')
    newDict.write(str(my_dict))
    newDict.close()
  
except:
    print("Unable to write to file")