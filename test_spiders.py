from spiders.chi_spider import CHISpider
from spiders.informa_spider import InformaSpider

print("Testing CHISpider...")
c = CHISpider("CONF-CHI", "Test CHI", "https://www.immunogenicitysummit.com/22/immunogenicity-prediction", topic="Topic")
res_c = c.extract()
print(f"CHI Extracted {len(res_c)} speakers.")
if res_c:
    print("Sample CHI Speaker:", res_c[0])

print("\nTesting InformaSpider...")
i = InformaSpider("CONF-INF", "Test Informa", "https://informaconnect.com/bioprocessinternational/speakers/", topic="Topic")
res_i = i.extract()
print(f"Informa Extracted {len(res_i)} speakers.")
if res_i:
    print("Sample Informa Speaker:", res_i[0])

