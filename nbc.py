# Naive Bayes Classifier
#1.Separate into two groups 'spam' and 'ham'
#	Load lines from file for each line
#	Spam if it begins with 1; Ham if it begins with 0
#	After emails are separated, count words
#2.Count within each group
#3.Adjust the counts by applying add-one smoothing. Add the UNKNOWN word.
#4.Change the adjusted counts to probabilities.
#5.Write a function that uses the probabilities to classify emails. To avoid underflow errors, add log probabilities.
#6. Apply the function to the test data.
#7. Calculate precision and recall. (Demoninator for precision is the # the machine classified as spam, for recall it is the number of actual spam in the data.)(Accuracy includes hams and spams not just spams.)

import math
#Create separate dictionaries for spam and ham
spam_words = {} #e.g. spam words['nigeria'] = 10 
ham_words = {} #e.g. ham words['nigeria'] = 1
spam_count = 0.0
ham_count = 0.0

#Populate dictionary with keys(words) and values(counts)
for line in open('./spam_assassin.train'):
	#Extract labels and words from lines
	splitted = line.split() #remove whitespaces (create list of substrings)
	label = splitted[0] #first element is label '0' or '1'
	words = splitted[1:] #remaining items are words
	#Count spams ('1') and hams (else)
	if label == '1': 
		spam_count += 1
	else:
		ham_count +=1
	for word in words:
		if label == '1': 
			#increment frequency in spam words
			if word in spam_words: #check if key is in dictionary
				spam_words[word] += 1 #Exists? increment count
			else:
				spam_words[word] = 1 #Nonexistant? Assign count of 1

		else: 
			#increment frequency in ham words
			if word in ham_words: #check if key is in dictionary
				ham_words[word] += 1 #Exists? Count +=1
			else:
				ham_words[word] = 1 #Nonexistant? Count = 1
# 3. +1 Smoothing
#Add unknown word and assign count 0 then +1 for each element in spam_words & ham_words
spam_words['<UNKNOWN>'] = 0
ham_words['<UNKNOWN>'] = 0
for word in spam_words:
	spam_words[word] +=1
for word in ham_words:
	ham_words[word] +=1

# 4. Calculate Probabilities
#Calculate total values of ham and spam
ham_total = float(sum(ham_words.values())) 
spam_total = float(sum(spam_words.values())) 

for word in ham_words:
	ham_words[word] /= ham_total #P(word|ham)
for word in spam_words:
	spam_words[word] /= spam_total #P(word|spam)

spam_prior = spam_count / float(spam_count+ham_count) #Returns prior P(spam)
ham_prior = ham_count/ float(spam_count+ham_count) #Returns prior P(ham)

# 5. Classifier Function
def classify(input_mail, spam_prior, ham_prior, spam_words, ham_words):
	#Calculate scores for spam and ham
	spam_score = math.log(spam_prior) 
	ham_score = math.log(ham_prior)#Set scores to log of prior value
	for word in input_mail: #iterate over each word in input_mail
		spam_score += math.log(spam_words.get(word, spam_words['<UNKNOWN>']))
		ham_score += math.log(ham_words.get(word, ham_words['<UNKNOWN>'])) 
	if spam_score >= ham_score:
		return '1'
	else:
		return '0'

both_said_spam = 0
we_said_spam = 0
data_said_spam = 0
test_file = open ('./spam_assassin.test')
for line in test_file:
	ll=line.split()
	answer = ll[0]
	input_words = ll[1:]
	prediction = classify(input_words, spam_prior, ham_prior, spam_words, ham_words)
	if answer == '1' : data_said_spam += 1
	if prediction == '1' : we_said_spam +=1
	if answer == '1' and prediction == '1' : both_said_spam += 1
test_file.close()

precision = float(both_said_spam) / we_said_spam
recall = float(both_said_spam) / data_said_spam

print 'precision =', precision
print 'recall =' , recall



 
