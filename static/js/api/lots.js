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