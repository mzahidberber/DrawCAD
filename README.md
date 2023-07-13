
<img src="cad.png">
<hr>
<h6 align="center">
  <a href="https://drawprogram.org/">DrawCAD |</a>
  <a href="https://drawprogram.org/Home/DrawCAD">Doc |</a>
  <a href="https://drawprogram.org/Home/DrawApi">Api |</a>
  <a href="https://drawprogram.org/Home/DrawGeo">Geo |</a>
  <a href="https://drawprogram.org/Home/DrawAuth">Auth</a>
</h6>

<hr>
<h3>DrawCAD</h3>
<p>
Teknik çizim programı olan DrawCAD ile temel seviyede teknik çizimler gerçekleştirilebilir.Mimarlık ve mühendislik gibi alanların teknik çizimlerinde kullanılmak üzere tasarlanmıştır.Line,polyline,rectangle ve circle gibi birçok komut ile çizimler yapılıp move,mirror ve scale gibi komutlarla bu çizimler düzenlenebilir.Snap araçlarıyla nokta yakalama işlemleri gerçekleştirilip polar mod ve ortho mod ile dik ve açılı bir şekilde çizim yapılabilir.Layer sistemiyle çizilen elemanların çizgi kalınlığı,rengi ve kalem tipi gibi özellikleri üzerinde düzenlemeler yapılabilir.Programı kullanmaya başlamadan önce kullanıcı adı ve şifre ile kayıt yapılmalı daha sonra giriş gerçekliştirilmelidir.Yapılan çizimler bulut sistemine veya kendine özgü dosya formatı(.df) ile yerel olarak kaydedilebilmektedir.

</p>
<p>
Arayüz dört adet hizmeti kullanarak çalışmaktadır.Hizmetler varsayılan olarak
<a href="https://github.com/mzahidberber/Draw-UI-Python">drawprogram.org</a> adresinde çalışmaktadır ama kendiniz localde test etmek isterseniz docker compose ile kullanabilirsiniz.Hizmetleri localde kullabilmek için Core/Url/Urls.py dosyasındaki local için olan adresleri etkinleştirmelisiniz.
</p>
```
class Urls(enum.Enum):
    drawgeo="http://localhost:5001/geo"
    drawapi= "http://localhost:5000"
    drawauth= "http://localhost:5002"
    server="https://drawprogram.org"
```

<h3>Başlangıç</h3>
<p>Kullanmak için .exe dosyasını veya kaynak kodunu başlatabilirsiniz.Kaynak kodunu kullancak iseniz başlatmadan önce bazı python kütüphanelerinin yüklü olması gereklidir.</p>

```
PyQt5 5.15.7
cryptography 41.0.1
arrow 1.2.3
shapely 2.0.1
multipledispatch 0.6.0
numpy 1.23.3
```



<p>Paketlerin yüklü olduğundan emin olduktan sonra kullanmak için Run.py dosyasını çalıştırmalısınız.</p>
```
python Run.py
```

<h3>Hizmetler</h3>
<img src="drawcad.png">
<p>
DrawCAD yazılımı arka uçta dört adet servis ön uçta bir adet clientten oluşan modüler bir yapıya sahiptir. Arka uçtaki servislerin üç tanesi restapi tipinde olup json veri tipiyle birbirleriyle haberleşmekte dördünce serviste mysql servis bu servistede datalar tutulmaktadır.Api ve auth hizmetleri C# ile geo ve client python diliyle yazılmıştır.Hizmetler serverda docker ile sanallaştırılmış ve birbirleriyle iletişime geçirilmiştir.
</p>
<h3>Başlangıç</h3>
<p>Kullanmak için docker compose kullanabilirsiniz.Hizmetlerin imagelerini dockerhubtan indirir ve çalıştırır.</p>
```
docker-compose up -d
```


