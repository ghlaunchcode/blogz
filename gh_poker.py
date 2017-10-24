"""Provides gh_poker routines"""

# poker.py
# 2017, polarysekt


from random import shuffle

ghDEBUG = False#True
ghDEBUG2 = True
ghDEBUG3 = False #trip
ghDEBUG4 = False #pair

STRLST_POKER_SUIT_CHR = ["s", "h", "c", "d"]
STRLST_POKER_SUIT_STR = ["spades", "hearts", "clubs", "diamonds"]
STRLST_POKER_SUIT_SYM = []
STRLST_POKER_SUIT_HTM = ["&spades;", "&hearts;", "&clubs;", "&diams;"]

STRLST_POKER_VALUE_CHR = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K"]
STRLST_POKER_VALUE_CH2 = ["A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K"]
STRLST_POKER_VALUE_STR = ["ace", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "jack", "queen", "king"]


STRLST_POKER_HAND = [ "high card", "pair", "two pair", "three of a kind", "straight", "flush", "full house", "four of a kind", "straight flush" ]


def check_flush( cards ):
    #check flush
    runningSuit = -1
    for c in cards:
        if runningSuit < 0:
            runningSuit = get_card_suit_i(c)
        else:
            if get_card_suit_i(c) == runningSuit:
                pass
            else:
                return False
        
    return True
    
def check_straight( cards ):
    if len(cards) < 5:
        return False
    
    #check straight
    
    pos = -1
    
    #TODO!
    #sort list
    reflist = []
    
    for a in range(5):
        reflist.append( get_card_value_i( cards[a] ))
    
    checklist = sorted(reflist)
    #dont judge me
    #for iter in range(5):
        #for c in range(len(cards)):
            #pos = 0
            #for i in range(len(cards)):
                #if get_card_value_i(cards[c]) > get_card_value_i(cards[i]):
                    #pos = i
            #tmp = cards[pos]
            #cards[pos] = cards[c]
            #for n in range(pos):
                #swt = cards[pos-n]
                #if( n < pos-1 ):
                    #cards[pos-n] = tmp
                    #tmp = swt

        
    
    #ace high
    #TODO
    
    #ace low
    
    #if ghDEBUG2:
        #print( "check_straight:", str(get_card_value_i(cards[4]) - get_card_value_i(cards[0])) )
        #print( get_hand_ch( cards ) )
    
    if get_card_value_i(checklist[4]) - get_card_value_i(checklist[0]) == 4:
        # pair gives false positive
        if check_pair( cards ) or check_trips( cards ) or check_twopair(cards): # or check_fok( cards ):
            return False;
        if ghDEBUG2:
            print( "STRAIGHT: [", get_hand_ch( cards ), "] (", checklist, ")" )
        #TODO
        return True;
    
    return False

def check_fok( cards ):
    if len(cards) < 4:
        return False
    
    runningMatch = -1
    countMatch = 0
    altMatch = -1
    countAlt = 0
    
    for c in cards:
        if runningMatch < 0:
            runningMatch = get_card_value_i(c)
            countMatch = 1
        else:
            if get_card_value_i(c) == runningMatch:
                countMatch += 1
            else:
                if altMatch < 0:
                    altMatch = get_card_value_i(c)
                else:
                    if get_card_value_i(c) == altMatch:
                        countAlt += 1
                    else:
                        return False
                    
    if countMatch == 4 or countAlt == 4:
        return True
    
    return False
    
def check_full( cards ):
    if len(cards) < 5:
        return False;

    runningMatch = -1
    runningAlt = -1
    runningLast = -1
    
    countMatch =0
    countAlt = 0
    countLast = 0
    
    for c in cards:
        if runningMatch < 0:
            runningMatch = get_card_value_i(c)
            countMatch = 1
        else:
            if get_card_value_i(c) == runningMatch:
                countMatch += 1
            else:
                if runningAlt < 0:
                    runningAlt = get_card_value_i(c)
                    countAlt = 1
                else:
                    if get_card_value_i(c) == runningAlt:
                        countAlt += 1
                    else:
                        if runningLast < 0:
                            runningLast = get_card_value_i(c)
                            countLast = 1
                        else:
                            if get_card_value_i == runningLast:
                                countLast += 1
                            else:
                                return False

    if countMatch == 3:
        if countAlt == 2 or countLast == 2:
            if ghDEBUG3:
                print( "full ret:",countMatch,countAlt,countLast)
                print( "hand:",get_hand_ch(cards) )
            return True
    if countAlt == 3:
        if countMatch == 2 or countLast == 2:
            if ghDEBUG3:
                print( "full ret:",countMatch,countAlt,countLast)
                print( "hand:",get_hand_ch(cards) )
            return True
    if countLast == 3:
        if countMatch == 2 or countAlt == 2:
            if ghDEBUG3:
                print( "full ret:",countMatch,countAlt,countLast)
                print( "hand:",get_hand_ch(cards) )
            return True
        
    return False


