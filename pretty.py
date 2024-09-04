import re, requests, sys, json, time


fname = "woc.citations.papers";
if (len(sys.argv) > 1): fname = sys.argv[1]
f = open(fname)
#[u'externalids', u'influentialcitationcount', u'title', u'url', u'publicationtypes', u'journal', u'year', u'venue', u'citationcount', u'publicationdate', u'publicationvenueid', u'authors', u's2fieldsofstudy', u'referencecount', u'corpusid', u'isopenaccess']

for l in f:
  v = json.loads (l)
  #print(v['year'])

  #if v['influentialcitationcount'] <= 0: continue
  a=v['authors']
  aa = ""
  for a0 in a:
    if aa == "": aa = a0['name'].encode('latin-1', 'ignore')
    else: aa += " and " +a0['name'].encode('latin-1', 'ignore')
  dt=v['publicationdate']
  j=v['journal']
  ve=v['venue']
  tit = v['title'].encode('latin-1', 'ignore')
  #print(v['externalids'])
  type="@article{"
  if (re.match('conference', ve, re.IGNORECASE)): type="@inproceedings"
  print (type+v['externalids']['CorpusId']+",")  
  aa=""
  for a0 in a: 
    if aa == "": aa = a0['name'].encode('latin-1', 'ignore')
    else: aa += " and " +a0['name'].encode('latin-1', 'ignore')
  print ("author={"+aa+"},")
  print ("year="+str(v['year'])+",")
  if type == '@article{': print ('journal={'+v['venue']+"},")
  else: print('booktitle={'+v['venue']+"},")
  print ("title = {"+tit+"},")
  
  #print(v['s2fieldsofstudy'])
  print ("note={citation count "+str(v['citationcount'])+", influential citation count "+str(v['influentialcitationcount'])+"},")
  #print (v['publicationtypes'])
  print ("}")




