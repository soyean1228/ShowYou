class Analyzer:
    def post_find(self):
        import pymongo

        client = pymongo.MongoClient(
            "mongodb+srv://showyou:showyou@showyou-aznp8.mongodb.net/test?retryWrites=true&w=majority"
        )
        db = client.get_database('ShowYou')
        collection = db.get_collection('post')
        doc = collection.find()
        # for result in doc :
        #     print(result)
        client.close()
        return doc


    def sentiment_analysis_result_insert(self,list):
        import pymongo

        client = pymongo.MongoClient(
            "mongodb+srv://showyou:showyou@showyou-aznp8.mongodb.net/test?retryWrites=true&w=majority"
        )
        db = client.get_database('ShowYou')
        collection = db.get_collection('sentiment_analysis_result')
        collection.drop()
        collection.insert(list)
        client.close()


    def post_category_insert(self,list):
        import pymongo

        client = pymongo.MongoClient(
            "mongodb+srv://showyou:showyou@showyou-aznp8.mongodb.net/test?retryWrites=true&w=majority"
        )
        db = client.get_database('ShowYou')
        collection = db.get_collection('post_category')
        collection.drop()
        collection.insert(list)
        client.close()



    was_initialized=False


    def get_sentiment_analysis_model():
        import keras
        model=keras.models.load_model('showyou/Analyzer/sentiment analysis model')
        return(model)


    def get_category_analysis_model():
        import keras
        model=keras.models.load_model('showyou/Analyzer/category analysis model')
        return(model)


    def get_Tokenizer_for_sentiment_analysis():
        file=open('showyou/Analyzer/Tokenizer for sentiment analysis', 'rb')
        import pickle
        Tokenizer=pickle.load(file)
        file.close()
        return(Tokenizer)


    def get_Tokenizer_for_category_analysis():
        file=open('showyou/Analyzer/Tokenizer for category analysis', 'rb')
        import pickle
        Tokenizer=pickle.load(file)
        file.close()
        return(Tokenizer)


    def get_keywordses(self):
        test_data = self.post_find()

        stopwords = ['의', '가', '이', '은', '들', '는', '좀', '잘', '걍', '과', '도', '를', '으로', '자', '에', '와', '한', '하다']

        import konlpy
        from konlpy.tag import Okt
        okt = Okt()
        X_test = []
        for sentence in test_data:
          temp_X = []
          temp_X = okt.morphs(str(sentence['post']), stem=True) # 토큰화
          temp_X = [word for word in temp_X if not word in stopwords] # 불용어 제거
          X_test.append(temp_X)

        return(X_test)


    def analyze_sentiments(self,Tokenizer,X_test,model):
        X_test = Tokenizer.texts_to_sequences(X_test)

        from keras.preprocessing.sequence import pad_sequences
        max_len = 20 # 전체 데이터의 길이를 20로 맞춘다

        X_test = pad_sequences(X_test, maxlen=max_len)

        predictions = model.predict(X_test)

        sentiments=[]
        for index in range(0,len(predictions)):
            row={}
            row['post_id']=index
            row['sentiment']=float(predictions[index][0])
            sentiments.append(row)

        self.sentiment_analysis_result_insert(sentiments)


    def analyze_categories(self,Tokenizer,X_test,model):
        X_test = Tokenizer.texts_to_sequences(X_test)

        from keras.preprocessing.sequence import pad_sequences
        max_len = 20 # 전체 데이터의 길이를 20로 맞춘다

        X_test = pad_sequences(X_test, maxlen=max_len)

        predictions = model.predict(X_test)

        categories=[]
        for index_for_posts in range(0,len(predictions)):
            highest_prediction=0
            lowest_prediction=1
            for index_for_categories in range(0,6):
                prediction_for_category=predictions[index_for_posts][index_for_categories]
                if prediction_for_category>highest_prediction:
                    highest_prediction=prediction_for_category

                    if index_for_categories==0:
                        category='IT'
                    elif index_for_categories==1:
                        category='건강'
                    elif index_for_categories==2:
                        category='경제'
                    elif index_for_categories==3:
                        category='뷰티'
                    elif index_for_categories==4:
                        category='생활'
                    else:
                        category='엔터테인먼트'

                elif prediction_for_category<lowest_prediction:
                    lowest_prediction=prediction_for_category

            prediction_for_known_category=highest_prediction-lowest_prediction
            prediction_for_unknown_category=lowest_prediction
            if prediction_for_unknown_category>prediction_for_known_category:
                    category='기타'

            row={}
            row['post_id']=index_for_posts
            row['category']=category
            categories.append(row)

        self.post_category_insert(categories)



    @classmethod
    def __init__(cls):
        if not cls.was_initialized:
            print('Analyzer: Analyzer is under initialization.')
            cls.sentiment_analysis_model=cls.get_sentiment_analysis_model()
            cls.Tokenizer_for_sentiment_analysis=cls.get_Tokenizer_for_sentiment_analysis()

            cls.category_analysis_model=cls.get_category_analysis_model()
            cls.Tokenizer_for_category_analysis=cls.get_Tokenizer_for_category_analysis()

            cls.was_initialized=True
            print('Analyzer: Analyzer initialized.')
        else:
            print('Analyzer: Analyzer has initialized.')
        print()


    def analyze(self):
        print('Analyzer: Analyzer is under analysis.')
        keywordses=self.get_keywordses()
        self.analyze_sentiments(self.Tokenizer_for_sentiment_analysis, keywordses, self.sentiment_analysis_model)
        self.analyze_categories(self.Tokenizer_for_category_analysis, keywordses, self.category_analysis_model)
        print('Analyzer: Analyzer analyzed posts.')
        print()



def analyze():
    analyzer=Analyzer()
    analyzer.analyze()
