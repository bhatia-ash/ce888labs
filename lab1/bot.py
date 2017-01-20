from sopel import module
from emo.wdemotions import EmotionDetector

emo = EmotionDetector()

start = [0, 0, 0, 0, 0, 0]
avg = [0,0,0,0,0,0]
count = 0

@module.rule('')
def hi(bot, trigger):
    global start, count, avg
    print(trigger, trigger.nick)
    #bot.say('Hi, ' + trigger.nick)
    res = emo.detect_emotion_in_raw_np(trigger)
    count += 1
    for i in range(len(res)):
        start[i] += res[i]
        avg[i] = start[i] / count
    print('anger: ' + str(avg[0]))
    print('disgust: ' + str(avg[1]))
    print('fear: ' + str(avg[2]))
    print('joy: ' + str(avg[3]))
    print('sadness: ' + str(avg[4]))
    print('surprise: ' + str(avg[5]))






