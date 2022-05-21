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

function renderBalance(elementSelector='#balance') {
    $(elementSelector).html(Math.round(user.balance * 100) / 100)
}

function renderShares(elementSelector='#shares') {
    if (shares.shares.length === 0) {
        $(elementSelector).html(
            `
            <p class="mt-3">
                В вашем портфеле акций пусто. Приобрести акции можно на
                <a href="/marketplace">торговой площадке</a>.
            </p>
            `
        )
    } else {
        let rows = ``
        for (let shareId = 0; shareId < shares.shares.length; shareId++) {
            let {company, count, industry} = Object(shares.shares[shareId])
            rows += `
                <tr onclick="window.location.href = '/marketplace/sell-shares?' +
                                    'company=${company}&' + 
                                    'shares=${count}'">
                    <td>${industry}</td>
                    <td>
                        <a class="company-link"
                           href="/companies/${company}">
                            ${company}
                        </a>
                    </td>
                    <td>${count}</td>
                </tr>
            `
        }
        $(elementSelector).html(
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