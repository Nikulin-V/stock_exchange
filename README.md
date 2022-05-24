# Stock exchange
Этот сервис позволяет вам познакомиться с основами фондового рынка. В частности, с торговлей акциями. Сервис использует **Python&nbsp;3.9**, сделан на фреймворке для веб-приложений **Django**.
> Проект проверялся только на `Python 3.9`, с другими версиями могут возникать ошибки

Здесь вы можете создавать компании или ОАО и управлять ими, выпускать новые акции и продавать их на торговой площадке, увеличивая баланс на своём счёте. Помните: чем больше доверия, тем больше прибыль компании, тем больше стоят её акции на торговой площадке.
Прежде чем начать - прочитайте правила. Мы старались сделать их максимально интересными.

## Правила торговли на фондовой бирже

Термины и сокращения:

- 🚶 - Игрок фондовой биржи
- 🛒 - Торговая площадка
- 💸 - Внутриигровая валюта
- Компания - внутриигровая организация
- Акция - внутриигровая акция компании
- Константа - постоянная величина, заданная администратором

Порядок игры:

1. Зарегистрируйтесь как 🚶. При регистрации вы получите свои первые 💸.

2. В целях получения прибыли Вы можете открыть компанию в разделе "Компании". Чтобы открыть компанию, Вам надо будет заплатить взнос, который является Константой. После открытия компании у Вас появится определенное количество акций, которое является Константой.

3. Вы можете выставить свои акции на продажу на 🛒. При продаже акций Вы указываете цену за 1 акцию, количество акций и выбираете компанию, акции которой хотите продать.

4. На 🛒 Вы можете покупать или продавать акции компаний других путём нажатия на строку в таблице акций как на 🛒 , так и в профиле. При покупке акций Вы выбираете компанию, акции которой хотите купить, и количество акций. При покупке Вам автоматически предложат купить самые дешевые акции выбранной компании. Откроется окно с подтверждением покупки.

5. При покупке акций на торговой площадке всем акционерам компании (кроме Покупателя и Продавца), акции которой участвуют в сделке выплачивается комиссия в зависимости от количества акций в их собственности. Комиссия за 1 акцию в % является Константой.

6. Помимо покупки и продажи акций на 🛒 можно снять акции с продажи.

7. Компании приносят прибыль раз в определённое количество времени (Константа). Прибыль на каждую индустрию - Константа. Прибыль распределяется между компаниями одной индустрии в зависимости от очков доверия <sub>(п. 8)</sub>

8. Доверие к компаниям задаётся 🚶. Каждый 🚶 распределяет 100 очков доверия между компаниями каждой из отраслей. Добавить очки доверия к компаниям, в которой 🚶 является акционером нельзя.

9. В том случае, если 🚶 не распределил часть очков доверия, то они распределяются поровну между компаниями, в которых 🚶 не является акционером.

10. Удачной игры. Ни кризиса, ни инфляции!
