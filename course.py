from random import lognormvariate, choices
from math import log


class Lesson(object):
    def __init__(self, vocabulary):
        self.vocabulary = vocabulary
        self.word_mean_length = 3

    def generate(self, n):
        words = []
        for _ in range(n):
            length = round(lognormvariate(log(self.word_mean_length), .3))
            words.append(''.join(choices(self.vocabulary, k=length)))
        result = ' '.join(words)
        result = result[:n]
        result = result.strip()
        return result


class Course(object):
    def __init__(self, kind):
        if kind=='hebrew':
            vocabularies = [['חכ',],
                            ['גל',],
                            ['כחג', 'כחל', 'כחגל',],
                            ['יע','יעכ','יעח','יעחכ', 'יעחכלג']
          # '',
          # '',
          # '',
          ]
        self.lessons = [[Lesson(voc) for voc in l] for l in vocabularies]

        self.group=0
        self.ind=0

    def update(self, current_errors, total_errors, correct):
        if current_errors<3:
            if total_errors<5:
                self.ind+=1
                if len(self.lessons[self.group])==self.ind:
                    self.group+=1
                    self.ind=0

        elif current_errors>6 or total_errors>10:
            if self.ind>0:
                self.ind-=1

    def generate(self,n):
        return self.lessons[self.group][self.ind].generate(n)





