from core.socketio import sio
from marketplace.models import Shares
from users.models import CustomUser


@sio.on('getShares')
def getShares(sid, data):
    event_name = 'getShares'

    user = CustomUser.objects.filter(username=data['user']).all()[0]
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
