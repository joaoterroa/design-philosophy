const assert=require('node:assert/strict');const fs=require('node:fs');const path=require('node:path');const root=path.resolve(__dirname,'../app');
const tokens=fs.readFileSync(path.join(root,'tokens.css'),'utf8');const css=fs.readFileSync(path.join(root,'style.css'),'utf8');const html=fs.readFileSync(path.join(root,'index.html'),'utf8');
const vars=s=>Object.fromEntries([...s.matchAll(/--([\w-]+):\s*([^;]+);/g)].map(m=>[m[1],m[2].trim()]));const light=vars(tokens.split(':root[data-theme=dark]')[0]);const dark=vars(tokens.split(':root[data-theme=dark]')[1].split(':root[data-display=tv]')[0]);
assert(!/#[\da-f]{3,8}\b|rgba?\(|hsla?\(/i.test(css),'Literal colour outside tokens');
for(const p of ['font-size','border-radius','box-shadow','animation-duration','transition-duration'])for(const m of css.matchAll(new RegExp('(?:^|[;{])'+p+':([^;}]+)','g')))assert(/var\(--/.test(m[1]),`Untokenized ${p}: ${m[1]}`);
assert(!/\d(?:px|rem)\b/.test(css.replace(/@media[^\{]+\{/g,'')),'Literal spatial size outside tokens');
const colors=Object.keys(light).filter(k=>light[k].startsWith('#'));assert.deepEqual(colors.sort(),Object.keys(dark).filter(k=>dark[k].startsWith('#')).sort(),'Theme colour mismatch');
const lum=h=>{const c=[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)/255).map(x=>x<=.04045?x/12.92:((x+.055)/1.055)**2.4);return .2126*c[0]+.7152*c[1]+.0722*c[2]};const ratio=(a,b)=>{const x=[lum(a),lum(b)].sort((a,b)=>b-a);return(x[0]+.05)/(x[1]+.05)};
const checks=[];for(const [name,t]of [['light',light],['dark',{...light,...dark}]]){
 for(const fg of ['fg','muted','brand','critical','caution','healthy'])for(const bg of ['bg','surface']){const r=ratio(t[fg],t[bg]);assert(r>=4.5,`${name} ${fg}/${bg} ${r}`);checks.push({theme:name,pair:`${fg}/${bg}`,ratio:+r.toFixed(2)})}
 for(const [fg,bg,min]of [['critical','critical-bg',4.5],['fg','critical-bg',4.5],['muted','critical-bg',4.5],['caution','caution-bg',4.5],['muted','caution-bg',4.5],['chart','bg',3],['focus','bg',3],['focus','surface',3]]){const r=ratio(t[fg],t[bg]);assert(r>=min,`${name} ${fg}/${bg} ${r}`);checks.push({theme:name,pair:`${fg}/${bg}`,ratio:+r.toFixed(2)})}
}
assert(html.indexOf('tokens.css')<html.indexOf('style.css'),'Token load order');assert(fs.readFileSync(path.resolve(root,'fixtures.js')).equals(fs.readFileSync(path.resolve(root,'../../fixtures.js'))),'Fixtures changed');
fs.writeFileSync(path.resolve(__dirname,'contrast.json'),JSON.stringify(checks,null,2));console.log(`PASS: token wiring, literal guards, theme parity, unchanged fixtures, ${checks.length} contrast checks. Minimum ratio ${Math.min(...checks.map(c=>c.ratio))}`);
