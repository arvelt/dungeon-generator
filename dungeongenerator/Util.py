# -*- coding: UTF-8 -*-
class Util(object):

    @staticmethod
    def is_colliding_square(ax, ay, bx, by, cx, cy, dx, dy):
        # abとcdという四角形として
        # cdがののab右にある、cdがabの左にある、cdがabの下にある、cdがabの上にある
        if bx < cx or dx < ax or by < cy or dy < ay:
            # 衝突していない
            return False
        else:
            return True
