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

        archiveAux = open("lexicon/verbs.txt","r")
        mensaje = archiveAux.read()

        aux = ""
        mensajeFinal = []
        j=0

        for i in range(len(mensaje)):

            if(mensaje[i]!="\n"):
                aux += mensaje[i]
            else:
                mensajeFinal.append(aux)
                j+=1
                aux = ""
                
        '''for i in range(0,j):
            print(mensajeFinal[i])'''
        archiveAux.close()

        for word, tag in tagger.tag(tokens):
            for i in range(len(mensajeFinal)):
                if(word == mensajeFinal[i]):
                    print(word,"y", mensajeFinal[i])
                    counterAux += 1

        if(counterAux == 1):
            self.singleCommand(text.data, mensajeFinal)

        elif(counterAux == 2):
            self.composedCommand(text.data, mensajeFinal)
            #LLamo al comando compuesto

        elif(counterAux == 0):
            counter[0] += 1
            data = "BAD_RECOGNITION"
            oration = "NO_INTERPRETATION"
        
            archive.write("command_%d|%s|%s\n" % (counter[0],data, oration))
        
        

        #print(tokens)
        #tagged = nltk.pos_tag(tokens)
        #print(tagged[0])

        #sent = ['Mitchell', 'decried', 'the', 'high', 'rate', 'of', 'unemployment']
        

        #for word, tag in tagger.tag(sent):
            #print(word, '->', tag)'''

    def singleCommand(self, data, mensajeFinal):

        oration = ""

        print(data)

        tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])

        #sentence = """I am here to take the tv"""
        tokens = nltk.word_tokenize(data)
        print(tokens)

        for word, tag in tagger.tag(tokens):

            for i in range(len(mensajeFinal)):
            
                if(word==mensajeFinal[i] and word != "search" and word != "take" and word != "place" and word != "bring"):
                    counter[0] += 1
                    print("estoy aqui")
                    oration = "MOTION("

                elif (word == "search" and word==mensajeFinal[i]):
                    counter[0] += 1
                    oration = "SEARCHING("

                elif (word == "take" and word==mensajeFinal[i]):
                    counter[0] += 1
                    oration = "TAKING("

                elif (word == "place" or word == "put" and word==mensajeFinal[i]):
                    counter[0] += 1
                    oration = "PLACING("

                elif (word == "bring" and word==mensajeFinal[i]):
                    counter[0] += 1
                    oration = "BRINGING("


        if(oration == ""):
                counter[0] += 1
                data = "BAD_RECOGNITION"
                oration = "NO_INTERPRETATION"
        
        oration += ")"
        
        archive.write("command_%d|%s|%s\n" % (counter[0],data, oration))

    def composedCommand(self, data, mensajeFinal):

        i = 0
        oration = ""

        print(data)

        tagger = UnigramTagger(brown.tagged_sents(categories='news')[:500])

        #sentence = """I am here to take the tv"""
        tokens = nltk.word_tokenize(data)
        print(tokens)

        for word, tag in tagger.tag(tokens):
            
            for j in range(len(mensajeFinal)):
            
                if(word==mensajeFinal[j] and word != "search" and word != "take" and word != "put" and word != "place" and word != "bring"):
                    i += 1

                    if(i==2):
                        counter[0] += 1
                        oration += "#"
                
                    print("estoy aqui")
                    oration += "MOTION("
                    oration += ")"

                elif (word == "search" and word==mensajeFinal[j]):
                    i += 1

                    if(i==2):
                        counter[0] += 1
                        oration += "#"

                    counter[0] += 1
                    oration += "SEARCHING("
                    oration += ")"

                elif (word == "take" and word==mensajeFinal[j]):
                    i += 1

                    if(i==2):
                        counter[0] += 1
                        oration += "#"

                    counter[0] += 1
                    oration += "TAKING("
                    oration += ")"

                elif (word == "place" or word == "put" and word==mensajeFinal[j]):
                    i += 1

                    if(i==2):
                        counter[0] += 1
                        oration += "#"

                    counter[0] += 1
                    oration += "PLACING("
                    oration += ")"

                elif (word == "bring" and word==mensajeFinal[j]):
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