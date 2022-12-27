from Test_data.Filter_Check_data.function import Function



def test_gym_fitness_centre(browser):
    new = Function(browser)
    new.common("/chicago/illinois/united-states/price-0,3500/furnished", "Gym / Fitness Centres", "Price", page_range=2)




