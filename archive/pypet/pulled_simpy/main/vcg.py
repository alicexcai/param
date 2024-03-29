#!/usr/bin/env python

import random

from gsp import GSP


class VCG:
    """
    Implements the Vickrey-Clarke-Groves mechanism for ad auctions.
    """
    @staticmethod
    def compute(slot_clicks, reserve, bids):
        """
        Given info about the setting (clicks for each slot, and reserve price),
        and bids (list of (id, bid) tuples), compute the following:
          allocation:  list of the occupant in each slot
              len(allocation) = min(len(bids), len(slot_clicks))
          per_click_payments: list of payments for each slot
              len(per_click_payments) = len(allocation)

        If any bids are below the reserve price, they are ignored.

        Returns a pair of lists (allocation, per_click_payments):
         - allocation is a list of the ids of the bidders in each slot
            (in order)
         - per_click_payments is the corresponding payments.
        """

        # The allocation is the same as GSP, so we filled that in for you...

        valid = lambda a_bid: a_bid[1] >= reserve
        valid_bids = list(filter(valid, bids))

        # shuffle first to make sure we don't have any bias for lower or
        # higher ids
        random.shuffle(valid_bids)
        valid_bids.sort(key=lambda b: b[1], reverse=True)

        num_slots = len(slot_clicks)
        allocated_bids = valid_bids[:num_slots]
        if len(allocated_bids) == 0:
            return ([], [])

        (allocation, just_bids) = list(zip(*allocated_bids))

        # TODO: You just have to implement this function
        def total_payment(k):
            """
            Total payment for a bidder in slot k.
            """
            c = slot_clicks
            n = len(allocation)
            # payment = 0
            # print("payment", payment)
            # print("reserve", reserve)

            # TODO: Compute the payment and return it.

            if k >= n:
                return 0
            elif k == n - 1:
                return c[k] * valid_bids[k+1][1] if len(valid_bids) > n else c[k] * reserve
            else:
                return (c[k] - c[k+1])*just_bids[k+1] + total_payment(k+1)
            
            # def payment(i):
            #     if i >= n - 1: 
            #         return 0 
            #     else:
            #         return (slot_clicks[i] - slot_clicks[i+1])*just_bids[i+1] + payment(i+1)

            # return payment(k)
            
            # # Begin new code
            # if k >= n:
            #     payment = 0
            # # else:
            # #     payment(v,i) = (slot_clicks[i])
            # #     total_payment(k+1)
                
            # else:
            #     for i in range(k+1,n):
            #         payment += (slot_clicks[i-1] - slot_clicks[i]) * just_bids[i]
            
            
            # print("payment", payment)

            # return payment
            # End new code

        def norm(totals):
            """Normalize total payments by the clicks in each slot"""
            return [x_y[0]/x_y[1] for x_y in zip(totals, slot_clicks)]

        per_click_payments = norm(
            [total_payment(k) for k in range(len(allocation))])

        return (list(allocation), per_click_payments)

    @staticmethod
    def bid_range_for_slot(slot, slot_clicks, reserve, bids):
        """
        Compute the range of bids that would result in the bidder ending up
        in slot, given that the other bidders submit bidders.
        Returns a tuple (min_bid, max_bid).
        If slot == 0, returns None for max_bid, since it's not well defined.
        """
        # Conveniently enough, bid ranges are the same for GSP and VCG:
        return GSP.bid_range_for_slot(slot, slot_clicks, reserve, bids)
