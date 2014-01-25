from util import hook, http, text, web
import json
import re

## CONSTANTS

AMAZON_RE = (r"(http.*(www\.)?amazon\.com/[^ ]+)", re.I)

## HOOK FUNCTIONS

@hook.regex(*AMAZON_RE)
def amazon_url(match):
    item = http.get_html(match.group(1))
    title = item.xpath('//title/text()')[0]
    price = item.xpath("//span[@id='priceblock_ourprice']/text()")[0]
    rating = item.xpath("//div[@id='avgRating']/span/text()")[0].strip()

    star_count = round(float(rating.split(' ')[0]),0)
    stars=""
    for x in xrange(0,int(star_count)):
        stars = "%s%s" % (stars,'★')
    for y in xrange(int(star_count),5):
        stars = "%s%s" % (stars,'☆')

    return ('\x02%s\x02 - \x02%s\x02 - \x034%s\x034' % (title, stars, price)).decode('utf-8')


@hook.command('az')
@hook.command
def amazon(inp):
    href = "http://www.amazon.com/s/url=search-alias%3Daps&field-keywords={}".format(inp.replace(" ","%20"))
    results = http.get_html(href)
    # title = results.xpath('//title/text()')[0]
    try:
        title = results.xpath("//div[@id='result_0']/h3/a/span/text()")[0]
        url = results.xpath("//div[@id='result_0']/h3/a/@href")[0]
        price = results.xpath("//div[@id='result_0']//li[@class='newp']/div/a/span/text()")[0]
        rating = results.xpath("//div[@id='result_0']//span[@class='asinReviewsSummary']/a/@alt")[0]
    except:
        title = results.xpath("//div[@id='result_1']/h3/a/span/text()")[0]
        url = results.xpath("//div[@id='result_1']/h3/a/@href")[0]
        price = results.xpath("//div[@id='result_1']//li[@class='newp']/div/a/span/text()")[0]
        rating = results.xpath("//div[@id='result_1']//span[@class='asinReviewsSummary']/a/@alt")[0]

    azid = re.match(r'^.*\/dp\/([\w]+)\/.*',url).group(1)

    star_count = round(float(rating.split(' ')[0]),0)
    stars=""
    for x in xrange(0,int(star_count)):
        stars = "%s%s" % (stars,'★')
    for y in xrange(int(star_count),5):
        stars = "%s%s" % (stars,'☆')

    return ('\x02%s\x02 - %s - \x034%s\x02 - http://amzn.com/%s' % (title, stars, price, azid)).decode('utf-8')