def check_trips( cards ):
    if len(cards) < 3:
        return False
    
    runningMatch = -1
    runningAlt = -1
    runningLast = -1
    
    countMatch =0
    countAlt = 0
    countLast = 0
    
    for c in cards:
        if runningMatch < 0:
            runningMatch = get_card_value_i(c)
            countMatch = 1
        else:
            if get_card_value_i(c) == runningMatch:
                countMatch += 1
            else:
                if runningAlt < 0:
                    runningAlt = get_card_value_i(c)
                    countAlt = 1
                else:
                    if get_card_value_i(c) == runningAlt:
                        countAlt += 1
                    else:
                        if runningLast < 0:
                            runningLast = get_card_value_i(c)
                            countLast = 1
                        else:
                            if get_card_value_i == runningLast:
                                countLast += 1
                            else:
                                return False
    
    if countMatch == 3 or countAlt == 3 or countLast == 3:
        if ghDEBUG3:
            print( "trips ret:",countMatch,countAlt,countLast)
            print( "hand:",get_hand_ch(cards) )
        return True
    
    return False

def check_twopair( cards ):
    if len(cards) < 4:
        return False
    
    runningMatch = -1
    runningAltA = -1
    runningAltB = -1
    runningLast = -1
    countMatch = 0
    countAltA = 0
    countAltB = 0
    countLast = 0
    
    for c in cards:
        if runningMatch < 0:
            runningMatch = get_card_value_i(c)
            countMatch = 1
        else:
            if get_card_value_i(c) == runningMatch:
                countMatch += 1
            else:
                if runningAltA < 0:
                    runningAltA = get_card_value_i(c)
                    countAltA = 1
                else:
                    if get_card_value_i(c) == runningAltA:
                        countAltA += 1
                    else:
                        if runningAltB < 0:
                            runningAltB = get_card_value_i(c)
                            countAltB = 1
                        else:
                            if get_card_value_i(c) == runningAltB:
                                countAltB += 1
                            else:
                                if runningLast < 0:
                                    runningLast = get_card_value_i(c)
                                    countLast = 1
                                else:
                                    if get_card_value_i(c) == runningLast:
                                        countLast += 1
                                    else:
                                        return False
                                    
    if countMatch == 2:
        if countAltA == 2 or countAltB == 2 or countLast == 2:
            if ghDEBUG4:
                print( "two pair ret:",countMatch,countAltA,countAltB,countLast)
                print( "hand:",get_hand_ch(cards) )
            return True
    if countAltA == 2:
        if countAltB == 2 or countLast == 2:
            if ghDEBUG4:
                print( "two pair ret:",countMatch,countAltA,countAltB,countLast)
                print( "hand:",get_hand_ch(cards) )
            return True

    if countAltB == 2:
        if countLast == 2:
            if ghDEBUG4:
                print( "two pair ret:",countMatch,countAltA,countAltB,countLast)
                print( "hand:",get_hand_ch(cards) )
            return True

    
    return False
    

def check_pair( cards ):
    if len(cards) < 2:
        return False
    
    runningMatch = -1
    runningAltA = -1
    runningAltB = -1
    runningLast = -1
    countMatch = 0
    countAltA = 0
    countAltB = 0
    countLast = 0
    
    for c in cards:
        if runningMatch < 0:
            runningMatch = get_card_value_i(c)
            countMatch = 1
        else:
            if get_card_value_i(c) == runningMatch:
                countMatch += 1
            else:
                if runningAltA < 0:
                    runningAltA = get_card_value_i(c)
                    countAltA = 1
                else:
                    if get_card_value_i(c) == runningAltA:
                        countAltA += 1
                    else:
                        if runningAltB < 0:
                            runningAltB = get_card_value_i(c)
                            countAltB = 1
                        else:
                            if get_card_value_i(c) == runningAltB:
                                countAltB += 1
                            else:
                                if runningLast < 0:
                                    runningLast = get_card_value_i(c)
                                    countLast = 1
                                else:
                                    if get_card_value_i(c) == runningLast:
                                        countLast += 1
                                    else:
                                        return False
                                    
    if countMatch == 2 or countAltA == 2 or countAltB == 2 or countLast == 2:
        if ghDEBUG4:
            print( "pair ret:",countMatch,countAltA,countAltB,countLast)
            print( "hand:",get_hand_ch(cards) )
        return True
    
    return False



