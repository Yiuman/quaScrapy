from scrapy import cmdline

name = 'qua'
cmd = 'scrapy crawl {0}'.format(name)
cmdline.execute(cmd.split())
