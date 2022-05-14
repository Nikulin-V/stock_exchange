clicked = false
renderPage()
setInterval(renderPage, 5000)

function renderPage() {
    if (!clicked)
        renderElements()
}

function renderElements() {
    user.get(renderBalance)
    shares.get(renderShares)
}

function renderBalance() {
    $('#balance').html(Math.round(user.balance * 100) / 100)
}

function renderShares() {
    if (shares.shares.length === 0) {
        $('#shares').html(
            `<p class="mt-3">Акций нет</p>`
        )
    } else {
        let rows = ``
        for (shareId = 0; shareId < shares.shares.length; shareId++) {
            let share = Object(shares.shares[shareId])
            rows += `
                <tr>
                    <td>${share.industry}</td>
                    <td>${share.company}</td>
                    <td>${share.count }</td>
                </tr>
            `
        }
        $('#shares').html(
            `<table class="table table-hover text-center">
                        <caption class="caption-top">Список акций, принадлежащих вам</caption>
                        <thead class="table-dark">
                        <tr>
                            <td class="col-4">Сфера деятельности</td>
                            <td class="col-5">Название компании</td>
                            <td class="col-3">Количество акций</td>
                        </tr>
                        </thead>
                        ${rows}
                    </table>`
        )
    }
}