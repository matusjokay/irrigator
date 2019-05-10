import serial
import RPi.GPIO as GPIO
import time
import syslog
from flask import Flask, render_template, request
import datetime
app = Flask(__name__)

vlhkost_pody1 = 65
vlhkost_pody2 = 66

dazdovy_senzor = 67

vlhkost_vzduchu = 68
teplota_vzduchu = 69

senzor_teploty1 = 70
senzor_teploty2 = 71

barometricky_tlak = 72
intezita_svetla = 73

ard = serial.Serial('/dev/ttyS0', 9600 , timeout=1)

@app.route('/')
def hello():
    while True:

        now = datetime.datetime.now()
        timeString = now.strftime("%Y-%m-%d %H:%M")

        print ("Raspberry Pi chce vediet aka je vlhkost pody ")
        vlhkostA = bytes((vlhkost_pody1,))
        vlhkostB = bytes((vlhkost_pody2,))
     #   print(vlhkostA, vlhkostB)
        wr = ard.write(vlhkostA)
        wr = ard.write(vlhkostB)

        print ("Message from arduino: ")
        msgA = ard.read(3)
        msgB = ard.read(3)
        # print (msgA , msgB)
        time.sleep(4)

        if msgA:
            i_msgA=int(msgA);
            print(i_msgA)
        if msgB:
            i_msgB=int(msgB);
            print(i_msgB)

        if (i_msgA < 25 and i_msgB < 25):
            print("vlhkost pody je velmi nizka, SPUSTI ZAVLAHU")

        print ("Raspberry Pi chce vediet ci prsi")
        dazdovyC = bytes((dazdovy_senzor,))
        # print(dazdovyC)
        wr = ard.write(dazdovyC)

        print ("Message from arduino: ")
        msgC = ard.readline()
        # print (msgC )
        time.sleep(4)

        if msgC:
            i_msgC=float(msgC);

        if (i_msgC < 2):
            i_msgCC ="PRSI";
            print(i_msgCC)
        else:
            i_msgCC = "NEPRSI";
            print(i_msgCC)

        print ("Raspberry Pi chce vediet co je vo vzduchu")
        vlhkost_vzdD = bytes((vlhkost_vzduchu,))
        teplota_vzdE = bytes((teplota_vzduchu,))
        # print(vlhkost_vzdD, teplota_vzdE)
        wr = ard.write(vlhkost_vzdD)
        wr = ard.write(teplota_vzdE)

        print ("Message from arduino: ")
        msgD = ard.read(5)
        msgE = ard.read(5)
        # print (msgD , msgE)
        time.sleep(4)

        if msgD:
            i_msgD=float(msgD);
            print(i_msgD)
        if msgE:
            i_msgE=float(msgE);
            print(i_msgE)

        if (i_msgD < 25.0):
            print("vlhkost vzduchu je velmi nizka, VYVETRAJ VZDUCH")
        if (i_msgE < 5.0):
            print("teplota vzduchu je velmi nizka, ZOHREJ VZDUCH")

        print ("Raspberry Pi chce vediet aka je teplota pody ")
        teplotaF = bytes((senzor_teploty1,))
        teplotaG = bytes((senzor_teploty2,))
        # print(teplotaF, teplotaG)
        wr = ard.write(teplotaF)
        wr = ard.write(teplotaG)

        print ("Message from arduino: ")
        msgF = ard.readline()
        msgG = ard.readline()
        # print (msgF , msgG)
        time.sleep(4)

        if msgF:
            i_msgF=float(msgF);
            print(i_msgF)
        if msgG:
            i_msgG=float(msgG);
            print(i_msgG)

        if (i_msgF < 5.0 and i_msgG < 5.0):
            print("teplota vzduchu je velmi nizka, ZOHREJ SKLENIK")

        print ("Raspberry Pi chce vediet aky je barometricky tlak ")
        tlakH = bytes((barometricky_tlak,))
        # print(tlakH)
        wr = ard.write(tlakH)

        print ("Message from arduino: ")
        msgH = ard.readline()
       #  print (msgH )
        time.sleep(4)

        if msgH:
            i_msgH=float(msgH);
            print(i_msgH)

        if (i_msgH < 950.0):
            print("tlak je velmi nizky, ODPADNES")

        print ("Raspberry Pi chce vediet aka je intenzita svetla ")
        svetloI = bytes((intezita_svetla,))
        # print(svetloI)
        wr = ard.write(svetloI)

        print ("Message from arduino: ")
        msgI = ard.readline()
       #  print (msgI)
        time.sleep(4)

        if msgI:
            i_msgI=float(msgI);
            print(i_msgI)

        if (i_msgI < 15.0):
            print("intezita svetla je velmi nizka, OSVETLI SKLENIK")

        templateData = {
            'title' : 'HELLO!',
            'time': timeString,
            'i_msgA' : i_msgA,
            'i_msgB' : i_msgB,
            'i_msgC' : i_msgCC,
            'i_msgD' : i_msgD,
            'i_msgE' : i_msgE,
            'i_msgF' : i_msgF,
            'i_msgG' : i_msgG,
            'i_msgH' : i_msgH,
            'i_msgI' : i_msgI
        }
        return render_template('index.html', **templateData)


if __name__ == '__main__':
    app.jinja_env.auto_reload = True
    app.config['TEMPLATES_AUTO_RELOAD'] = True
    app.run(debug = True)

