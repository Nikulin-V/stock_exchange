clicked = false
renderPage()
setInterval(renderPage, 5000)

function renderPage() {
    if (!clicked)
        renderElements()
}

function renderElements() {
    user.get(renderBalance)
    lots.get(renderLots)
}

function renderBalance(elementSelector='#balance') {
    $(elementSelector).html(Math.round(user.balance * 100) / 100)
}

function renderLots() {
    renderUserLots()
    renderMarketplaceLots()
}

function renderUserLots(elementSelector='#user-lots') {
    if (lots.user_lots.length === 0) {
        $(elementSelector).html(
            `
            <p>
                У вас нет акций, размещённых на торговой площадке.
                Выставить акции на продажу можно в <a href="/auth/profile">профиле</a>.
            </p>
            `
        )
    } else {
        let rows = ``
        for (let lotId = 0; lotId < lots.user_lots.length; lotId++) {
            let {company, count, price} = Object(lots.user_lots[lotId])
            rows += `
                <tr>
                    <td>${company}</td>
                    <td>${count}</td>
                    <td>${parseFloat(price)}</td>
                </tr>
            `
        }
        $(elementSelector).html(
        `<table class="table table-hover text-center">
                    <caption class="caption-top">Ваши акции, продающиеся на торговой площадке</caption>
                    <thead class="table-dark">
                        <tr>
                            <td class="col-8 text-left">Компания</td>
                            <td class="col-2">Акции</td>
                            <td class="col-2">Цена за акцию</td>
                        </tr>
                    </thead>
                    ${rows}
                </table>`
        )
    }
}

function renderMarketplaceLots(elementSelector='#marketplace-lots') {
    if (lots.marketplace_lots.length === 0) {
        $(elementSelector).html(
            `<p>На данный момент на торговой площадке нет лотов доступных для покупки</p>`
        )
    } else {
        let rows = ``
        for (let lotId = 0; lotId < lots.marketplace_lots.length; lotId++) {
            let {company, count, price, user} = Object(lots.marketplace_lots[lotId])
            rows += `
                <tr>
                    <td>${company}</td>
                    <td>${user}</td>
                    <td>${count}</td>
                    <td>${parseFloat(price)}</td>
                </tr>
            `
        }
        $(elementSelector).html(
        `<table class="table table-hover text-center">
                    <caption class="caption-top">Акции, доступные для приобретения</caption>
                    <thead class="table-dark">
                        <tr>
                            <td class="col-5 text-left">Компания</td>
                            <td class="col-3">Продавец</td>
                            <td class="col-2">Акции</td>
                            <td class="col-2">Цена за акцию</td>
                        </tr>
                    </thead>
                    ${rows}
                </table>`
        )
    }
}