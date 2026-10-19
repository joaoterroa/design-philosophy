import fs from 'node:fs';
import assert from 'node:assert/strict';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const tokens=fs.readFileSync(path.join(root,'app/tokens.css'),'utf8');
const styles=fs.readFileSync(path.join(root,'app/style.css'),'utf8');
const html=fs.readFileSync(path.join(root,'app/index.html'),'utf8');
const vars=s=>Object.fromEntries([...s.matchAll(/--([\w-]+):\s*([^;\n}]+)/g)].map(m=>[m[1],m[2].trim()]));
const light=vars(tokens.match(/:root\s*\{([\s\S]*?)\}/)[1]);
const darkOnly=vars(tokens.match(/:root\[data-theme="dark"\]\s*\{([\s\S]*?)\}/)[1]);
const dark={...light,...darkOnly};
const colors=Object.keys(light).filter(k=>/^#[\da-f]{6}$/i.test(light[k]));
assert.deepEqual(colors.filter(k=>!(k in darkOnly)),[],'Theme color parity');
assert.equal(html.indexOf('tokens.css')<html.indexOf('style.css'),true,'Tokens load first');
assert.deepEqual(styles.match(/#[\da-f]{3,8}\b|rgba?\(|hsla?\(/gi)||[],[],'No component color literals');
for(const prop of ['font-size','border-radius','box-shadow','transition-duration','animation-duration']){
 const unscaled=[...styles.matchAll(new RegExp('(?:^|[;{])\\s*'+prop+':([^;}]+)','g'))].map(m=>m[1]).filter(v=>!v.includes('var(')&&!['0','none','inherit'].includes(v.trim()));
 assert.deepEqual(unscaled,[],`${prop} uses tokens`);
}
const lum=hex=>{
 const c=[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)/255).map(c=>c<=.04045?c/12.92:((c+.055)/1.055)**2.4);
 return .2126*c[0]+.7152*c[1]+.0722*c[2];
};
const contrast=(a,b)=>{const l=[lum(a),lum(b)].sort((a,b)=>b-a);return(l[0]+.05)/(l[1]+.05)};
const pairs=[];
for(const fg of ['fg','muted','heading'])for(const bg of ['bg','surface','subtle','critical-bg'])pairs.push([fg,bg,4.5]);
pairs.push(['critical','critical-bg',4.5],['critical','surface',4.5],['critical','bg',4.5],['warning','warning-bg',4.5],['warning','surface',4.5],['quiet','quiet-bg',4.5],['teal','surface',4.5],['teal','bg',4.5],['nav-fg','nav',4.5],['nav-muted','nav',4.5],['bar','track',3],['focus','surface',3],['focus','bg',3]);
const results=[];
for(const [theme,t]of [['light',light],['dark',dark]])for(const [fg,bg,min]of pairs){
 const ratio=contrast(t[fg],t[bg]);results.push({theme,fg,bg,ratio:+ratio.toFixed(2),minimum:min});
 assert.ok(ratio>=min,`${theme}: ${fg} on ${bg}: ${ratio.toFixed(2)}`);
}
assert.equal(fs.readFileSync(path.join(root,'app/fixtures.js'),'utf8'),fs.readFileSync(path.join(root,'../fixtures.js'),'utf8'),'Fixture copy unchanged');
fs.writeFileSync(path.join(root,'verification/contrast-results.json'),JSON.stringify(results,null,2));
console.log(`PASS: token use, theme parity, offline wiring, fixture copy and ${results.length} contrast pairs.`);
