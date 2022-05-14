let shares = Object()

shares.get = function (fn=null) {
    if (fn)
        shares.getFn = fn
    else
        shares.getFn = null
    socket.emit('getShares', {'user': user.username})
}

socket.on('getShares', function (data) {
    shares.shares = data['shares']
    if (shares.getFn)
        shares.getFn()
})