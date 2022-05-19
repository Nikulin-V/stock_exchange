let user = Object()

user.get = function (fn=null) {
    if (fn)
        user.getFn = fn
    else
        user.getFn = null
    socket.emit('getUser', {'user': user.username})
}

socket.on('getUser', function (data) {
    user.username = data['username']
    user.first_name = data['first_name']
    user.last_name = data['last_name']
    user.email = data['email']
    user.balance = parseFloat(data['balance'])
    if (user.getFn)
        user.getFn()
})