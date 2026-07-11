import typer
from bot import BinanceFuturesClient

app = typer.Typer()


API_KEY = "aFJpyKIBwNvJHv6RUWYDVmDWmyXx1M5C13y0mqEy9sPCuUJBvQQh862fgjgIYzbd" 
API_SECRET = "fBrr8IWpnymedamrShfj8LnpQktKKuGrqtdAvreIWVSSMRr6XKeW3S3OZ7CkZc19"

@app.command()
def order(
    symbol: str = typer.Option(..., help="e.g. BTCUSDT"),
    side: str = typer.Option(..., help="BUY or SELL"),
    order_type: str = typer.Option(..., help="MARKET or LIMIT"),
    quantity: float = typer.Option(..., help="Quantity"),
    price: float = typer.Option(None, help="Price for LIMIT")
):
    if side.upper() not in ["BUY", "SELL"] or order_type.upper() not in ["MARKET", "LIMIT"]:
        typer.echo("Invalid Input")
        raise typer.Exit()
    if order_type.upper() == "LIMIT" and price is None:
        typer.echo("Price required for LIMIT")
        raise typer.Exit()

    client = BinanceFuturesClient(api_key=API_KEY, api_secret=API_SECRET)
    client.place_order(symbol=symbol, side=side, order_type=order_type, quantity=quantity, price=price)

if __name__ == "__main__":
    app()
