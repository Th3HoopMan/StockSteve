import discord
import logging
import yfinance as yf
from discord.ext import commands
import os
from coinbase.wallet.client import Client



token = os.getenv("DISCORD_BOT_TOKEN")

logging.basicConfig(level=logging.INFO)

client = discord.Client()

bot = commands.Bot(command_prefix='!')

coinbase_key = os.getenv("COINBASE_API_KEY")
coinbase_secret = os.getenv("COINBASE_API_SECRET")

coinbase_client = Client(coinbase_key, coinbase_secret)



translation = {
    "regularMarketPrice": "The current price is: ",
    "open": "The open price was: ",
    "regularMarketPreviousClose": "The previous close price was: ",
    "regularMarketOpen": "The regular market open price was: ",
    "volume24Hr": "The volume from the last 24hrs is: ",
    "regularMarketDayHigh": "The regular market day high is: ",
    "regularMarketPreviousClose": "The regular market previous close was: ",
    "openInterest": "The open interest is: ",
    "marketCap": "The market is: ",
    "averageVolume": "The average volume is: ",
    "dayLow": "The regular market day low is: ",
    "ytdReturn": "The YTD return is: ",
    "volume": "The volume for this stock is: ",
    "fiftyTwoWeekHigh": "The 52-week high is: ",
    "fiftyTwoWeekLow": "The 52-week low is: ",
    "dayHigh": "The day high is: ",
    "shortName": "The short name is: ",
    "longName": "The long name is: ",
    "52WeekChange": "The 52-week change is: ",
    "sharesOutstanding": "The shares outstanding are: ",
    "sharesShort": "The number of shares shorted is: ",
    "sharesPercentSharesOut": "The percent of shares out is: ",
    "shortRatio": "The short ratio is: ",
    "threeYearAverageReturn": "The 3 year average return is: ",
    "dateShortInterest": "The the short interest is: ",
    "sharesShortPriorMonth": "The the number of shares short last month was: ",
    "impliedSharesOutstanding": "The the implied shares outstanding is: ",
    "fiveYearAverageReturn": "The 5 year average return is: ",
    "revenueGrowth": "The revenue growth is: ",
    "earningsGrowth": "The earnings growth is is: ",
    "totalCash": "The total cash is: ",
    "totalDebt": "The total debt is: ",
    "totalRevenue": "The total revenue is: "
}

def getStockData(action, stockInfo):
    if action in stockInfo.keys():
        if type(stockInfo[action]) == int or type(stockInfo[action]) == float:
            value = "{:,}".format(stockInfo[action])
        else:
            value = stockInfo[action]
        if stockInfo[action] is None:
            return "I don't have {action} for that particular stock".format(action=action)
        elif action == "longBusinessSummary":
            return stockInfo[action]
        if action in translation.keys():
            return "{translation} [{symbol}] {value}".format(translation=translation[action], symbol=stockInfo["symbol"], value=str(value))
        else:
            return "The {action} for {symbol} is: {value}".format(action=action, symbol=stockInfo["symbol"], value=str(value))
    elif action == "overview":
        return "Stock: {symbol} \nPrice: {price}\nHigh: {high}\nLow: {low}".format(symbol=stockInfo["symbol"], price="{:,}".format(stockInfo["regularMarketPrice"]), high="{:,}".format(stockInfo["dayHigh"]), low="{:,}".format(stockInfo["dayLow"]))
    else:
        return "I don't recognize {action} for this stock.".format(action=action)



def pullStock(symbol, action):
    try:
        if (symbol.startswith("$")):
            logging.info("Pulling stock")
            stock = yf.Ticker(symbol[1:])
        else:
            logging.info("Pulling stock")
            stock = yf.Ticker(symbol)
        logging.info("Pulled stock")
        logging.info(stock.info)
        logging.info("Getting {action} stock data".format(action=action))
        return getStockData(action, stock.info)
    except Exception as e:
        logging.error(e, exc_info=True)
        return "There was an issue finding {action} data for {stock}. Please check your formatting and try again.".format(action=action, stock=symbol) 

