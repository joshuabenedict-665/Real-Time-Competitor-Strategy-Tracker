# price_predictor.py
def run_model(scraped_list):
    # Simple heuristic model: predicted = scraped * 0.95 (round)
    output = []
    for item in scraped_list:
        scraped = item.get("price")
        if scraped is None:
            pred = None
        else:
            pred = round(scraped * 0.95)
        output.append({"name": item.get("name"), "predicted_price": pred})
    return output
