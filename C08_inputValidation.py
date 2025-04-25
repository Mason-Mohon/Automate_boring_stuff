import pyinputplus as pyip
import random, time

numberOfQuestion = 10
correctAnswers = 0
for questionNumber in range(numberOfQuestion):
    #pick two random numbers
    num1 = random.randint(0, 9)
    num2 = random.randint(0, 9)

    prompt = '#%s: %s x %s = ' % (questionNumber, num1, num2)

    try:
        #right answers handled by allow regexes
        #wrong answers handled by block regexes w/ custom message
        pyip.inputStr(prompt, allowRegexes=['^%s$' % (num1 * num2)],
                      blockRegexes =[('.*', 'Wrong answer dummy!')],
                      timeout=8, limit=3)
    except pyip.TimeoutException:
        print('Out of time!')
    except pyip.RetryLimitException:
        print('Out of retries!')
    else:
        print('Correct!')
        correctAnswers += 1

    time.sleep(1)
print('Score: %s / %s' % (correctAnswers, numberOfQuestion))