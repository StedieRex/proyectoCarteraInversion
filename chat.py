import pandas as pd
import random
import os
import math

def get_current_directory():
    return os.path.dirname(os.path.abspath(__file__))

def change_working_directory():
    os.chdir(get_current_directory())

def calculate_individual_return(asset_array):
    return sum(asset_array) / len(asset_array)

def calculate_portfolio_return(asset_a_return, asset_b_return, weight_a, weight_b):
    return (weight_a * asset_a_return) + (weight_b * asset_b_return)

def calculate_portfolio_risk(asset_a, asset_b, asset_a_return, asset_b_return, weight_a, weight_b):
    variance_a = sum((x - asset_a_return) ** 2 for x in asset_a) / (len(asset_a) - 1)
    variance_b = sum((x - asset_b_return) ** 2 for x in asset_b) / (len(asset_b) - 1)
    covariance_ab = sum(((x - asset_a_return) * (y - asset_b_return)) for x, y in zip(asset_a, asset_b)) / (len(asset_a) - 1)
    return math.sqrt((weight_a ** 2) * variance_a + (weight_b ** 2) * variance_b + 2 * weight_a * weight_b * covariance_ab)

def compare_portfolios(portfolio, existing_portfolios):
    for existing_portfolio in existing_portfolios:
        if set(portfolio[:2]) == set(existing_portfolio[:2]):
            return False
    return True

def create_portfolios(df):
    num_portfolios = 10
    portfolios = []
    while num_portfolios > 0:
        portfolio = random.sample(df.columns[1:], 2)
        if compare_portfolios(portfolio, portfolios):
            portfolios.append(portfolio)
            num_portfolios -= 1
    return portfolios

def roulette_selection(best_portfolios):
    roulette = []
    for portfolio in best_portfolios:
        for _ in range(int(portfolio[4])):
            roulette.append(portfolio)
    return random.sample(roulette, 7)

def crossover(best_portfolios, selected_portfolios):
    new_generation = []
    for _ in range(5):
        for best_portfolio in best_portfolios:
            asset_a, asset_b = best_portfolio[:2]
            if best_portfolio[2] > best_portfolio[3]:
                new_generation.append([asset_b if asset_a in portfolio else asset_a for portfolio in selected_portfolios])
            else:
                new_generation.append([asset_a if asset_b in portfolio else asset_b for portfolio in selected_portfolios])
    return new_generation

def format_portfolios(portfolios):
    formatted_portfolios = []
    for i in range(0, len(portfolios), 2):
        if compare_portfolios(portfolios[i:i+2], formatted_portfolios):
            formatted_portfolios.append(portfolios[i:i+2])
    return formatted_portfolios

def main():
    change_working_directory()
    df = pd.read_csv('data/preciosCierreEmpresas.csv')
    portfolios = create_portfolios(df)

    balanced_portfolios = []
    for portfolio in portfolios:
        asset_a_array = df[portfolio[0]].values
        asset_b_array = df[portfolio[1]].values
        asset_a_return = calculate_individual_return(asset_a_array)
        asset_b_return = calculate_individual_return(asset_b_array)
        portfolio_return = calculate_portfolio_return(asset_a_return, asset_b_return, 0.5, 0.5)
        portfolio_risk = calculate_portfolio_risk(asset_a_array, asset_b_array, asset_a_return, asset_b_return, 0.5, 0.5)
        rf = portfolio_return / portfolio_risk
        balanced_portfolios.append(portfolio + [0.5, 0.5, rf])

    selected_portfolios = roulette_selection(balanced_portfolios)

    best_portfolios = sorted(selected_portfolios, key=lambda x: x[4], reverse=True)[:2]
    new_generation = crossover(best_portfolios, selected_portfolios)
    formatted_new_generation = format_portfolios(new_generation)

    print("Best Portfolios:")
    for portfolio in best_portfolios:
        print(portfolio)
    print("\nNew Generation:")
    for portfolio in formatted_new_generation:
        print(portfolio)

if __name__ == "__main__":
    main()