def pullCryptoPrice(coin):
    try:
        price = coinbase_client.get_buy_price(currency_pair = '{coin}-USD'.format(coin=coin))
        return "The price of {coin} is: {price}".format(coin=coin, price="{:,}".format(price["amount"]))
    except Exception as e:
        logging.error(e, exc_info=True)
        return "Had an issue pulling price data for {coin}. Please check your formatting and try again." .format(coin=coin)

@bot.command(
    help="Gives the current price of Bitcoin in USD",
    breif="Gives the current price of Bitcoin in USD"
)
async def BTC(ctx):
    await ctx.send(pullCryptoPrice("BTC"))

@bot.command(
    help="Gives the current price of Ethereum in USD",
    breif="Gives the current price of Ethereum in USD"
)
async def ETH(ctx):
    await ctx.send(pullCryptoPrice("ETH"))

@bot.command(
    help="Gives the current price of the coin you specified in USD",
    breif="Gives the current price of the coin you specified in USD"
)
async def crypto(ctx, coin):
    await ctx.send(pullCryptoPrice(coin.upper()))

@bot.command(
    help="Gives the current price, day High, and day Low of the stock",
    breif="Gives the current price along with the day high/low of the stock"
)
async def overview(ctx, stock):
    await ctx.send(pullStock(stock, "overview"))

@bot.command(
    help="Gives a summary on the company",
    breif="Gives a summary on the company"
)
async def summary(ctx, stock):
    await ctx.send(pullStock(stock, "longBusinessSummary"))

@bot.command(
    help="Gives the current regular Market price of the stock",
    breif="Gives the current price of the stock"
)
async def price(ctx, stock):
    await ctx.send(pullStock(stock, "regularMarketPrice"))

@bot.command(
    help="The price the regular market opened at",
    breif="The price the regular market opened at"
)
async def open(ctx, stock):
    await ctx.send(pullStock(stock, "regularMarketOpen"))

@bot.command(
    help="The price the regular market closed at",
    breif="The price the regular market closed at"
)
async def close(ctx, stock):
    await ctx.send(pullStock(stock, "regularMarketPreviousClose"))

@bot.command(
    help="The volume over the past 24 hours",
    breif="The volume over the past 24 hours"
)
async def volume24Hr(ctx, stock):
    await ctx.send(pullStock(stock, "volume24Hr"))

@bot.command(
    help="The day high price",
    breif="The day high price"
)
async def high(ctx, stock):
    await ctx.send(pullStock(stock, "dayHigh"))

@bot.command(
    help="The day low price",
    breif="The day low price"
)
async def low(ctx, stock):
    await ctx.send(pullStock(stock, "dayLow"))

@bot.command(
    help="The volume for the day",
    breif="The volume for the day"
)
async def volume(ctx, stock):
    await ctx.send(pullStock(stock, "volume"))

@bot.command(
    help="The total number of outstanding derivative contracts, such as options or futures that have not been settled",
    breif="The total number of outstanding derivative contracts, such as options or futures that have not been settledy"
)
async def openInterest(ctx, stock):
    await ctx.send(pullStock(stock, "openInterest"))

@bot.command(
    help="The total dollar market value of a company's outstanding shares of stock",
    breif="The total dollar market value of a company's outstanding shares of stock"
)
async def marketCap(ctx, stock):
    await ctx.send(pullStock(stock, "marketCap"))

@bot.command(
    help="The average trade volume",
    breif="The average trade volume"
)
async def avgVolume(ctx, stock):
    await ctx.send(pullStock(stock, "averageVolume"))

@bot.command(
    help="The Year to Date return on the stock",
    breif="The Year to Date return on the stock"
)
async def ytdReturn(ctx, stock):
    await ctx.send(pullStock(stock, "ytdReturn"))

@bot.command(
        help="The 52 Week high",
    breif="The 52 Week high"
)
async def yearHigh(ctx, stock):
    await ctx.send(pullStock(stock, "fiftyTwoWeekHigh"))

@bot.command(
    help="The 52 Week low",
    breif="The 52 Week low"
)
async def yearLow(ctx, stock):
    await ctx.send(pullStock(stock, "fiftyTwoWeekLow"))

