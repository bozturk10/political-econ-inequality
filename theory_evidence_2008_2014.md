# Brezilya–Meksika: araştırma sorusu için ilk veri seti (2008–2014)

Derleme tarihi: 16 Kasım 2026. Makine okunur tablo: [`data/theory_indicators_2008_2014.csv`](data/theory_indicators_2008_2014.csv). Her satırda ülke, yıl, gösterge, değer, birim, kaynak serisi ve bağlantı bulunur. 45 gözlem vardır; eksik yıllar tahmin edilmedi.

## Sonuç değişkenleri

| Gösterge | Brezilya 2008 → 2014 | Meksika 2008 → 2014 |
|---|---:|---:|
| Gini (0–100) | 54,0 → 52,1 (−1,9 puan) | 50,8 → 48,9 (−1,9 puan) |
| En yoksul %20'nin gelir payı | %3,2 → %3,6 (+0,4 yüzde puanı) | %3,9 → %4,7 (+0,8 yüzde puanı) |

Kaynak: Dünya Bankası WDI, [Gini](https://data.worldbank.org/indicator/SI.POV.GINI) ve [en yoksul %20 gelir payı](https://data.worldbank.org/indicator/SI.DST.FRST.20). Bunlar aynı değişken değildir: Gini tüm dağılımı, ikinci gösterge alt dilimin toplam gelir payını özetler.

## Teorilere karşılık gelen göstergeler

| Mekanizma | Toplanan karşılaştırma | İlk okuma |
|---|---|---|
| Nakit transferlerinin erişimi (Haggard–Kaufman / Garay) | 2012'de koşullu nakit transferi kategorisinin en yoksul %20'ye erişimi: Brezilya %27,3; Meksika %62,7. Tüm nüfusa erişim: %17,2; %24,2. | Meksika bu anlık ölçülerde daha yüksek. “Brezilya'nın CCT kapsaması daha genişti” varsayımı desteklenmiyor. |
| Transferlerin hedeflenmesi ve yeterliliği | 2012'de toplam CCT ödemelerinin en yoksul %20'ye giden payı: Brezilya %27,6; Meksika %53,8. Bu dilimdeki yararlanıcı hanelerde transferin refah/gelire oranı: %18,0; %22,5. | Tek yıllık karşılaştırma, 2008–2014 değişiminin nedeni olarak okunamaz. |
| Emek piyasası / asgari ücret (Huber–Stephens) | Reel ulusal asgari ücret endeksi, 2000=100: Brezilya 160,8 → 203,6 (**%26,6 artış**); Meksika 100,5 → 101,7 (**%1,2 artış**). | Brezilya'da reel asgari ücret çok daha hızlı yükselmiş. Endeks seviyeleri ülkeler arası ücret düzeyi karşılaştırması değildir. |
| İşçi örgütlenmesi (Huber–Stephens) | Sendikalaşma oranı, çalışanlar içinde: Brezilya %19,4 → %17,8; Meksika %15,6 → %13,6. | İki ülkede de düşüş var. Sendika üyeliği siyasal mobilizasyonun doğrudan ölçüsü değildir. |
| İşgücü segmentasyonu | Kayıt dışı istihdam, 2012 → 2014: Brezilya %41,6 → %40,7; Meksika %60,3 → %58,7. | Meksika'da düzey daha yüksek; Brezilya'nın 2008 verisi bu ILO serisinde yok. |
| Parti/siyasal bağlam (Garay; Huber–Stephens) | 2008–2014'te Brezilya'da PT (Lula ve Dilma); Meksika'da 2012'ye dek PAN (Calderón), ardından PRI (Peña Nieto). | Dönem kodlaması var; seçmen rekabeti veya kayıt dışı kesimlerin mobilizasyonu için güvenilir ortak yıllık ölçü henüz yok. |

Kaynaklar: [Dünya Bankası ASPIRE veri ve tanımları](https://www.worldbank.org/en/data/datatopics/aspire/documentation), [ASPIRE ham veri](https://datacatalogfiles.worldbank.org/ddh-published/0037942/DR0087109/ASPIRE%20performance%20indicators.zip), [ILO reel asgari ücret, Tablo 10](https://www.ilo.org/sites/default/files/wcmsp5/groups/public/%40americas/%40ro-lima/documents/publication/wcms_450098.pdf), [ILOSTAT toplu veri](https://ilostat.ilo.org/data/bulk/); siyasal dönemlerin kaynakları [`data/cct_government_timeline_sources.md`](data/cct_government_timeline_sources.md) içindedir.

## Yorum sınırları ve eksik kalanlar

- ASPIRE değerleri **tek tek Bolsa Família / Oportunidades idari kayıtları değil**, hane anketlerinden hesaplanan koşullu transfer *kategorisi* değerleridir. En yoksul beşte birlik grup transfer öncesi refaha göre sıralanmıştır. Brezilya için 2008 ve 2014 ASPIRE gözlemi yoktur; bu yüzden iki ülkenin CCT değişimini aynı uç yıllarla karşılaştırmıyoruz. ASPIRE'nin Brezilya 2012–2015 serisindeki büyük sıçrama da anket/tanım farkı denetlenmeden trend sayılmamalı.
- Sosyal harcamaların GSYH'ye oranı için [OECD SOCX](https://www.oecd.org/en/data/datasets/social-expenditure-database-socx.html) ve [CEPALSTAT](https://statistics.cepal.org/portal/cepalstat/dashboard.html?area_id=411&indicator_id=3127&lang=en) iki uygun adaydır; bu dosyada 2008–2014 için **doğrulanmış ortak bir sayısal seri henüz yoktur**. Farklı kapsamlı veya farklı yıllara ait harcama sayılarını yan yana koymadık.
- Garay'ın siyasal rekabet ve *outsider* mobilizasyonu mekanizması için yalnızca hükümet/parti tarihçesi hazır. Bu, mekanizmayı sınamak için yeterli değildir; ülke raporları ve program genişleme kararlarıyla süreç izleme gerekir.
- Bu veri, iki ülkeyi betimleyerek teorileri tartışmaya yarar; transfer, ücret veya iktidar partisinin eşitsizlikteki değişime **nedensel katkısını** tek başına ayıramaz. Ayrıca Brezilya'nın Dünya Bankası serisi 2008–2014 içinde PNAD → PNAD Contínua geçişini aşar; bu nedenle uç yıl farkları temiz bir zaman serisi değişimi olarak sunulmamalıdır. Meksika'da da 2006–2008 ve 2014–2016 arasında yöntem kırılmaları vardır; bkz. [`comparison_window_decision.md`](comparison_window_decision.md).
