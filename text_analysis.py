import nltk
from nltk import tokenize, corpus
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords, wordnet
from nltk.stem import PorterStemmer
import string
import re

"""
v1: tokenizes sentence. eliminates stopwords and cuts the words down to stems.
it them compares the theoretical synsets with the student's synsets and associate a similarity score.
Works well except when a lot adjectives are added in the theoretical answer. 
"""

class QuestionContainer():
    def __init__(self, question, answer='', studentAnswer=""):
        """
        question is the question in string-form
        answer is the theoretical answer to the question. it may be left blank.
        student answer is set to an empty list at first, since it will be entered later on.
        """
        self.question = word_tokenize(question)
        self.answer = word_tokenize(answer)
        self.studentAnswer = word_tokenize(studentAnswer)
    
    def setQuestion(self, newQuestion):
        self.question = word_tokenize(newQuestion)
    
    def setAnswer(self, newAnswer):
        self.answer = word_tokenize(newAnswer)
    
    def setStudentAnswer(self, studentAnswer):
        self.studentAnswer = word_tokenize(studentAnswer)

    def getQuestion(self):
        return self.question
    
    def getAnswer(self):
        return self.answer

    def getStudentAnswer(self):
        return self.studentAnswer

    def lemmatize(self):
        """
        First part of text analysis. Every word must be converted back to its base form (lemma).
        """
        lemmedQ = []
        lemmedA = []
        lemmedSA = []

        ps = PorterStemmer()

        for i in self.question:
            lemmedQ.append(ps.stem(i))

        for i in self.answer:
            lemmedA.append(ps.stem(i))

        for i in self.studentAnswer:
            lemmedSA.append(ps.stem(i))

        return lemmedQ, lemmedA, lemmedSA

    def removeStopWords(self):
        """
        This method is used to remove the stopwords from the instance's question,
        the theoretical answer and the student's answer
        """
        question, answer, studentAnswer = self.lemmatize()

        stop_words = set(corpus.stopwords.words("english"))

        question = [w for w in question if w not in string.punctuation and len(w) > 0 and w.lower() not in stop_words]
        answer = [w for w in answer if w not in string.punctuation and len(w) > 0 and w.lower() not in stop_words]
        studentAnswer = [w for w in studentAnswer if w not in string.punctuation and len(w) > 0 and w.lower() not in stop_words]

        return question, answer, studentAnswer
   
    def synsetExtraction(self):
        """
        After lemmatizing the words and removing stopwords, we can proceed to extracting the core themes.
        for v1, we will build a database around the theoretical answer
        """
        question, answer, studentAnswer = self.removeStopWords()

        questionSyn = []
        answerSyn = []
        studentAnswerSyn = []

        for i in question:
            questionSyn.append(wordnet.synsets(i))

        for i in answer:
            answerSyn.append(wordnet.synsets(i))

        for i in studentAnswer:
            studentAnswerSyn.append(wordnet.synsets(i))

        return questionSyn, answerSyn, studentAnswerSyn

    def compareAnswers(self):
        """
        v1: comparison will go to 1-depth hyponym. 
        This means part of a student's answer will be GOOD if it is part of either
        part of the theoretical answer's direct synsets OR their direct hyponyms.
        If a synset from a word from the student's answer matches
        a) an answer's direct synset or
        b) an answer's 1-depth hyponym,
        then it's counted as a "good" word
        """
        similarity = 0
        questionSyn, answerSyn, studentAnswerSyn = self.synsetExtraction()
        # studentAnswerSyn de forme [syn1, syn2, syn3]
        # syn1 de forme [synonym1, synonym2, synonym3]
        realAnswerSynSet = [i for i in answerSyn if i not in questionSyn]
        realAnswerSyn = set()
        expr = r"(.[a-z].[0-9]{2})$" #forme .[lettre].[nombre]
        for i in realAnswerSynSet:
            for j in i:
                synonym = j.name()
                synonym = re.sub(expr, "", synonym)
                realAnswerSyn.add(synonym)

        checked_synonyms = set()
        for i in studentAnswerSyn:
            for j in i:
                synonym = j.name()
                synonym = re.sub(expr, "", synonym)
                if synonym not in checked_synonyms:
                    checked_synonyms.add(synonym)
                    if synonym in realAnswerSyn: #if any of the synonyms match, similarity += 1 and we move on to next word
                        similarity += 1
                        realAnswerSyn.remove(synonym)
                        break
                checked_synonyms.add(synonym)

        return round(similarity/len(realAnswerSynSet), 4)

if __name__ == "__main__":

    Q1 = QuestionContainer("What is the tree mainly made of?", "A tree is mainly made of bark, sap, wood, leaves.")
    "elements importants: bark, sap, wood, leaves"

    Q1.setStudentAnswer("Trees are mainly made of wood, bark, leaves.")

    print(Q1.compareAnswers())
    #test plus poussé

    Q2 = QuestionContainer("What is blood?", 
                            "Blood is a combination of plasma and cells that circulate through the entire body. \
                            It is a specialized bodily fluid that supplies essential substances \
                            around the body, such as sugars, oxygen, and hormones. \
                            It also removes waste from the cells in the body.",
                            "Blood is a fluid that circulates in our body, 45%\ cells \
                            (red blood cells containing hemoglobin to transport oxygen, white blood cells \
                            for one immune defense, platelets to help blood clot), 55%\ fluid containing proteins, \
                            coagulation factors, antibodies etc. etc., it transports oxygen and nutrients all around the body.")

    print(Q2.compareAnswers())

    Q3 = QuestionContainer("What is plasma made of?",
                            "atomic nuclei and their electrons.",
                            "Plasma physics is about gasses heated until the molecules \
                            are broken down into atoms and the atoms are broken down into \
                            positively charged nuclei and free-flying electrons. \
                            All this breaking happens because the kinetic energy of atoms \
                            and molecules increases as temperature increases.")
    
    print(Q3.compareAnswers())

    Q4 = QuestionContainer("What color is the sky?", "The sky is blue or gray", "The sky is oftentimes blue in color or grey")
    print(Q4.compareAnswers())
    Q5 = QuestionContainer("What color is the sky?", "The sky is blue or gray", "The sky is oftentimes bluish in color or grey")
    print(Q5.compareAnswers())
 