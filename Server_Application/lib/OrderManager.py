import os

class OrderManager:

    def startMenu(self):
        try:
            clear = lambda: os.system('cls')    # Clearing the cmd prompt for Windows
            clear()
        except:
            clear = lambda: os.system('clear')  # Clearing the cmd prompt for Linux
        print('\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n')
        print(' *******************************************\n')
        print('    Enter how many time you want to pick    ')
        print('    an item from the given carriers.        ')
        print('\n *******************************************\n\n')
        print('    When you are satisfied with the order') 
        print('    simply press "d"                          \n\n')

    def itemSelection(self):
        carrierID = [1, 2, 3, 4, 5]
        carPick = [0, 0, 0, 0, 0]
        run = True
        while run:
            runTemp = ""
            for x in range(0, len(carrierID)):
                stringTemp = ""

                itemTemp = input('     Items from Carrier ' + str(carrierID[x]) + ': ')
                try:
                    intTemp = '0'
                    intTemp = int(itemTemp)
                    carPick[x] = itemTemp
                except:
                    stringTemp = str(itemTemp)
                    print('     Items from Carrier ' + str(carrierID[x]) + ': 0')

                if stringTemp == "d":
                    conf = ""
                    print('\n\n    Your current order is as follows: \n')
                    for x in range(0, len(carrierID)):
                        print('     Items from Carrier ' + str(carrierID[x]) + ': ' + str(carPick[x]))
                        
                    conf = input('\n    Confirm that you want to place the order (y/n) ')
                    if conf == "y":
                        run = False
                        break
            
            if run:
                runTemp = input('\n    Do you wish to change your order? (y/n) ')
                if runTemp != "y":
                    run = False

        return carPick

    def formatOrder(self, pickCar):
        encodeStr = ""
        for x in range(0, len(pickCar)):
            encodeStr += str(pickCar[x])
            if x < len(pickCar) - 1:
                encodeStr += ':'

        return encodeStr

