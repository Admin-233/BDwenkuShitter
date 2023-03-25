import pandas as pd
import numpy as np
import tls_client
from revChatGPT.ChatGPT import Chatbot
import time

token = "eyJhbGciOiJkaXIiLCJlbmMiOiJBMjU2R0NNIn0..TGqMlR68FwoAS6vR.c0dgfwHla1rtSc_s2q80kEqYFIW78QwoJ_zXfuf5gmOqFOXIXvju_AifJRwKhCeJ264EknItJRofLkaK38D8JfODsY-jLyXfpCXB_uzYPnznwdEbc1F1YsANJtzaps74P4kVHTR0r9vYVOBxvLsItaHrZolGfWm7NkXHupqjhBt6ugdAc76NZswzFDmnk9gcRq1k6CtsdVxvhnAPR6YkwozSeTWkcmuxZRrAhogGT8J3I3V8HsfLhxgrj54WqFTGwdVBaclhSiqzP0hXbLHaEMZ_lTyq3qm5MMa0xMz9Y_XVfXbha2mYtEixd0x8oVaXoydCNmFjWBwONH9MJgkLV0HlPRdSYorem5rDo_UNGRq4BySFyLrQHA5AtGx4xAmNrWUMCUOSP9y0XVWKJVJMLD80odTi-ldAvxSr_VYT2ibohNxbd8y7oO4res9VUZ0RdCSagcIhl8NmOIWi3nKdQhG-lgdfIUM8zTn34B6Iy_FsgyCvAl6c99-kIANmmWqGBD3ry1m8NzwYEiPIz8IKMEzNwdf3hX0HB2qIcxYGal9OZYSd0swydkaGZ0rDY83YofOHXSK_QqpEUWdOYHzEnOEWnwOwLlooFkJixUXWLXes9HdawMBmjOMMTesL2aXuLQYsBnF0mjf54YEyy8B_2UriopNcfZv_zH7XgJ7CSI7YkziF8bbKIHeHpOQDXFYJD8l7aHQRKL6Q-5vIAWMEqFPlNsx4VqerUpu-NJmM-hUxK-bduVE5rllWlrjwcCvbiCEmaoD54Y4Lh1u_OnPbeSQ8IcZzP8GoNzYqSXmZkHYnB8H2992GAVgjNU_9sCkaXdHWqIP17lXMD1AFXcy2lpR-DHnB_MBTKbFybgXawQbeeRpfWD5BBWThMAGTdLjjiPQHfViY6syl3v1Riaf1-2buMKDEMstCoKXEs6M_SLQiLkZjUllNlA8fx2wr3SLanugztT2te2myYsAelpIe2kopJops5Jaew5S_I2HntAmKgCej0rQG3H1RVaijBesuEZE-KI5OW4xduZdOew3A_Zuxhvh6x1AT9bUXnfnCbDMYiwwXrWzvHbq7c1COyh7QrllSVO0XWkXfbhaLtJ81oTqBevHH-UKPVju5XMI1ALE_h8Z1D8g_mVyoQTh8bMuED0p0g1sy3_-TYKLV2DeIZLUDg31AlyophXqAwxxmJ-VYCn9kckandHcQyfKJtY5O9515cep7Zp60f-IgQ7UxIZAtZ2GsxwVJeK1YmJ8D-o88w7uHw_pB-uFhMuwuAxnF_mALTs5-Bw9u-KNKNS_UHN9R23FpEWTPSN9a-BknKrusxsb7lzNuccg51E4ezR0snmMCaBCSUw3RNi7p9ibYRTKtYok7UbrkmOQq9ummC72IsEYIK8kANiGIVukH792S2_m23OGYnKnRjQhzLbd6sQpJ3QXCsNB6Zvj79UmizKzxqChmFaNwjTaoVqOgGTufD6OslZjAxh0nQHGvI1SsOeEXAnzXYWjzP8tLyocWJVmaEfAtjDCz3gYAFEq8kbRXb3nt74S2MQwHwd_LwOqegeMg5oQNsj3S8kFW0aq59ogU9UbO_oj_JcjkInCJWDfvy6U_jjtnwoDGDyvvPW1j-sOelgXHhWp6PVuRxrAaViFn9q15vkuVRd638j078DdfGixqclMZQx6SWUd9rsFqX3sDfCrJvq1QCli0I9HQ_wXaf1fP2JveDiVH5ND8ssLDV-vU57hx-JpwAxE9JoSD11Lo6kAM3LIvWaH9Ooxr9cYTG1a6Oec8x_Bge28mu2mASqsqULeMBR-AB2Jcq7GPLa-TDeWxsYmUKWtIfAmgVUYJQJwhuJ91dKuNTJkz9XXJ-fTd6ENMO-lKZ_nQoY84xHOwC1qPcIau8cq41IgPOo3j227zkcRT4e7cr3SEDYhEqJu3B3Y74xFXMmT5L39r4TThhyV7QzO_cbqA-GPOC7a4hb0zUDcsPBrQJx2kRyoBiDxAw9fIWu3ujsRntbb4Cb5IPhRcpCSQoW5y2avQiS60RzN5WIGny63ZtLchrYfkoPIVphBbjYcF6J_S8aVXW8xbBBxZN31AoIuRGd3FnhOPEZ9sC7hL2-W0fR0XXbzc-iF4M3kimFtD38Rokys6IIBYNOwV6D8weu5dkMspwCbzEJERYfizRoRGg4INvThS3yrYR4mW_vLJSiVj-1iGCOabZrF4jdUo3QYw5YTH449WTFNL5VYMcbzLHVp6vWMo5k3L0XMCVZ5Df-m38z52dpbCEG1MryA.bxKuXXYyNx3mUZSlxaV60Q"
csvfile = 'test.csv'

missonlist = pd.read_csv(csvfile, usecols=[1],encoding='gbk')
missonlist = np.array(missonlist)
missonlist = missonlist.tolist()
missonlist.reverse()

failedlist = pd.read_excel('failedresult.xlsx', usecols=[0])
failedlist = np.array(failedlist)
failedlist = failedlist.tolist()

chatbot = Chatbot({"session_token": token}, conversation_id=None, parent_id=None)
response = chatbot.ask('你好', conversation_id=None, parent_id=None)
for i in missonlist:
    try:
        response = chatbot.ask(i[0], conversation_id=response['conversation_id'], parent_id=response['parent_id']) # You can specify custom conversation and parent ids. Otherwise it uses the saved conversation (yes. conversations are automatically saved)
    except tls_client.exceptions.TLSClientExeption:
        chatbot.reset_chat()
        response = chatbot.ask('你好', conversation_id=None, parent_id=None)
        continue
    print('\n\n\n\n\n')
    for i2 in failedlist:
        if i2[0] in response['message']:
            print('不合格的结果')
            print('')
            output = 0
            break
        else:output = 1
    print(i[0])
    print('')
    print(response['message'])
    if output == 1:
        filename = 'output//' + i[0] + '.txt'
        with open(filename , 'w' ,encoding = 'utf-8') as f:
            f.write(response['message'])
    time.sleep(180)
    #chatbot.reset_chat()
