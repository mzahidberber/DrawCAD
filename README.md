
<img src="cad.png">
<hr>
<h6 align="center">
  <a href="https://docs.drawprogram.org">DrawCAD |</a>
  <a href="https://docs.drawprogram.org/doc">Doc |</a>
  <a href="https://docs.drawprogram.org/api">Api |</a>
  <a href="https://docs.drawprogram.org/geo">Geo |</a>
  <a href="https://docs.drawprogram.org/auth">Auth</a>
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
    server="https://localhost"
```

<h3>Başlangıç</h3>
<p>Kullanmak için kaynak kodunu başlatabilirsiniz.Başlatmadan önce bazı python kütüphanelerinin yüklü olması gereklidir.</p>

```
pip install -r requirements.txt
python Run.py
```


<h3>Hizmetler</h3>
<div align="center">
  <img src="drawcad.png"  style="width:70%;">
</div>
<p>
DrawCAD yazılımı arka uçta dört adet servis ön uçta bir adet clientten oluşan modüler bir yapıya sahiptir. Arka uçtaki servislerin üç tanesi restapi tipinde olup json veri tipiyle birbirleriyle haberleşmekte dördünce serviste mysql servis bu servistede datalar tutulmaktadır.Api ve auth hizmetleri C# ile geo ve client python diliyle yazılmıştır.Hizmetler serverda docker ile sanallaştırılmış ve birbirleriyle iletişime geçirilmiştir.
</p>
<h3>Başlangıç</h3>
<p>Kullanmak için docker compose kullanabilirsiniz.Hizmetlerin imagelerini dockerhubtan indirir ve çalıştırır.</p>

```
docker-compose up -d
```