@bot.command(
    help="The short name",
    breif="The short name"
)
async def shortName(ctx, stock):
    await ctx.send(pullStock(stock, "shortName"))

@bot.command(
    help="The long name",
    breif="The long name"
)
async def longName(ctx, stock):
    await ctx.send(pullStock(stock, "longName"))

@bot.command(
    help="The 52 Week change",
    breif="The 52 Week change"
)
async def yearChange(ctx, stock):
    await ctx.send(pullStock(stock, "52WeekChange"))

@bot.command(
    help="Stock currently held by all its shareholders",
    breif="Stock currently held by all its shareholders"
)
async def sharesOutstanding(ctx, stock):
    await ctx.send(pullStock(stock, "sharesOutstanding"))

@bot.command(
    help="Number of shares shorted",
    breif="Number of shares shorte"
)
async def sharesShort(ctx, stock):
    await ctx.send(pullStock(stock, "sharesShort"))

@bot.command(
    help="The number of shares short in a stock by the stock's average daily trading volume",
    breif="The number of shares short in a stock by the stock's average daily trading volume"
)
async def shortRatio(ctx, stock):
    await ctx.send(pullStock(stock, "shortRatio"))

@bot.command(
    help="The average return over 3 years",
    breif="The average return over 3 years"
)
async def threeYearAvgReturn(ctx, stock):
    await ctx.send(pullStock(stock, "threeYearAverageReturn"))

@bot.command(
    help="The shares of a company that are currently sold short and not yet covered",
    breif="Shares currently sold short/not covered"
)
async def shortInterest(ctx, stock):
    await ctx.send(pullStock(stock, "dateShortInterest"))

@bot.command(
    help="The number of shares shorted last month",
    breif="The number of shares shorted last month"
)
async def sharesShortPrevMonth(ctx, stock):
    await ctx.send(pullStock(stock, "sharesShortPriorMonth"))

@bot.command(
    help="The 5 year average return",
    breif="The 5 year average return"
)
async def fiveYearAvgReturn(ctx, stock):
    await ctx.send(pullStock(stock, "fiveYearAverageReturn"))

@bot.command(
    help="The revenue growth",
    breif="The revenue growth"
)
async def revenueGrowth(ctx, stock):
    await ctx.send(pullStock(stock, "revenueMonth"))

@bot.command(
    help="The total cash the company has on hand",
    breif="The total cash the company has on handk"
)
async def totalCash(ctx, stock):
    await ctx.send(pullStock(stock, "totalCash"))

@bot.command(
    help="The earnings growth",
    breif="The earnings growt"
)
async def earningsGrowth(ctx, stock):
    await ctx.send(pullStock(stock, "earningsGrowth"))

@bot.command(
    help="The total amount of debt a company has",
    breif="The total amount of debt a company has"
)
async def totalDebt(ctx, stock):
    await ctx.send(pullStock(stock, "totalDebt"))

@bot.command(
    help="The total revenue the company has",
    breif="The total revenue the company has"
)
async def totalRevenue(ctx, stock):
    await ctx.send(pullStock(stock, "totalRevenue"))

@bot.event
async def on_command_error(ctx, error):
    logging.error(error)

# previousClose
# regularMarketOpen
# volume24Hr
# regularMarketDayHigh
# regularMarketPreviousClose
# open
# regularMarketDayLow
# regularMarketVolume
# openInterest
# marketCap
# averageVolume
# dayLow
# ask
# ytdReturn
# volume
# fiftyTwoWeekHigh
# fiftyTwoWeekLow
# bid
# tradeable
# dayHigh
# exchange
# shortName
# longName
# 52WeekChange
# sharesOutstanding
# sharesShort
# sharesPercentSharesOut
# shortRatio
# sharesShortPreviousMonthDate
# threeYearAverageReturn
# dateShortInterest
# sharesShortPriorMonth
# impliedSharesOutstanding
# fiveYearAverageReturn
# revenueGrowth
# currentPrice
# earningsGrowth
# totalCash
# totalDebt
# totalRevenue            

bot.run(token)



    

