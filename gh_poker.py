#! /usr/env python

# poker.py
# 2017, polarysekt


from random import shuffle

STRLST_POKER_SUIT_CHR = [ "s", "h", "c", "d" ]
STRLST_POKER_SUIT_STR = [ "spades", "hearts", "clubs", "diamonds" ]
STRLST_POKER_SUIT_SYM = [ ]
STRLST_POKER_SUIT_HTM = [ "&spades;", "&hearts;", "&clubs;", "&diams;" ]

STRLST_POKER_VALUE_CHR = [ "A", "2", "3", "4", "5", "6", "7", "8", "9", "T", "J", "Q", "K" ]
STRLST_POKER_VALUE_CH2 = [ "A", "2", "3", "4", "5", "6", "7", "8", "9", "10", "J", "Q", "K" ]
STRLST_POKER_VALUE_STR = [ "ace", "two", "three", "four", "five", "six", "seven", "eight", "nine", "ten", "jack", "queen", "king" ]

class Deck:
        
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
            self.cards.append( i )

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
            self.player.append( [ -1, -1 ] )
        #self.player = [ [] ]
        self.community = []
        self.muck = []
        
        self.log.append( "SHUFFLE" )
        self.deck.shuffle()
        
        
        for h in range(2):
            if h == 0:
                self.log.append( "DEAL FIRST HOLE CARD" )
            else:
                self.log.append( "DEAL SECOND HOLE CARD" )
            
            self.log.append( "BURN" )
            self.burn()
        
            for p in range(self.numplayers):
                self.log.append( "DEAL 1 to P" + str(p) )
                self.player[p][h]= self.deck.deal()
        
        self.log.append( "BURN" )
        self.burn()
        
        self.log.append( "SHOW FLOP" )
        for c in range(3):
            self.community.append( self.deck.deal() )
            
        for c in range(2):
            self.log.append( "BURN")
            self.burn()
            if c == 0:
                self.log.append( "DEAL TURN" )
            else:
                self.log.append( "DEAL RIVER" )
            self.community.append( self.deck.deal() )
        self.log.append( "TODO :: hand determination" )
        self.log.append( "Game Over" )
        
    def burn(self):
        self.muck.append( self.deck.deal() )

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
    

# return simple 5 card hand
def getHand():
    deck = Deck()
    deck.shuffle()
    
    retHand = []
    for i in range(5):
        retHand.append( deck.deal )
        
    return retHand

def getHandHTML():
    hand = getHand()
    retString = ""
    for ind in range(2):
        i = hand[ind]
        retString += '<span class="ghPokerCard">'
        s = getCardSuit(i)
        if s % 2 != 0:
            retString += '<span class="cardRed">'
        retString += str(getCardValue( i ))
        retString += getCardSuitHTML( i )
        if s % 2 != 0:
            retString += '</span>'
        retString += "</span> "
    retString += '<div class="ghPokerTable">'
    for ind in range(2,7):
        i = hand[ind]
        retString += '<span class="ghPokerCard">'
        s = getCardSuit(i)
        if s % 2 != 0:
            retString += '<span class="cardRed">'
        retString += str(getCardValue( i ))
        retString += getCardSuitHTML( i )
        if s % 2 != 0:
            retString += '</span>'
        retString += "</span> "
    retString += '</div>'
    return retString

def get_hand_html( hand ):
    retString = ""
    for c in range(len(hand)):
        s = get_card_suit_i( hand[c] )
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
        retString += get_card_full_ht( hand[c] )
        retString += '</div>'
            
    return retString

def get_hand_ch( hand ):
    retString = ""
    for c in range(len(hand)):
        retString += get_card_full_ch( hand[c] )
        if c < len(hand)-1:
            retString += " "
            
    return retString
    

def get_card_value_i( val ):
    if val < 52 and val >= 0:
        return val % 13
    else:
        return -1

def get_card_suit_i( val ):
    if val < 52 and val >= 0:
        return int(val / 13)
    else:
        return -1

def get_card_value_ch( val ):
    if val < 52 and val >= 0:
        return STRLST_POKER_VALUE_CHR[ get_card_value_i( val) ]
    else:
        return None

def get_card_suit_ch( val ):
    if val < 52 and val >= 0:
        return STRLST_POKER_SUIT_CHR[ get_card_suit_i( val) ]
    else:
        return None