def get_hand_value( cards ):
    # expect 5 or less card hands?
    
    iValue = 0
    isFlush = False
    isStraigh = False
    isFok = False
    isFull = False
    isTP = False

    isFlush = check_flush( cards )
    isStraight = check_straight( cards )
    
    #special case Straight Flush
    if isFlush and isStraight:
        return 8
    
    isFok = check_fok( cards )
    
    if isFok:
        return 7;

    #TODO special case Full
    #isFull = False
    if check_full( cards ):
        return 6

    if isFlush:
        return 5
    
    if isStraight:
        return 4

    if check_trips( cards ):
        return 3

    if check_twopair(cards):
        return 2
    
    if check_pair( cards ):
        return 1
    
    return 0
    

def get_best_hand( cards ):
    test_hand = []
    save_hand = []
    countCards = len( cards )
    high_hand = -1

    if countCards < 5:
        for i in range( countCards ):
            test_hand.append( cards[i] )
        return get_hand_value( test_hand )

    #grab first 5	
    for i in range(5):
        test_hand.append( cards[i] )
    
    if countCards == 5:
        return get_hand_value( test_hand )
    
    for c in range(5):
        save_hand.append( test_hand[c] )
    #loop pic 5's
    for i in range(5):
        # switch first, second, third, fourth, fifth for each > 5
        for s in range(countCards - 5):
            for c in range( 5 ):
                test_hand[c] = save_hand[c]
            test_hand[i] = cards[countCards - s - 1]
            if ghDEBUG:
                print( "save hand:", get_hand_ch(save_hand) )
                print( str( countCards -s))
                print( "switch hand:", get_hand_ch(test_hand) )
            v = get_hand_value( test_hand )
            if v > high_hand:
                high_hand = v
    
    return high_hand



class Deck:
    """Provides Deck object"""

    def deal(self):
        if self.index < 52:
            ret = self.cards[self.index]
            self.index += 1
            return ret
        else:
            return -1

    def shuffle(self):
        shuffle(self.cards)
        self.index = 0

    def remain(self):
        return 51 - self.index

    def __init__(self):
        self.index = 0
        self.cards = []
        for i in range(52):
            self.cards.append(i)

class Holdem:

    def player_count(self):
        return self.numplayers

    def get_log(self):
        return self.log

    def get_log_str(self):
        retStr = ""
        for i in self.log:
            retStr += i
            retStr += "\n"
        return retStr

    def deal_all(self):
        self.log = []
        for p in range(self.numplayers):
            self.player.append([-1, -1])
        #self.player = [ [] ]
        self.community = []
        self.muck = []
        
        self.log.append("SHUFFLE")
        self.deck.shuffle()
        
        
        for h in range(2):
            if h == 0:
                self.log.append("DEAL FIRST HOLE CARD")
            else:
                self.log.append("DEAL SECOND HOLE CARD")
            
            self.log.append("BURN")
            self.burn()
        
            for p in range(self.numplayers):
                self.log.append("DEAL 1 to P" + str(p))
                self.player[p][h]= self.deck.deal()
        
        self.log.append("BURN")
        self.burn()
        
        self.log.append("SHOW FLOP")
        for c in range(3):
            self.community.append( self.deck.deal() )
            
        for c in range(2):
            self.log.append("BURN")
            self.burn()
            if c == 0:
                self.log.append("DEAL TURN")
            else:
                self.log.append("DEAL RIVER")
            self.community.append( self.deck.deal() )
        self.log.append("TODO :: hand determination")
        self.log.append("Game Over")
        
    def burn(self):
        self.muck.append(self.deck.deal())

    def get_community(self):
        return self.community

    def get_hole(self, playerid):
        if playerid < self.numplayers and playerid >= 0:
            return self.player[playerid]
        else:
            return None

    def __init__(self, numplayers):
        if numplayers > 0:
            if numplayers < 11:
                self.numplayers = numplayers
            else:
                self.numplayers = 10
        else:
            self.numplayers = 1
        
        self.player = []
        self.deck = Deck()
        self.muck = []
        self.log = []

def get_hand_html(hand):
    retString = ""
    for c in range(len(hand)):
        s = get_card_suit_i(hand[c])
        if s % 2 == 0:
            #retString += '<span class="pokercard_black">'
            retString += '<div class="pokercard_black' #">'
        else:
            #retString += '<span class="pokercard_red">'
            retString += '<div class="pokercard_red' #">'

        if c > 0 and len(hand) < 3:
            retString += ' cardoverlap">'
        else:
            retString += '">'
        retString += get_card_full_ht(hand[c])
        retString += '</div>'
            
    return retString

