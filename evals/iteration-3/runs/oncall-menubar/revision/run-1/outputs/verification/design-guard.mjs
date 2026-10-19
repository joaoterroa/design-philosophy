import fs from 'node:fs';
import assert from 'node:assert/strict';
import path from 'node:path';
import {fileURLToPath} from 'node:url';
const root=path.resolve(path.dirname(fileURLToPath(import.meta.url)),'..');
const tokens=fs.readFileSync(path.join(root,'app/tokens.css'),'utf8');
const css=fs.readFileSync(path.join(root,'app/style.css'),'utf8').replace(/\/\*[\s\S]*?\*\//g,'');
const html=fs.readFileSync(path.join(root,'app/index.html'),'utf8');
const vars=s=>Object.fromEntries([...s.matchAll(/--([\w-]+):\s*([^;]+);/g)].map(m=>[m[1],m[2].trim()]));
const split=tokens.indexOf(':root[data-theme="dark"]');
const light=vars(tokens.slice(0,split)), darkVars=vars(tokens.slice(split)), dark={...light,...darkVars};
assert.deepEqual(css.match(/#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(/gi)||[],[],'No literal colours outside tokens');
for(const property of ['font-size','border-radius','box-shadow','transition-duration']) {
  const raw=[...css.matchAll(new RegExp(`${property}:\\s*([^;}]+)`,'g'))].map(m=>m[1].trim()).filter(v=>!v.startsWith('var('));
  assert.deepEqual(raw,[],`Use tokens for ${property}`);
}
assert.deepEqual(Object.keys(light).filter(k=>light[k].startsWith('#') && !Object.hasOwn(darkVars,k)),[],'Dark colour parity');
for(const m of css.matchAll(/var\(--([\w-]+)\)/g)) assert.ok(Object.hasOwn(light,m[1]),`Undefined token ${m[1]}`);
assert.ok(html.indexOf('tokens.css')<html.indexOf('style.css'),'Tokens must load first');
assert.equal(fs.readFileSync(path.join(root,'app/fixtures.js'),'utf8'),fs.readFileSync(path.join(root,'../fixtures.js'),'utf8'),'Fixture copy must stay identical');
const lum=hex=>{
 const [r,g,b]=[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)/255).map(c=>c<=0.04045?c/12.92:((c+0.055)/1.055)**2.4);
 return .2126*r+.7152*g+.0722*b;
};
const ratio=(a,b)=>{const[x,y]=[lum(a),lum(b)].sort((x,y)=>y-x);return(x+.05)/(y+.05)};
const pairs=[...['fg','muted'].flatMap(fg=>['bg','surface','field','health-bg'].map(bg=>[fg,bg,4.5])),['health','health-bg',4.5],['health','surface',4.5],['health','bg',4.5],['caution','caution-bg',4.5],['accent','health-bg',3],['on-accent','accent',4.5],['on-accent','accent-hover',4.5],['focus','bg',3],['focus','field',3],['line-strong','field',3],['line-strong','surface',3],['focus','health-bg',3]];
const report=[];
for(const [theme,t] of [['light',light],['dark',dark]]) for(const [fg,bg,min] of pairs){const r=ratio(t[fg],t[bg]); report.push({theme,fg,bg,ratio:+r.toFixed(2),minimum:min});assert.ok(r>=min,`${theme}: ${fg} on ${bg} is ${r.toFixed(2)} (<${min})`)}
fs.writeFileSync(path.join(root,'verification/contrast.json'),JSON.stringify(report,null,2));
console.log(`PASS: token wiring, literal guard, theme parity, fixture integrity, ${report.length} contrast pairs.`);
