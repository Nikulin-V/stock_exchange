let lots = Object()

lots.get = function (fn=null) {
    if (fn)
        lots.getFn = fn
    else
        lots.getFn = null
    socket.emit('getLots', {'user': user.username})
}

socket.on('getLots', function (data) {
    lots.marketplace_lots = data['marketplace_lots']
    lots.user_lots = data['user_lots']
    if (lots.getFn)
        lots.getFn()
})

lots.return = function (company=null,
                        shares=0,
                        price=0,
                        fn = null) {
    data = {
        'company': company,
        'shares': shares,
        'price': price
    }
    if (fn)
        lots.returnFn = fn
    else
        lots.returnFn = null
    socket.emit('returnLot', data)
}

socket.on('returnLot', function (data) {
    renderPage()
    if (lots.returnFn)
        lots.returnFn()
})