def get_hand_ch(hand):
    retString = ""
    for c in range(len(hand)):
        retString += get_card_full_ch(hand[c])
        if c < len(hand)-1:
            retString += " "
            
    return retString
    

def get_card_value_i(val):
    if val < 52 and val >= 0:
        return val % 13
    else:
        return -1

def get_card_suit_i(val):
    if val < 52 and val >= 0:
        return int(val / 13)
    else:
        return -1

def get_card_value_ch(val):
    if val < 52 and val >= 0:
        return STRLST_POKER_VALUE_CHR[get_card_value_i(val)]
    else:
        return None

def get_card_suit_ch(val):
    if val < 52 and val >= 0:
        return STRLST_POKER_SUIT_CHR[get_card_suit_i(val)]
    else:
        return None

def get_card_full_ch(val):
    if val < 52 and val >= 0:
        return get_card_value_ch(val) + get_card_suit_ch(val)
    else:
        return None

def get_card_value_ht(val):
    if val < 52 and val >= 0:
        return STRLST_POKER_VALUE_CHR[get_card_value_i(val)]
    else:
        return None

def get_card_suit_ht(val):
    if val < 52 and val >= 0:
        return STRLST_POKER_SUIT_HTM[get_card_suit_i(val)]
    else:
        return None
    
def get_card_full_ht(val):
    if val < 52 and val >= 0:
        return get_card_value_ht(val) + get_card_suit_ht(val)
    else:
        return None

def get_demo(numplayers):
    strStringReturn = ""

    #print(numplayers)
    if True:
        if numplayers > 0 and numplayers < 11:
            
            #strGameTitle = ""
            #strGameTitle = '<h3>' +str(numplayers)+" Player"
            #if numplayers is not 1:
            #    strGameTitle += "s"
            #strGameTitle += "</h3>"
            #strStringReturn += strGameTitle
            
            holdem = Holdem(numplayers)
            holdem.deal_all()
        
            strStringReturn += '<div class="playergame">'
            for p in range(holdem.numplayers):
                strStringReturn += '<div class="pokerplayer">'
                strStringReturn += '<span class="playerlabel">' + "P" + str(p) + "</span>" + get_hand_html( holdem.get_hole(p) )
                strStringReturn += '</div>'
            strStringReturn += '</div>'

            strStringReturn += '<div class="communitylabel">Community:</div>'
            strStringReturn += '<div class="pokercommunity">' + get_hand_html( holdem.get_community() )
            strStringReturn += '</div>'

            strStringReturn += '<div class="infoz">'
            
            # game log
            strStringReturn += '<div>'
            strStringReturn += '<div class="talabel">Log</div>'
            strStringReturn += '<textarea id="textLog">'
            strStringReturn += holdem.get_log_str()
            strStringReturn += '</textarea>'
            strStringReturn += '</div>'

            # TEXT SUMMARY
            strStringReturn += "<div>"
            strStringReturn += '<div class="talabel">Summary</div>'
            strStringReturn += '<textarea id="textSummary">'
            for p in range(holdem.numplayers):
                strStringReturn += "Player " + str(p) + ": " + get_hand_ch(holdem.get_hole(p) ) + "\n"

            strStringReturn += "Community: " + get_hand_ch(holdem.get_community()) + "\n"
            strStringReturn += '</textarea>'
            strStringReturn += "</div>"

            # Hand Breakdown
            strStringReturn += "<div>"
            strStringReturn += '<div class="talabel">Hand Value</div>'
            strStringReturn += '<textarea id="textTODO">'
            #print( strStringReturn )
            #strStringReturn = ""
            # get best hands:
            for p in range(holdem.numplayers):
                strStringReturn += "Player " + str(p) + ": " + STRLST_POKER_HAND[get_best_hand( holdem.get_hole(p) + holdem.get_community())]+ "\n"
            
            
            strStringReturn += '</textarea>'
            strStringReturn += "</div>"

            strStringReturn += "</div>"

    return strStringReturn

def test_units():
    #hand = getHand()
    #getCardValue( hand[0] );
    #getCardSuit( hand[0] )
    
    #print( getHandHTML() )
#    for a in range(1):
#        strGameTitle = '<h3>Game #'+str(a)+"</h3>"
#        print( strGameTitle )
    print(get_demo(10))
    #if a < 10:
    #print("<hr/>")
    
    return True

def main():
    test_units()

if __name__ == "__main__":
    main()

# vim:expandtab:ts=4:sw=4
