import rclpy
from rclpy.node import Node

from std_msgs.msg import String

import stanfordnlp
import nltk


from nltk.corpus import brown
from nltk.tag import UnigramTagger

archive=open("output/results.txt","w")
counter = [0]

class audioSubscriber(Node):

    def __init__(self):
        super().__init__('audio_subscriber')

        self.subscription = self.create_subscription(
            String,                                              # CHANGE
            'audio',
            self.listener_callbackS,
            10)
        self.subscription    

    def listener_callbackS(self, text):
        self.get_logger().info('I heardsad: "%s"' % text.data)

        counterAux = 0

        oration = ""

        tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])

        #sentence = """I am here to take the tv"""
        tokens = nltk.word_tokenize(text.data)

        for word, tag in tagger.tag(tokens):
            if(tag == "VB" or tag == "VBD"):
                counterAux += 1

        if(counterAux == 1):
            self.singleCommand(text.data)

        elif(counterAux == 2):
            self.composedCommand(text.data)
            #LLamo al comando compuesto

        #print(tokens)
        #tagged = nltk.pos_tag(tokens)
        #print(tagged[0])

        #sent = ['Mitchell', 'decried', 'the', 'high', 'rate', 'of', 'unemployment']
        

        #for word, tag in tagger.tag(sent):
            #print(word, '->', tag)'''

    def singleCommand(self, data):

        oration = ""

        print(data)

        tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])

        #sentence = """I am here to take the tv"""
        tokens = nltk.word_tokenize(data)
        print(tokens)

        for word, tag in tagger.tag(tokens):
            print(word, '->', tag)
            
            if(tag == "VB" or tag == "VBD" and word != "search" and word != "take" and word != "place" and word != "bring"):
                counter[0] += 1
                print("estoy aqui")
                oration = "MOTION("

            elif (word == "search"):
                counter[0] += 1
                oration = "SEARCHING("

            elif (word == "take"):
                counter[0] += 1
                oration = "TAKING("

            elif (word == "place" or word == "put"):
                counter[0] += 1
                oration = "PLACING("

            elif (word == "bring"):
                counter[0] += 1
                oration = "BRINGING("


        if(oration == ""):
                counter[0] += 1
                data = "BAD_RECOGNITION"
                oration = "NO_INTERPRETATION"
        
        oration += ")"
        
        archive.write("command_%d|%s|%s\n" % (counter[0],data, oration))

    def composedCommand(self, data):

        i = 0
        oration = ""

        print(data)

        tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])

        #sentence = """I am here to take the tv"""
        tokens = nltk.word_tokenize(data)
        print(tokens)

        for word, tag in tagger.tag(tokens):
            print(word, '->', tag)
            
            if(tag == "VB" or tag == "VBD" and word != "search" and word != "take" and word != "put" and word != "place" and word != "bring"):
                i += 1

                if(i==2):
                    counter[0] += 1
                    oration += "#"
                
                print("estoy aqui")
                oration += "MOTION("
                oration += ")"

            elif (word == "search"):
                i += 1

                if(i==2):
                    counter[0] += 1
                    oration += "#"

                counter[0] += 1
                oration += "SEARCHING("
                oration += ")"

            elif (word == "take"):
                i += 1

                if(i==2):
                    counter[0] += 1
                    oration += "#"

                counter[0] += 1
                oration += "TAKING("
                oration += ")"

            elif (word == "place" or word == "put"):
                i += 1

                if(i==2):
                    counter[0] += 1
                    oration += "#"

                counter[0] += 1
                oration += "PLACING("
                oration += ")"

            elif (word == "bring"):
                i += 1

                if(i==2):
                    counter[0] += 1
                    oration += "#"

                counter[0] += 1
                oration += "BRINGING("
                oration += ")"

        

        if(oration == ""):
                counter[0] += 1
                data = "BAD_RECOGNITION"
                oration = "NO_INTERPRETATION"
        
        
        
        archive.write("command_%d|%s|%s\n" % (counter[0],data, oration))

        
        
            
        

def main(args=None):
    
    rclpy.init(args=args)

    audio_subscriber = audioSubscriber()

    rclpy.spin(audio_subscriber)

    audio_subscriber.destroy_node()
    rclpy.shutdown()
    archive.close()


if __name__ == '__main__':
    main()