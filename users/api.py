from datetime import timedelta

from core.socketio import get_socket_user, sio
from django.db.models import Sum
from django.utils import timezone
from marketplace.models import Shares
from rating.models import Rating
from stock_exchange.game_config import EARNING, EARNING_TIME_SECONDS

last_time = timezone.now()


def income(multiplier):
    data = Rating.rating.get_companies_rating_dict()
    for key in data:
        for company, percentage in data[key].items():
            if company == 'total_points':
                continue
            company_profit = percentage * multiplier * EARNING / 100
            count_count = (
                Shares.shares.select_related('company')
                .filter(company__name=company)
                .aggregate(amount=Sum('count'))['amount']
            )

            stockholders = (
                Shares.shares.select_related("company")
                .filter(company__name=company)
                .select_related("user")
            )
            for stockholder in stockholders:
                user = stockholder.user
                user.balance += stockholder.count / count_count * company_profit
                user.save()


@sio.on('getUser')
def getUser(*args):
    sid, data = args
    event_name = 'getUser'

    global last_time
    if (timezone.now() - last_time).seconds >= EARNING_TIME_SECONDS:
        multiplier = (timezone.now() - last_time).seconds // EARNING_TIME_SECONDS
        last_time = timezone.now() + timedelta(
            seconds=((timezone.now() - last_time).seconds % EARNING_TIME_SECONDS)
        )
        income(multiplier)

    user = get_socket_user(sid)

    data = {
        'username': user.username,
        'first_name': user.first_name,
        'last_name': user.last_name,
        'email': user.email,
        'balance': user.balance,
    }

    sio.emit(event_name, data, to=sid)
