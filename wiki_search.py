"""
This script gives the user an intro level understanding to some topic they input.
If the topic is specific enough, it will give you a summary (from Wikipedia) and
suggest related topics that would help the user better understand the current
topic & summary.
"""
import requests, bs4, sys

#get topic from user
topic = ''.join(sys.argv[1:]) 

#scrape wikipedia for user given topic 
result = requests.get('https://en.wikipedia.org/wiki/' + topic) 
try:
  result.raise_for_status()

  soup = bs4.BeautifulSoup(result.text, "html.parser")
  #summary of topic on wiki
  paragraphs = soup.select('#mw-content-text > div.mw-parser-output > p:not([class])') 
  
  # if paragraphs = 1, topic is ambiguous, ex. "hey"
  # if 2+ paragraphs selected, topic is unambiguous ex. "Islam"
  if len(paragraphs) == 1:
    headers = soup.select('#mw-content-text > div.mw-parser-output > h3 .mw-headline') 
    related_topics = map(lambda tag: tag.getText(), headers)
    print("Look into " + ', '.join(related_topics) + " on " + topic)
  elif len(paragraphs) > 1:
    for item in paragraphs: 
      #print excerpt
      print(item.getText() + "\n") 

      #finding & printing references related to excerpt
      refs = item.select('p > a')
      n_refs = len(refs)
      refs_to_share = min(3, n_refs)

      msg = ("There are " + str(n_refs) + " other topics that would help " 
        + "you better understand this excerpt. So, if you are confused, " 
        + "try looking into these:")
      print(msg)

      for i in range(refs_to_share):
        print(str(i+1) + ". " + refs[i].getText())
      print("\n")
    
except Exception as error:
  print(error)
