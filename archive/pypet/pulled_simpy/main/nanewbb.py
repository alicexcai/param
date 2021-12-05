#!/usr/bin/env python
# python auction.py --perms 1 --iters 2 --reserve=40 --seed 1 Truthful,5

import sys

from gsp import GSP
from util import argmax_index

class NANewbb:
    """Balanced bidding agent"""
    def __init__(self, id, value, budget):
        self.id = id
        self.value = value
        self.budget = budget

    def initial_bid(self, reserve):
        return self.value / 2


    def slot_info(self, t, history, reserve):
        """Compute the following for each slot, assuming that everyone else
        keeps their bids constant from the previous rounds.

        Returns list of tuples [(slot_id, min_bid, max_bid)], where
        min_bid is the bid needed to tie the other-agent bid for that slot
        in the last round.  If slot_id = 0, max_bid is 2* min_bid.
        Otherwise, it's the next highest min_bid (so bidding between min_bid
        and max_bid would result in ending up in that slot)
        """
        
        prev_round = history.round(t-1)
        other_bids = [a_id_b for a_id_b in prev_round.bids if a_id_b[0] != self.id]

        clicks = prev_round.clicks
        def compute(s):
            (min, max) = GSP.bid_range_for_slot(s, clicks, reserve, other_bids)
            if max == None:
                max = 2 * min
            return (s, min, max)
            
        info = list(map(compute, list(range(len(clicks)))))
#        sys.stdout.write("slot info: %s\n" % info)
        return info


    def expected_utils(self, t, history, reserve):
        """
        Figure out the expected utility of bidding such that we win each
        slot, assuming that everyone else keeps their bids constant from
        the previous round.

        # Utility is: pos_i(value_per_click - bid_per_click_of_below)
        returns a list of utilities per slot.
        """
        # What we need to do:
        #   Take each slot, figure out what we need to bid to win that slot, and then calculate the utility.
        # print(f"{t} {history.round(t-1).clicks}")
        
        # Heads up, when we clean this up, I'm pretty sure we can delete this position-effects line, we're not using it anymore.

        # position_effects = [history.round(t-1).clicks[i]/sum(history.round(t-1).clicks) for i in range(0,len(history.round(t-1).clicks))]
        # position_effects = []
        # for i in range(0,len(history.round(t-1).clicks)):
        #     position_effects.append(len(history.round(t-1).clicks[i])/sum(history.round(t-1).clicks))
        # print("position effects", position_effects)

        # TODO: Fill this in
        # print("help", self.value)
        # print("help2", history.round(t-1).bids[1])
        #utilities = [(self.value - history.round(t-1).bids[i+1][1]) * position_effects[i] for i in range(0, len(position_effects)-1)] 
        slot_info = self.slot_info(t, history, reserve)
        print("slot info", slot_info)
        utilities = [(self.value - slot_info[i][1]) * history.round(t-1).clicks[i] for i in range(len(slot_info))] 
        # utilities =[]
        # for i in range(0, len(position_effects)-1):
        #     print("calculate", self.value - history.round(t-1).bids[i+1] * position_effects[i])
        #     utilities.append(self.value - history.round(t-1).bids[i+1] * position_effects[i])
        
        print("utilities", utilities)

        self.utilities = utilities
        
        return utilities

    def target_slot(self, t, history, reserve):
        """Figure out the best slot to target, assuming that everyone else
        keeps their bids constant from the previous rounds.

        Returns (slot_id, min_bid, max_bid), where min_bid is the bid needed to tie
        the other-agent bid for that slot in the last round.  If slot_id = 0,
        max_bid is min_bid * 2
        """
        i =  argmax_index(self.expected_utils(t, history, reserve))
        info = self.slot_info(t, history, reserve)
        return info[i]

    def bid(self, t, history, reserve):
        # The Balanced bidding strategy (BB) is the strategy for a player j that, given
        # bids b_{-j},
        # - targets the slot s*_j which maximizes his utility, that is,
        # s*_j = argmax_s {clicks_s (v_j - t_s(j))}.
        # - chooses his bid b' for the next round so as to
        # satisfy the following equation:
        # clicks_{s*_j} (v_j - t_{s*_j}(j)) = clicks_{s*_j-1}(v_j - b')
        # (p_x is the price/click in slot x)
        # If s*_j is the top slot, bid the value v_j
        utils = self.expected_utils(t,history,reserve)
        print("slot info", len(self.slot_info(t, history, reserve)))
        target_slot = utils.index(max(utils))
        print("target slot", target_slot)


        prev_round = history.round(t-1)
        (slot, min_bid, max_bid) = self.target_slot(t, history, reserve)

        if utils[target_slot] < 0 or target_slot == 0:
            bid = self.value
        else:
            print("targetslot", target_slot - 1)
            bid = self.value - float((max(utils)))/float((prev_round.clicks[target_slot - 1]))

        print("bid", bid)
        
        return bid

    def __repr__(self):
        return "%s(id=%d, value=%d)" % (
            self.__class__.__name__, self.id, self.value)


