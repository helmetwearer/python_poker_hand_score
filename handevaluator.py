# probably needs a better library than randrange... or at least one that's not public and can't be predicted by super 1337 peoples
from random import randrange
# 5 * last score + 1 = next level score. Made a decimal and rankings for Straight Flush through Highcard (9 - 1) are the main weight
#Cuz in poker, if you have tied hand ranks, the highest point totals in your cards break the tie
#Scoring system makes 5 kings 1 less than an ace, since that's how poker scores your cards (AA-22-3  beats KK-QQ-A for example)
#Hand scoring and smart hand checking works way better than lookup tables for combinations 7 cards and greater
HIGHCARD_SCORES = [1, 6, 31, 156, 781, 3906, 19531,97656,488281, 2441406,12207031,61035156,305175781]
 
CARD_ORDER_DESCENDING = ['A','K','Q','J','10','9','8','7','6','5','4','3','2', 'A']
def get_deck():
    return [
        ['A','S', 'Ace of Spades',305175781],
        ['K','S', 'King of Spades', 61035156],
        ['Q','S', 'Queen of Spades', 12207031],
        ['J','S', 'Jack of Spades', 2441406],
        ['10','S', 'Ten of Spades', 488281],
        ['9','S', 'Nine of Spades', 97656],
        ['8','S', 'Eight of Spades', 19531],
        ['7','S', 'Seven of Spades', 3906],
        ['6','S', 'Six of Spades', 781],
        ['5','S', 'Five of Spades', 156],
        ['4','S', 'Four of Spades',31],
        ['3','S', 'Three of Spades', 6],
        ['2','S', 'Two of Spades', 1],
        ['A','D', 'Ace of Diamonds', 305175781],
        ['K','D', 'King of Diamonds',  61035156],
        ['Q','D', 'Queen of Diamonds',  12207031],
        ['J','D', 'Jack of Diamonds', 2441406],
        ['10','D', 'Ten of Diamonds', 488281],
        ['9','D', 'Nine of Diamonds', 97656],
        ['8','D', 'Eight of Diamonds', 19531],
        ['7','D', 'Seven of Diamonds', 3906],
        ['6','D', 'Six of Diamonds', 781],
        ['5','D', 'Five of Diamonds', 156],
        ['4','D', 'Four of Diamonds', 31],
        ['3','D', 'Three of Diamonds', 6],
        ['2','D', 'Two of Diamonds', 1], 
        ['A','C', 'Ace of Clubs', 305175781],
        ['K','C', 'King of Clubs', 61035156],
        ['Q','C', 'Queen of Clubs', 12207031],
        ['J','C', 'Jack of Clubs', 2441406],
        ['10','C', 'Ten of Clubs', 488281],
        ['9','C', 'Nine of Clubs', 97656],
        ['8','C', 'Eight of Clubs', 19531],
        ['7','C', 'Seven of Clubs', 3906],
        ['6','C', 'Six of Clubs', 781],
        ['5','C', 'Five of Clubs', 156],
        ['4','C', 'Four of Clubs', 31],
        ['3','C', 'Three of Clubs', 6],
        ['2','C', 'Two of Clubs', 1],
        ['A','H', 'Ace of Hearts', 305175781],
        ['K','H', 'King of Hearts',  61035156],
        ['Q','H', 'Queen of Hearts',  12207031],
        ['J','H', 'Jack of Hearts', 2441406],
        ['10','H', 'Ten of Hearts', 488281],
        ['9','H', 'Nine of Hearts', 97656],
        ['8','H', 'Eight of Hearts', 19531],
        ['7','H', 'Seven of Hearts', 3906],
        ['6','H', 'Six of Hearts', 781],
        ['5','H', 'Five of Hearts', 156],
        ['4','H', 'Four of Hearts', 31],
        ['3','H', 'Three of Hearts', 6],
        ['2','H', 'Two of Hearts', 1]
    ]


def get_hand(deck, size=5):
    hand = []
    for i in range(0,size):
        hand.append(deck.pop(randrange(0,len(deck))))
    return hand


