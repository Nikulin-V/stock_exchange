let price = $('#id_price').val()
let cost = $('#cost')
let fee = parseFloat($('#fee').html())

$('#id_shares').on('input',function () {
    if (!isNaN(parseInt($(this).val())) && parseInt($(this).val()) > 0) {
        cost.html(Math.round(parseFloat(price) * parseInt($(this).val()) * (1 + fee / 100) * 100) / 100)
    }
    else cost.html('—')
})