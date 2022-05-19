from core.socketio import sio, get_socket_user
from marketplace.models import Shares, Lot


@sio.on('getShares')
def getShares(sid, data):
    event_name = 'getShares'

    user = get_socket_user(sid)
    user_shares = Shares.shares.filter(
        user=user
    ).all()

    data = {
        'shares': [
            {
                'count': s.count,
                'company': s.company.name,
                'industry': s.company.industry.name
            }
            for s in user_shares
        ]
    }

    sio.emit(event_name, data)


@sio.on('getLots')
def getLots(sid, data):
    event_name = 'getLots'

    user = get_socket_user(sid)

    data = {
        'user_lots': [
            {
                'count': lot.count,
                'price': lot.price,
                'company': lot.company.name,
            }
            for lot in Lot.lots.get_user_lots(user)
        ],
        'marketplace_lots': [
            {
                'count': lot.count,
                'price': lot.price,
                'company': lot.company.name,
                'user': lot.user.username
            }
            for lot in Lot.lots.get_marketplace_lots(user)
        ]
    }

    sio.emit(event_name, data)
