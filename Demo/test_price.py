from Test_data.Filter_Check_data.function import Function


def test_price_0_1000(browser):
    new = Function(browser)
    new.common("/philadelphia/pennsylvania/united-states/price-0,1000", type_of="Price")
