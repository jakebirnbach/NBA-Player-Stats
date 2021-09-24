import requests
import json

#RUNS WITH LOCAL WEB SERVER IN TERMINAL 

url = 'http://localhost:8080/data'

#while True:
 #   try:
  #          data = requests.get(url).json()
   ##        json.dump(data,outfile)
      #      outfile.close()
     #       break
    #except requests.HTTPError as exception:
     #   next
    #except requests.ConnectionError as exception:
     #   next
    #except ValueError:  # includes simplejson.decoder.JSONDecodeError
        #print ('Decoding JSON has failed')
     #   next

#file = open("perams.json", "r")
#x = json.load(file)
#file.close()

#print(x['P1'])

x = 3.553227768593525
print(round(x,3))

#IDEA - Create another class to find culmulative z scores
def draft_main():
    #create async function that does this
    p1 = Player('Stephen','Curry',YEAR_F,YEAR_L)
    p2 = Player('Michael', 'Jordan', 1984, 2003)  

    print('{} {} Mean: '.format(p1.first_name,p1.last_name) +str(p1.mean))
    print('{} {} Mean: '.format(p2.first_name,p2.last_name) +str(p2.mean))
    print(compare_z_scores(p1, p2))
    print('Decade Mean P1: '+str(p1.years_mean))
    print('Decade Stdev P1: '+str(p1.years_std))
    print('Decade Mean P2: '+str(p2.years_mean))
    print('Decade Stdev P2: '+str(p2.years_std))
    plot_z_score(p1, 'p1')
    plot_z_score(p2, 'p2')