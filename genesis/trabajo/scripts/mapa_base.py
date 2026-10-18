"""Genera la geometría base (SVG paths) del Cercano Oriente para los mapas del estudio."""
import shapefile, json, math
from shapely.geometry import shape, box, mapping
from shapely.ops import unary_union
G='/home/user/trabajo/geo/'
LON0,LON1,LAT0,LAT1=24.0,52.0,21.0,42.5
W=1000
K=math.cos(math.radians((LAT0+LAT1)/2))
H=W*(LAT1-LAT0)/((LON1-LON0)*K)
def P(lon,lat): return ((lon-LON0)/(LON1-LON0)*W, (LAT1-lat)/(LAT1-LAT0)*H)
clip=box(LON0,LAT0,LON1,LAT1)
def path(geom,simp=0.01):
    geom=geom.simplify(simp,preserve_topology=True)
    out=[]
    def ring(coords,close=True):
        pts=[P(x,y) for x,y in coords]
        return 'M'+' L'.join(f'{x:.1f},{y:.1f}' for x,y in pts)+(' Z' if close else '')
    gs=getattr(geom,'geoms',[geom])
    for g in gs:
        if g.geom_type=='Polygon':
            out.append(ring(g.exterior.coords)); out+= [ring(i.coords) for i in g.interiors]
        elif g.geom_type=='LineString': out.append(ring(g.coords,False))
        elif g.geom_type in('MultiLineString','MultiPolygon','GeometryCollection'):
            out.append(path(g,0))
    return ' '.join(out)
land=unary_union([shape(s.__geo_interface__).intersection(clip) for s in shapefile.Reader(G+'ne_10m_land/ne_10m_land.shp').shapes() if shape(s.__geo_interface__).intersects(clip)])
lakes=[]; rivers={}
rl=shapefile.Reader(G+'ne_10m_lakes/ne_10m_lakes.shp')
fn=[f[0] for f in rl.fields[1:]]
for sr in rl.shapeRecords():
    g=shape(sr.shape.__geo_interface__)
    if g.intersects(clip):
        rec=dict(zip(fn,sr.record)); lakes.append((rec.get('name') or '',g.intersection(clip)))
rr=shapefile.Reader(G+'ne_10m_rivers_lake_centerlines/ne_10m_rivers_lake_centerlines.shp')
fn=[f[0] for f in rr.fields[1:]]
for sr in rr.shapeRecords():
    g=shape(sr.shape.__geo_interface__)
    if g.intersects(clip):
        rec=dict(zip(fn,sr.record)); nm=rec.get('name') or rec.get('name_en') or ''
        rivers.setdefault(nm,[]).append(g.intersection(clip))
out={'viewBox':f'0 0 {W} {H:.0f}','bbox':[LON0,LON1,LAT0,LAT1],'K':K,'W':W,'H':H,
     'tierra':path(land,0.02),
     'lagos':{n:path(g,0.005) for n,g in lakes},
     'rios':{n:path(unary_union(gs),0.01) for n,gs in rivers.items()}}
json.dump(out,open('/home/user/trabajo/mapas/base.json','w'))
print('H',round(H),'lagos',[n for n,_ in lakes][:30]); print('rios',list(rivers)[:60])
print('tamaño tierra',len(out['tierra']))
