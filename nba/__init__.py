import click
import nba


@click.command()
@click.option('--item', default="box")
@click.option('--year', default=2015)
def parser(item, year):

    nbaScraper = nba.NBA()
    if item == "box":
        return nbaScraper.getAllSeasonBoxes(year)
    elif item == "pbp":
        return nbaScraper.getAllSeasonPBPs(year)
    else:
        click.echo("Not a valid item, try pbp (play by plays) or box (box scores)")