def get_card_full_ch( val ):
    if val < 52 and val >= 0:
        return get_card_value_ch( val ) + get_card_suit_ch( val )
    else:
        return None

def get_card_value_ht( val ):
    if val < 52 and val >= 0:
        return STRLST_POKER_VALUE_CHR[ get_card_value_i( val) ]
    else:
        return None

def get_card_suit_ht( val ):
    if val < 52 and val >= 0:
        return STRLST_POKER_SUIT_HTM[ get_card_suit_i( val) ]
    else:
        return None
    
def get_card_full_ht( val ):
    if val < 52 and val >= 0:
        return get_card_value_ht( val ) + get_card_suit_ht( val )
    else:
        return None

def get_demo( numplayers ):
    strStringReturn = ""

    print( numplayers)
    if True:
        if numplayers > 0 and numplayers < 11:
            
            #strGameTitle = ""
            #strGameTitle = '<h3>' +str(numplayers)+" Player"
            #if numplayers is not 1:
            #    strGameTitle += "s"
            #strGameTitle += "</h3>"
            #strStringReturn += strGameTitle
            
            holdem = Holdem( numplayers )
            holdem.deal_all( )
        
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
                strStringReturn += "Player " + str(p) + ": " + get_hand_ch( holdem.get_hole(p) ) + "\n"

            strStringReturn += "Community: " + get_hand_ch( holdem.get_community() ) + "\n"
            strStringReturn += '</textarea>'
            strStringReturn += "</div>"

            # Hand Breakdown
            strStringReturn += "<div>"
            strStringReturn += '<div class="talabel">TODO</div>'
            strStringReturn += '<textarea id="textTODO">'
            strStringReturn += '</textarea>'
            strStringReturn += "</div>"

            strStringReturn += "</div>"

    return strStringReturn

def test_units():
    #hand = getHand()
    #getCardValue( hand[0] );
    #getCardSuit( hand[0] )
    
    #print( getHandHTML() )
    for a in range(1,11):
        strGameTitle = '<h3>Game #'+str(a)+" | "+str(a)+" Player"
        if a is not 1:
            strGameTitle += "s"
        strGameTitle += "</h3>"
        print( strGameTitle )
        
        holdem = Holdem( a )
        holdem.deal_all( )
        
        #strPlayer = ""
        #strCommunity = ""
    
        print( '<div class="playergame">')
        for p in range(holdem.numplayers):
            print('<div class="pokerplayer">')
            #strPlayer = '<span class="playerlabel">' + "Player " + str(p) + "</span>" + get_hand_html( holdem.get_hole(p) )
            #print(strPlayer)
            print('<span class="playerlabel">' + "P" + str(p) + "</span>" + get_hand_html( holdem.get_hole(p) ))
            print('</div>')
        print( '</div>' )

        print('<div class="pokercommunity">')
        #strCommunity = '<span class="communitylabel">Community:</span>' + get_hand_html( holdem.get_community() )
        #print( strCommunity )
        print('<span class="communitylabel">Community:</span>' + get_hand_html( holdem.get_community() ))
        print('</div>')


        print( '<div class="infoz">' )
        # TEXT SUMMARY
        print( '<div class="talabel">Summary</div>')
        #print( '<input type="textarea" id="textSummary" value="' )
        print( '<textarea id="textSummary">' )
        for p in range(holdem.numplayers):
            #strPlayer = "Player " + str(p) + ": " + get_hand_ch( holdem.get_hole(p) )
            #print(strPlayer)
            print( "Player " + str(p) + ": " + get_hand_ch( holdem.get_hole(p) ))

        #strCommunity = "Community: " + get_hand_ch( holdem.get_community() )
        #print( strCommunity )
        print("Community: " + get_hand_ch( holdem.get_community() ))
        #print( '"></input>' )
        print( '</textarea>' )

        
        # TODO game log
        print( '<div class="talabel">Log</div>')
        print( '<textarea id="textLog">' )
        print( holdem.get_log_str() )
        print( '</textarea>' )
        
        print( '</div>' )
        
        if a < 10:
            print( "<hr/>")
    
    return True


def getCardValue( card ):
    return g_ghPOKER_VALUES[card % 13]

def getCardSuit( card ):
	return int(card/13)

def getCardSuitHTML( card ):
    return g_ghPOKER_SUITS[getCardSuit(card)]


def main():
    test_units()

if __name__ == "__main__":
    main()

# vim:expandtab:ts=4:sw=4
