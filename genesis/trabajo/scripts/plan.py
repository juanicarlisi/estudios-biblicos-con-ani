import json
V=[31,25,24,26,32,22,24,22,29,32,32,20,18,24,21,16,27,33,38,18,34,24,20,67,34,35,46,22,35,43,55,32,20,31,29,43,36,30,23,23,57,38,34,34,28,34,31,22,33,26]
# (desde, hasta, título, parte)
P=[
("1:1","1:19","En el principio: luz, cielo, tierra y lumbreras","I"),
("1:20","2:3","Vida en abundancia, el hombre a imagen de Dios y el día de reposo","I"),
("2:4","2:25","El huerto, el mandato y la primera boda","I"),
("3:1","3:13","La serpiente, la tentación y la caída","I"),
("3:14","3:24","Juicio, promesa y expulsión del Edén","I"),
("4:1","4:26","Caín y Abel; dos linajes","I"),
("5:1","5:32","De Adán a Noé: el libro de las generaciones","I"),
("6:1","6:22","La corrupción del mundo y el arca","I"),
("7:1","7:24","El diluvio","I"),
("8:1","8:22","Dios se acordó de Noé","I"),
("9:1","9:29","El pacto con Noé y el arco iris","I"),
("10:1","10:32","La tabla de las naciones","I"),
("11:1","11:26","Babel y la línea de Sem","I"),
("11:27","12:9","La familia de Taré y el llamado de Abram","II"),
("12:10","13:18","Abram en Egipto; Abram y Lot se separan","II"),
("14:1","14:24","La guerra de los reyes y Melquisedec","II"),
("15:1","15:21","Abram creyó a Jehová: el pacto entre los animales partidos","II"),
("16:1","16:16","Agar e Ismael: el Dios que ve","II"),
("17:1","17:27","El Dios Todopoderoso: nombres nuevos y la circuncisión","II"),
("18:1","18:15","Los tres visitantes en Mamre","II"),
("18:16","18:33","Abraham intercede por Sodoma","II"),
("19:1","19:22","Lot en Sodoma","II"),
("19:23","19:38","Fuego sobre Sodoma y Gomorra","II"),
("20:1","20:18","Abraham y Abimelec en Gerar","II"),
("21:1","21:21","Nace Isaac; Agar e Ismael en el desierto","II"),
("21:22","21:34","El pacto de Beerseba","II"),
("22:1","22:24","El monte Moriah: Dios proveerá","II"),
("23:1","23:20","Muere Sara: la cueva de Macpela","II"),
("24:1","24:27","Una esposa para Isaac: la oración en el pozo","II"),
("24:28","24:49","Rebeca y la casa de Labán","II"),
("24:50","24:67","Rebeca va con Isaac","II"),
("25:1","25:18","Muere Abraham; los descendientes de Ismael","II"),
("25:19","25:34","Esaú y Jacob: la primogenitura","III"),
("26:1","26:22","Isaac en Gerar: la promesa renovada y los pozos","III"),
("26:23","26:35","Beerseba: Dios se aparece a Isaac","III"),
("27:1","27:29","Jacob arrebata la bendición","III"),
("27:30","27:46","El llanto de Esaú y la huida de Jacob","III"),
("28:1","28:22","Betel: la escalera y la puerta del cielo","III"),
("29:1","29:30","Jacob, Raquel y el engaño de Labán","III"),
("29:31","30:24","Los hijos de Jacob","III"),
("30:25","30:43","Jacob prospera con los rebaños","III"),
("31:1","31:24","Jacob huye de Labán","III"),
("31:25","31:55","Labán alcanza a Jacob: el pacto de Galaad","III"),
("32:1","32:21","Jacob se prepara para encontrar a Esaú","III"),
("32:22","33:20","Peniel: Jacob lucha con Dios y se reconcilia con Esaú","III"),
("34:1","34:31","Dina y la venganza en Siquem","III"),
("35:1","35:29","De vuelta a Betel; mueren Raquel e Isaac","III"),
("36:1","36:43","Los descendientes de Esaú","III"),
("37:1","37:17","José, el soñador","IV"),
("37:18","37:36","José vendido por sus hermanos","IV"),
("38:1","38:30","Judá y Tamar","IV"),
("39:1","39:23","José en casa de Potifar","IV"),
("40:1","40:23","José interpreta sueños en la cárcel","IV"),
("41:1","41:32","Los sueños de Faraón","IV"),
("41:33","41:57","José gobernador de Egipto","IV"),
("42:1","42:24","Los hermanos de José bajan a Egipto","IV"),
("42:25","43:15","El dinero en los costales; Benjamín","IV"),
("43:16","43:34","El banquete en casa de José","IV"),
("44:1","44:17","La copa de plata","IV"),
("44:18","44:34","Judá se ofrece en lugar de Benjamín","IV"),
("45:1","45:28","Yo soy José","IV"),
("46:1","46:34","Jacob baja a Egipto","IV"),
("47:1","47:31","Jacob ante Faraón; el hambre en Egipto","IV"),
("48:1","48:22","Jacob bendice a Efraín y Manasés","IV"),
("49:1","49:12","Las bendiciones de Jacob: de Rubén a Judá","IV"),
("49:13","49:33","Las bendiciones de Jacob: de Zabulón a Benjamín; muere Jacob","IV"),
("50:1","50:26","«Dios lo encaminó a bien»: el final de Génesis","IV"),
]
def idx(r):
    c,v=map(int,r.split(':')); return sum(V[:c-1])+v
dias=[];prev=0
for i,(a,b,t,p) in enumerate(P,1):
    ia,ib=idx(a),idx(b)
    assert ia==prev+1,(a,prev); prev=ib
    dias.append({'dia':i,'desde':a,'hasta':b,'titulo':t,'parte':p,'versiculos':ib-ia+1})
assert prev==1533
json.dump(dias,open('/home/user/trabajo/plan/plan.json','w'),ensure_ascii=False,indent=1)
import statistics
vs=[d['versiculos'] for d in dias]
print(len(dias),'días; promedio',round(statistics.mean(vs),1),'min',min(vs),'max',max(vs))
for p in 'I II III IV'.split(): print(p,sum(1 for d in dias if d['parte']==p))
