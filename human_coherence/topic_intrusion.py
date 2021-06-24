import warnings
warnings.warn("deprecated", DeprecationWarning)

import gensim
import gensim.corpora as corpora
from gensim.test.utils import datapath
import random

def main():
    loaded_dict = corpora.Dictionary.load('dictionary')
    
    lda_model = gensim.models.LdaModel.load('lda.model')

    tot = len( lda_model.show_topics() )
    while True:
        topic_id = input('{} Topics are available. Select the topic number you want to run the generator for  [1-{}] : '.format(tot, tot))
        if not topic_id.isnumeric():
            print('Please enter the positive integer')  
        elif (int(topic_id) <1) or int(topic_id) >tot:
            print('Please enter the correct value')
        else:
            break
            
    topic_id = int(topic_id)
    print('Generating terms for the topic ', topic_id)

    ab = lda_model.print_topic(topic_id-1, 15)
    words = [item[7:-1] for item in ab.replace(' ', '').split('+')]
    realwords = random.sample(words, 5)

    intrud_ind = random.choice(range(0, len(loaded_dict)))
    intruder = loaded_dict[ intrud_ind ]

    realwords.append(intruder)
    random.shuffle( realwords )

    print('Terms are generated for Topic {}, which one is the intruder?[1-6]'.format(topic_id))
    for i in range(6):
        print('{}- {}'.format(i+1, realwords[i]))
        
    while True:
        intruder_id = input('Please write the integer of intruder[1-{}] : '.format(6))
        if not intruder_id.isnumeric():
            print('Please enter the positive integer')
        elif (int(intruder_id) <1) or int(intruder_id) >6:
            print('Please enter the correct value')
        else:
            sel_int = realwords[int(intruder_id)-1]
            if sel_int == intruder:
                print('Correct!')
            else:
                print('Incorrect! (Correct value is {})'.format(intruder))
            break

        
        
if __name__ == "__main__":
    
    while True:
        main()
        temp = input('\n\n Please enter 0 to exit and any other key to continue: ')
        
        if temp =='0':
            break