### THAR BE DRAGONS... LOTTA ASININE STUFF TO SAVE LOOPS IN THE NAME OF PROCESSOR SPEED AND SOME CODING LAZINESS
def rank_hand(hand):
    #since we're sharing loops need some booleans
    is_straight_flush = is_quads = is_fullhouse = is_flush = is_straight = is_trips = is_two_pair = is_pair = did_ace = False
    
    #different lists for different hands to track
    straight_flush_hand_return = quads_hand_return = full_house_hand_return = flush_hand_return = straight_hand_return = trips_hand_return = two_pair_hand_return = pair_hand_return = []
    
    #initialize some maps we use
    flush_map = {'H':[],'S':[],'D':[], 'C':[]}
    order_map = {'2':[],'3':[],'4':[],'5':[],'6':[],'7':[],'8':[],'9':[],'10':[],'J':[],'Q':[],'K':[],'A':[]}
    
    for card in hand:
        order_map[card[0]].append(card)
        flush_map[card[1]].append(card)
        try:
            flush_map[card[1]+card[0]].append(card)
        except:
            # would probably be faster to pre-create the whole map but laaazzzyyyy
            flush_map[card[1]+card[0]] = [card]
            
    #save extra looping and do straightflush and flush together since they share the same mechanics
    for suit in ['H','S','D','C']:
        if len(flush_map[suit]) >= 5:
            f_counter = 0
            sf_counter = 0
            for rank in CARD_ORDER_DESCENDING:
                if suit+rank in flush_map:
                    sf_counter += 1
                    f_counter += 1
                    if not is_flush:
                        flush_hand_return.append(flush_map[suit+rank][0])
                    if not is_straight_flush:
                        straight_flush_hand_return.append(flush_map[suit+rank][0])
                elif not is_straight_flush:
                    straight_flush_hand_return = []
                    sf_counter = 0
                if f_counter >= 5:
                    is_flush = True
                if sf_counter >= 5:
                    is_straight_flush = True
    # save extra looping mechanisms and do quad/trips/pair/twopair/straight in the same since they share mechanics
    for rank in CARD_ORDER_DESCENDING:
        if not (rank == 'A' and did_ace):
            did_ace = True 
            if not is_quads and len(order_map[rank]) >= 4:
                is_quads = True
                for card in order_map[rank]:
                    quads_hand_return.append(card)
                for rank2 in CARD_ORDER_DESCENDING:
                    if len(order_map[rank2]) >= 1 and rank2 != rank:
                        quads_hand_return.append(order_map[rank2][0])
                        break
            if not is_trips and len(order_map[rank] )== 3:
                is_trips = True
                for card in order_map[rank]:
                    trips_hand_return.append(card)
                trip_offcard_counter = 0
                for rank2 in CARD_ORDER_DESCENDING:
                    if len(order_map[rank2]) == 1 and rank2 != rank:
                        trips_hand_return.append(order_map[rank2][0])
                        trip_offcard_counter += 1
                        if trip_offcard_counter == 2:
                            break
                    if len(order_map[rank2]) > 1 and rank2 != rank and trip_offcard_counter == 1:
                        trips_hand_return.append(order_map[rank2][1])
                        break
            if not is_pair and len(order_map[rank]) == 2:
                is_pair = True
                for card in order_map[rank]:
                    pair_hand_return.append(card)
                pair_offcard_counter = 0
                for rank2 in CARD_ORDER_DESCENDING:
                    if len(order_map[rank2]) == 1 and rank2 != rank:
                        pair_hand_return.append(order_map[rank2][0])
                        pair_offcard_counter += 1
                        if pair_offcard_counter == 3:
                            break
                    if len(order_map[rank2]) > 1 and rank2 != rank and (pair_offcard_counter == 1 or pair_offcard_counter == 2):
                        pair_hand_return.append(order_map[rank2][1])
                        pair_offcard_counter += 1
                        if pair_offcard_counter == 3:
                            break        
                    if len(order_map[rank2]) > 2 and rank2 != rank and (pair_offcard_counter == 2):
                        pair_hand_return.append(order_map[rank2][2])
                        pair_offcard_counter += 1
                        if pair_offcard_counter == 3:
                            break
            elif not is_two_pair and len(order_map[rank]) == 2:
                is_two_pair = True
                for card in [pair_hand_return[0],pair_hand_return[1],order_map[rank][0],order_map[rank][1]]:
                    two_pair_hand_return.append(card)
                for rank2 in CARD_ORDER_DESCENDING:
                    if len(order_map[rank2]) >= 1 and rank2 != rank and pair_hand_return[0][0] != rank2:
                        two_pair_hand_return.append(order_map[rank2][0])
                        break
        if not is_straight:
            if len(order_map[rank]) >= 1:
                straight_hand_return.append(order_map[rank][0])
                if len(straight_hand_return) >= 5:
                    is_straight = True
            else:
                straight_hand_return = []
    
    #this seems bad m'kay... again lazy
    if is_straight_flush:
        return [9 + hand_raw_score(straight_flush_hand_return), straight_flush_hand_return, 'Straight Flush']
    if is_quads:
        return [8 + hand_raw_score(quads_hand_return), quads_hand_return, 'Quads']
    if is_trips and is_pair:
        rethand = [trips_hand_return[0],trips_hand_return[1],trips_hand_return[2],pair_hand_return[0],pair_hand_return[1]]
        return [7 + hand_raw_score(rethand),rethand, 'Full House']
    if is_flush:
        return [6 + hand_raw_score(flush_hand_return), flush_hand_return, 'Flush']
    if is_straight:
        return [5 + hand_raw_score(straight_hand_return), straight_hand_return, 'Straight']
    if is_trips:
        return [4+ hand_raw_score(trips_hand_return), trips_hand_return, 'Three of a Kind']
    if is_two_pair:
        return [3+ hand_raw_score(two_pair_hand_return), two_pair_hand_return, 'Two Pair']
    if is_pair:
        return [2+ hand_raw_score(pair_hand_return), pair_hand_return, 'A Pair']
    #you aint get nothin do a highcard
    rethand = []
    for rank in CARD_ORDER_DESCENDING:
        if len(order_map[rank]) > 0:
            rethand.append(order_map[rank][0])
        if len(rethand) >= 5:
            return [1+ hand_raw_score(rethand), rethand, 'Highcard']
        
    # if it reaches here... you probably didn't have five cards... or you successfully divided by zero or something
    return None


def hand_raw_score(hand):
    score = 0
    for card in hand:
        score += card[3]
    # if ace plays low in straight subtract ace value... the wheel is only special case that matters here
    if score == 305175975:
        score -= 305175781
    #make a decimal so rank magnitude matters more
    score = score / float(10000000000)
    return score

#reading arrays of arrays is hard
def hand_to_string(hand):
    arr = []
    for card in hand:
        arr.append(card[2])
    return str(arr)

for i in range(0,10):
    counter = 0
    while counter < 999999:
        counter += 1
        hand = get_hand(get_deck(),size=5)
        score, winning_hand, name = rank_hand(hand)
        if name == 'Straight Flush':
            print 'for hand:' + hand_to_string(hand)
            print 'best_hand is ' + name + ' with a score of ' + str(score) + '        ' + hand_to_string(winning_hand)
            print counter
            break
