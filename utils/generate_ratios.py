def generate_profit_ratios(max_ratio):
    """
    Generate profit ratios up to X:max_ratio, inclusive.

    Args:
        max_ratio (int): The maximum value for the numerator or denominator.

    Returns:
        list: A list of profit ratio pairs [buy_ratio, sell_ratio].
    """
    profit_ratios = []
    for denominator in range(1, max_ratio + 1):
        for numerator in range(denominator, max_ratio + 1):  # Start at 'denominator' for inclusivity
            ratio = [round(numerator / 100, 2), round(denominator / 100, 2)]
            profit_ratios.append(ratio)
    return profit_ratios
