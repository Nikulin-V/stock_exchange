from companies.models import Company
from core.socketio import get_socket_user, sio
from marketplace.models import Lot, Shares


@sio.on('getShares')
def getShares(*args):
    sid, data = args
    event_name = 'getShares'

    user = get_socket_user(sid)
    user_shares = Shares.shares.filter(user=user).all()

    data = {
        'shares': [
            {
                'count': s.count,
                'company': s.company.name,
                'industry': s.company.industry.name,
            }
            for s in user_shares
        ]
    }

    sio.emit(event_name, data, to=sid)


@sio.on('getLots')
def getLots(*args):
    sid, data = args
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
                'user': lot.user.username,
            }
            for lot in Lot.lots.get_marketplace_lots(user)
        ],
    }

    sio.emit(event_name, data, to=sid)


@sio.on('returnLot')
def returnLot(sid, data):
    event_name = 'returnLot'

    user = get_socket_user(sid)
    company = Company.companies.get(name=data['company'])
    shares = int(data['shares'])
    price = float(data['price'])

    Lot.lots.get(user=user, company=company, count=shares, price=price).delete()

    user_shares = Shares.shares.filter(user=user, company=company)

    if user_shares:
        user_shares[0].count += shares
        user_shares[0].save()
    else:
        Shares.shares.create(user=user, company=company, count=shares)

    data = {'message': 'Success'}

    sio.emit(event_name, data, to=sid)
