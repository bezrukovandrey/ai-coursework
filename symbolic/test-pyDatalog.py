from pyDatalog import pyDatalog 


# Initial (binary) predicates (on which facts are built)
pyDatalog.create_terms('age, nbDependentChildren, yearlyIncome, currentAccount, savingsAccount, debtLevel, healthStatus, workStatus, loanPurpose, loanAmount, loanDuration, personalContribution, loanFile')

# Variables for the queries
pyDatalog.create_terms('X, Y, Z')


# Example of a set of facts
+age('p1', 35)
+nbDependentChildren('p1', 2)
+yearlyIncome('p1', 60000)
+currentAccount('p1', 10000)
+savingsAccount('p1', 30000)
+debtLevel('p1', 'low')
+healthStatus('p1', 'good')
+workStatus('p1', 'cdi')
+loanPurpose('p1', 'propertypurchase')
+loanAmount('p1', 400000)
+loanDuration('p1', 120)
+personalContribution('p1', 100000)
+loanFile('p1', 'complete')

+age('p2', 30) , 
+nbDependentChildren('p2', 0) , 
+yearlyIncome('p2', 40000),
+currentAccount('p2', 10000) , 
+savingsAccount('p2' , 5000), 
+debtLevel('p2', 'low'),
+healthStatus('p2', 'good'), 
+workStatus('p2','cdd'), 
+loanPurpose('p2', 'propertypurchase'),
+loanAmount('p2', 200000), 
+loanDuration('p2', 120), 
+personalContribution('p2', 10000),
+loanFile('p2', 'correct')


# Abstraction rules 
pyDatalog.create_terms('ageRange, incomeRange, durationRange, contributionRange, amountRange, hasRegularSalary, hasSalary, savings')
 
ageRange(X, 'young', 'R1')  <= age(X, Y) & (Y < 30)
ageRange(X, 'medium', 'R2') <= age(X, Y) & (Y >= 30) & (Y < 50)
ageRange(X, 'senior', 'R3') <= age(X, Y) & (Y >= 50)

incomeRange(X, 'high', 'R4') <= yearlyIncome(X,Y) & (Y > 60000)
incomeRange(X, 'medium', 'R5') <= yearlyIncome(X,Y) & (Y > 30000) & (Y <= 60000)
incomeRange(X, 'low', 'R6') <= yearlyIncome(X,Y) & (Y <= 30000)
durationRange(X , 'short', 'R7') <= loanDuration(X,Y) & (Y <= 36)
durationRange(X , 'medium', 'R8') <= loanDuration(X,Y) & (Y > 36) & (Y <= 60)
durationRange(X , 'long', 'R9') <= loanDuration(X,Y) & (Y > 60)
contributionRange(X,'weak', 'R10') <= personalContribution(X,Y) & (Y < 10000)
contributionRange(X,'medium', 'R11') <= personalContribution(X,Y) & (Y >= 10000) & (Y < 40000)
contributionRange(X,'high', 'R12') <= personalContribution(X,Y) & (Y >= 40000)
amountRange(X,'low', 'R13') <= loanAmount(X, Y) & (Y < 20000)
amountRange(X,'medium', 'R14') <= loanAmount(X, Y) & (Y >= 20000) & (Y < 100000)
amountRange(X,'high', 'R15') <= loanAmount(X, Y) & (Y >= 100000)
hasRegularSalary(X, 'R16') <= workStatus(X,'cdi')
hasSalary(X, 'R17') <= workStatus(X,'cdd')
hasSalary(X, 'R18') <= hasRegularSalary(X)
savings(X,'bad', 'R19') <= currentAccount(X,Y) & savingsAccount (X,Z) & (Z/Y < 2)
savings(X,'good', 'R20') <= currentAccount(X,Y) & savingsAccount (X,Z) & (Z/Y >= 2)

pyDatalog.create_terms('financialSituation, risk, loanQuality, situation, decision')

financialSituation(X,'good', 'R21') <= hasRegularSalary(X) & incomeRange(X, 'medium')
financialSituation(X,'good', 'R22') <= hasSalary(X) & incomeRange(X, 'high')
financialSituation(X,'good', 'R23') <= contributionRange(X,'high') & amountRange(X,'low')
financialSituation(X,'good', 'R24') <= contributionRange(X,'medium') & savings(X,'good')
risk(X,'weak', 'R25') <= durationRange(X , 'medium') & debtLevel(X,'moderate') & hasRegularSalary(X)
risk(X, 'moderate', 'R26') <= durationRange(X , 'medium') & debtLevel(X,'high')& hasRegularSalary(X)
risk(X,'reasonable', 'R27') <= risk(X,'moderate')
risk(X,'reasonable', 'R28') <= risk(X,'weak')
loanQuality(X,'good', 'R29') <= loanPurpose(X,'consumption') & loanFile(X,'complete')
loanQuality(X,'good', 'R30') <= loanPurpose(X,'consumption') & loanFile(X,'correct')
loanQuality(X,'good', 'R31') <= loanPurpose(X,'propertypurchase') & loanFile(X,'complete')
loanQuality(X,'middle', 'R32') <= loanPurpose(X,'other') & loanFile(X,'complete')
loanQuality(X,'middle', 'R33') <= loanPurpose(X,'propertypurchase') & loanFile(X,'correct')
situation(X, 'favourable', 'R34') <= ageRange(X,'young') & workStatus(X,'cdi')
situation(X, 'favourable', 'R35') <= ageRange(X,'medium') & workStatus(X,'cdi') & healthStatus(X,'good')
situation(X, 'favourable', 'R36') <= ageRange(X,'senior') & healthStatus(X,'good') & nbDependentChildren(X,0)

decision(X,'yes', 'R37') <= financialSituation(X,'good') & loanQuality(X,'good')
decision(X,'yes', 'R38') <= financialSituation(X,'good') & ~(loanQuality(X,'good')) & risk(X, 'reasonable')
decision(X,'yes', 'R39') <= financialSituation(X,'good') & ~(loanQuality(X,'good')) & ~(risk(X, 'reasonable') ) & situation(X,'favourable')
decision(X,'yes', 'R40') <= risk(X,'weak') & savings(X,'good') & loanQuality(X,'good')
decision(X,'yes', 'R41') <= risk(X,'weak') & savings(X,'good') & loanQuality(X,'middle')
decision(X,'no', 'R42') <= risk(X,'weak') & savings(X,'good') & ~(loanQuality(X,Y))
decision(X,'no', 'R43') <= financialSituation(X,'good') & ~(loanQuality(X,'good')) & ~(risk(X, 'reasonable') ) & ~(situation(X,'favourable'))
decision(X,'no', 'R44') <= savings(X,'bad') & ~(financialSituation(X,'good')) & loanQuality(X,'middle')
decision(X,'no', 'R45') <= savings(X,'bad') & ~(financialSituation(X,'good')) & risk(X,'moderate')

print(decision(X,Y))
