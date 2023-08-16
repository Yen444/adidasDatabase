import re
import urllib.robotparser
import urllib


robots_txt_content = """
# Tue, 30 May 2023 13:43:08 GMT (build: jaas-1456)
# DE

User-agent: *
Disallow: /*laufschuhe*
Disallow: /*sportschuhe*
Disallow: /*andere_sportschuhe*
Disallow: /on/demandware.store/Sites-adidas-DE-Site/de_DE/
Disallow: /search?*
Disallow: /en/search?*
Disallow: /personalizationengine
Disallow: /api/consents/*
Disallow: */account/*
Disallow: /api/profanityList
Disallow: /_bm/_data
Disallow: /api/ugc/models/*
Disallow: /api/pages/plp?path=/no-search-results
Disallow: /api/chk/customer/baskets*
Disallow: /*payment/*
Disallow: /*session-expired*
Disallow: *404_page_not_found*
Disallow: /api/size_charts/*
Disallow: /api/search/product/*
Disallow: /*|*
Disallow: /*%7C*
Disallow: /*ozworld*
Disallow: */order-details
Disallow: */confirmation
 
Allow: /*-*-*-*-*.js*
Allow: /*-*-*-*-*.json*
Allow: /*-*-*-*-*.css*
Allow: /*-*-*-*-*.svg*
Allow: /*-*-*-*-*.png*
Allow: /*-*-*-*-*.gif*
Allow: /*-*-*-*-*.jpg*
Allow: /*-*-*-*-*.jpeg*
Allow: /*-*-*-*-*.webp*
Allow: /*-*-*-*-*.woff2*
Allow: /*-*-*-*-*.html*
Allow: /*-*-*-*-*.xml*
Allow: /*/*.html*
Allow: /*size_charts/*-*-*-*-*
Allow: /*storefront/*-*-*-*-*
Allow: /*blog/*-*-*-*-*
Allow: /*blogs/*-*-*-*-*
Allow: /*api/*-*-*-*-*
Allow: /*hilfe/*-*-*-*-*

Disallow: /*-*-*-*-*

# New Values:
Disallow: /*outdoor_gifts*
Disallow: /*test_plp_*
Disallow: /*unisex*
Disallow: /*season_sale*

#Taxonomy Values:
Disallow: /*?*collection* 
Disallow: /*?*campaignplp* 
Disallow: /*?*personalize* 
Disallow: /*?*multi_age_gender* 
Disallow: /*?*gendersub* 
Disallow: /*?*age* 
Disallow: /*?*searchcolor* 
Disallow: /*?*v_size* 
Disallow: /*?*partner* 
Disallow: /*?*featurefilters* 
Disallow: /*?*surface* 
Disallow: /*?*foottype* 
Disallow: /*?*brand* 
Disallow: /*?*sportsubsub* 
Disallow: /*?*sportsub* 
Disallow: /*?*sustainability* 
Disallow: /*?*functions* 
Disallow: /*?*bestfor* 
Disallow: /*?*sport* 
Disallow: /*?*technology* 
Disallow: /*?*productlinestyle* 
Disallow: /*?*closure* 
Disallow: /*?*producttype* 
Disallow: /*?*features* 
Disallow: /*?*division* 
Disallow: /*?*outlet* 
Disallow: /*?*shoefinder* 
Disallow: /*?*new_arrivals* 
Disallow: /*?*pattern* 
Disallow: /*?*product_fit* 
Disallow: /*?*back_length* 
Disallow: /*?*neckline* 
Disallow: /*?*base_material* 
Disallow: /*?*rise*
Disallow: /*?*price_min*
Disallow: /*?*price_max*
Disallow: /*?*sleeve_length*
Disallow: /*?*gender* 
Disallow: /*?_remoteinclude*

# Other parameters:
Disallow: /*?customize
Disallow: /*?*prefn1=*
Disallow: /*?*prefv1=*
Disallow: /*?=$
Disallow: /*?_=*
Disallow: /*?lang=*
Disallow: /*?itemselector=*
Disallow: /*?itemSelector=*
Disallow: /*?sge=*
Disallow: /*?*gn*
Disallow: /*?*strCountry_adidascom*
Disallow: /*?*sz*

User-agent: Baiduspider
Disallow: /

User-Agent: AhrefsBot 
Crawl-delay: 10 

User-Agent: Pinterestbot 
Crawl-delay: 10
Sitemap: https://www.adidas.de/glass/sitemaps/adidas/DE/de/sitemap-index.xml
Sitemap: https://www.adidas.de/glass/sitemaps/adidas/DE/en/sitemap-index.xml
"""
def checkUrl(url):
   rp = urllib.robotparser.RobotFileParser()
   #rp.set_url("https://www.adidas.de/robots.txt")
   #rp.read()

   # since read hangs somehow we parse it directly
   rp.parse(robots_txt_content)
   result = rp.can_fetch("*", url)

   #result = rp.can_fetch("*", '/*-*-*-*-*.svg*')

   return result

   #allow = re.match('adidas.de/*-*-*-*-*', 'adidas.de/grand-court-cloudfoam-comfort-schuh/HP2534.html')

   #allow = re.match('adidas.de/*-*-*-*-*', 'adidas.de/grand-court-cloudfoam-comfort-schuh/HP2534.html')

   #print(allow)