import pandas as pd
from nltk.stem.wordnet import WordNetLemmatizer
from nltk.corpus import wordnet as wn
from nltk.corpus import stopwords
from nltk import pos_tag
from nltk.tokenize import word_tokenize
import re
import pickle
import os

with open('./utils/stopwords.txt') as f:
  additional_stopwords = f.read().splitlines()

custom_stopwords = set(stopwords.words('english') + list(additional_stopwords))

lemma = WordNetLemmatizer()

def get_wordnet_pos(tag):
    if tag.startswith('J'):
        return wn.ADJ
    elif tag.startswith('V'):
        return wn.VERB
    elif tag.startswith('N'):
        return wn.NOUN
    elif tag.startswith('R'):
        return wn.ADV
    else:
        return wn.VERB

def save_obj(obj, name ):
  with open('./pickle-files/' + name + '.pkl', 'wb') as f:
    pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)

def load_obj(name ):
  with open('./pickle-files/' + name + '.pkl', 'rb') as f:
    return pickle.load(f)

def pre_process (text):
  text = text.lower()
  text = re.sub("(\\d|\\W|\\_)+"," ",text)
  tokens = word_tokenize(text)
  pos_tokens = pos_tag(tokens)
  lemmatized_tokens = [lemma.lemmatize(token[0], pos=get_wordnet_pos(token[1])) for token in pos_tokens]
  text = [word for word in lemmatized_tokens if word not in custom_stopwords]
  return text



docs = pd.DataFrame(load_obj('analyzed_articles'))
print(docs.head(3))
print(docs.dtypes)

# docs['full_text'] = docs['title'] + " " + docs['text']
# docs['full_text'] = docs['full_text'].apply(lambda x: pre_process(x))
# print(docs['full_text'][10])



doc = "Hello my name is Daniel and 'this' is cool!!! Hopfully this will works! Did it work? Maybe??? !@#$%^&*()_+ ?><{}[] loving loves loved. Pandas is cool. I loved you"
print(pre_process(doc))


test = "devah pager who documented race bias in job market dies at supported by by katharine q seelye devah pager a harvard sociologist best known for rigorously measuring and documenting racial discrimination in the labor market and in the criminal justice system died on nov at her home in cambridge mass she was michael shohl her husband said the cause was pancreatic cancer in her seminal work dr pager who was the peter and isabel malkin professor of public policy at the kennedy school of government at harvard and a professor of sociology at the university documented what she called the powerful effects of race on hiring decisions which she said contributed to persistent inequality employers she found were more likely to hire a white man even if he had a felony conviction than a black man with no criminal record this suggests that being black in america today is essentially like having a felony conviction in terms of one s chances of finding employment dr pager said in a video interview with the stanford center on poverty and inequality her finding which appeared first in her doctoral dissertation in at the university of wisconsin madison surprised many i am a scholar of race relations william julius wilson the harvard sociologist and author of the declining significance of race said in an email and prior to devah s research i would not have predicted this finding read about five other women who changed our thinking about race her research quickly found its way into the presidential campaign howard dean the former vermont governor and at one time the leading contender for the democratic nomination often cited it saying he was determined to combat the institutional racism it revealed with the subject in the air and the recognition that ex convicts were less likely to commit more crimes if they had a job president george w bush created a program to help newly released prisoners re enter the job market white house aides said at the time that dr pager s study had helped shape the plan her research was remarkable enough for having such an immediate effect on public policy it was all the more unusual for having originated as a dissertation graduate students are not often able to undertake field experiments on such a scale but she cobbled together funding from five sources including the national science foundation to support her work her dissertation became a book marked race crime and finding work in an era of mass incarceration by her mid s she had established herself as a historic figure in the scientific study of racial discrimination mitchell duneier chairman of the sociology department at princeton said in a telephone interview her work was so well regarded that she had been on track to be elected to the prestigious national academy of sciences a rare achievement in any case but even rarer for someone in sociology for a woman and for one so young upon her death her name was removed from the ballot because membership cannot be given posthumously had she not died she was a sure bet to be elected robert m hauser who was one of dr pager s advisers on her dissertation at wisconsin said in a telephone interview devah iwalani pager was born on march in honolulu her father david pager is professor emeritus of computer sciences at the university of hawaii her mother sylvia topor pager who died in was a pediatrician in addition to her husband and her father she is survived by her son atticus who is and two brothers chet and sean she and mr shohl were married in after dr pager s diagnosis she grew up in hawaii where she attended the private punahou school she earned a bachelor s degree in psychology from the university of california los angeles in a master s in sociology from the university of cape town in a second master s from stanford in and a doctorate in sociology from wisconsin in before becoming a fulbright scholar in paris dr pager became attuned to racial issues when she left hawaii which has a high rate of interracial marriage for los angeles which she found more segregated when you grow up with that being normal she told the new york times in everything else seems strange and wrong in madison she volunteered to help homeless men she met many black men with prison records who told her of their difficulties finding work that gave her the idea to try to isolate the effect of a felony conviction on job applicants she recruited two teams of young well groomed well spoken college men of the same height one team black the other white and gave them identical résumés as they applied for entry level jobs in milwaukee the applicants took turns saying they had served an month sentence for cocaine possession dr pager said that even she had been surprised by the results a follow up telephone survey showed that blacks who said they had a criminal record had a callback rate of percent and blacks who said they did not had a rate of percent for whites the rates were percent for those who said they had a criminal record and percent for those who said they did not a memorial to those who lost their lives in before dr pager s research it was believed that ex convicts struggled to get jobs because they didn t have the right set of skills said prof david b grusky of stanford who worked with dr pager discrimination hadn t been considered a prominent reason what devah showed contrary to this view is that employers do indeed discriminate he said in an email and not just a little bit on the margins she went on to replicate these findings in in a similar study in new york city at the time she was teaching at princeton and worked with bruce western another princeton sociologist this time the teams applied for jobs their findings gave momentum to the so called ban the box movement which urged employers to eliminate the box on job applications asking whether the applicant had a felony record several major employers including walmart home depot and koch industries have now removed the question from their job applications ultimately the equal employment opportunity commission issued a guidance saying that a criminal record by itself shouldn t disqualify people said dr western who now teaches at columbia and had been in the midst of another project with dr pager when she died there was a direct line from devah s work to that guidance dr pager was a mentor to scores of students and continued to teach until three weeks before her death her husband said she loved to ride bikes sing and dance and frequently organized karaoke nights her signature song was the anthem popularized by gloria gaynor i will survive advertisement"

print(pre_process(test))
