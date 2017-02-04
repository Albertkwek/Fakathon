import nltk
from nltk.sentiment.vader import SentimentIntensityAnalyzer

'''
The code here is to take all the cleaned data(titles, articles, links, pictures) and extract all the variables needed.
input: a json file including all the data
output: a json file including all the variables
'''

def extractor(data):
    sid = SentimentIntensityAnalyzer()

    #############################################################################################################
    #This code is to take care of the title
    def title_extractor(title):

        result = {'title_length':len(title.split())}

        punc_count = 0
        for letter in title:
            if not ((letter <= 'z' and letter >= 'a') or (letter <= 'Z' and letter >= 'A') or letter == ' '):
                punc_count += 1
        result['title_puncutation'] = punc_count/len(title.split())
        
        result['title_sentiment_pos'] = sid.polarity_scores(title.lower())['pos']
        result['title_sentiment_neu'] = sid.polarity_scores(title.lower())['neu']
        
        #I want to get the subjectivity here. But some problems occur.
        
        word_type = nltk.pos_tag(title.split())
        import collections
        word_type = collections.Counter([i[1] for i in word_type])
        result['title_compounds'] = {i:word_type[i]/sum(word_type.values()) for i in word_type.keys()}
        
        return result
    
    #############################################################################################################
    #This code is to take care of the body.
    
    def body_extractor(body):
        result = {'body_length':len(body.split())}

        punc_count = 0
        for letter in body:
            if not ((letter <= 'z' and letter >= 'a') or (letter <= 'Z' and letter >= 'A') or letter == ' '):
                punc_count += 1
        result['body_puncutation'] = punc_count/len(body.split())
        
        #Sentiment
        result['body_sentiment_pos'] = sid.polarity_scores(body.lower())['pos']
        result['body_sentiment_neu'] = sid.polarity_scores(body.lower())['neu']
        
        #Complexity
        from nltk import sent_tokenize,word_tokenize
        num_chars=len(body)
        num_words=len(word_tokenize(body))
        num_sentences=len(sent_tokenize(body))
        vocab = {x.lower() for x in word_tokenize(body)}
        result['body_char_per_word'] = int(num_chars/num_words)
        result['body_word_per_sent'] = int(num_words/num_sentences)
        result['body_vocab_rate'] = (len(vocab)/num_words)
        
        #I want to get the subjectivity here. But some problems occur.
        
        return result
    
    #############################################################################################################
    #This code is to take care of the links.
    def link_extractor(link):
        domain_set = []
        from urllib.parse import urlparse
        for url in link:
            parsed_uri = urlparse( url )
            domain = '{uri.scheme}://{uri.netloc}/'.format(uri=parsed_uri)
            domain_set.append(domain)
        return {'links':dict(collections.Counter(domain_set))}
        
    result = title_extractor(data['title'])
    result.update(body_extractor(data['body']))
    result.update(link_extractor(data['link']))
    result.update('resource':data['resource'])
        
    return result



####################################################################
#Testing codes here
extractor({'resource':'Eagles',
        'title':'Welcome to the Hotel California! Such a lovely place such a lovely place such a lovely space!','link':['http://stackoverflow.com/questions/2161752/how-to-count-the-frequency-of-the-elements-in-a-list',
                                                                                                                          'https://www.facebook.com/messages/t/linusyatlong',
                                                                                                                          'https://drive.google.com/drive/u/1/folders/0B4S26umk_9w8SWJDQWdNSTFxME0'],
          'body': '''On a dark desert highway, cool wind in my hair Warm smell of colitas, rising up through the air
Up ahead in the distance, I saw a shimmering light
My head grew heavy and my sight grew dim
I had to stop for the night
There she stood in the doorway;
I heard the mission bell
And I was thinking to myself,
"This could be Heaven or this could be Hell"
Then she lit up a candle and she showed me the way
There were voices down the corridor,
I thought I heard them say...

Welcome to the Hotel California
Such a lovely place (Such a lovely place)
Such a lovely face
Plenty of room at the Hotel California
Any time of year (Any time of year)
You can find it here

Her mind is Tiffany-twisted, she got the Mercedes bends
She got a lot of pretty, pretty boys she calls friends
How they dance in the courtyard, sweet summer sweat.
Some dance to remember, some dance to forget

So I called up the Captain,
"Please bring me my wine"
He said, "We haven't had that spirit here since nineteen sixty nine"
And still those voices are calling from far away,
Wake you up in the middle of the night
Just to hear them say...

Welcome to the Hotel California
Such a lovely place (Such a lovely place)
Such a lovely face
They living it up at the Hotel California
What a nice surprise (what a nice surprise)
Bring your alibis

Mirrors on the ceiling,
The pink champagne on ice
And she said "We are all just prisoners here, of our own device"
And in the master"s chambers,
They gathered for the feast
They stab it with their steely knives,
But they just can"t kill the beast

Last thing I remember, I was
Running for the door
I had to find the passage back
To the place I was before
"Relax, " said the night man,
"We are programmed to receive.
You can check-out any time you like,
But you can never leave! "'''})