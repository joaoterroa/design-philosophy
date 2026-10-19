import fs from 'node:fs';
import assert from 'node:assert/strict';
const root=new URL('../app/',import.meta.url);
const tokens=fs.readFileSync(new URL('tokens.css',root),'utf8');
const css=fs.readFileSync(new URL('app.css',root),'utf8').replace(/\/\*[\s\S]*?\*\//g,'');
assert.equal((css.match(/#[\da-f]{3,8}\b|rgba?\(|hsla?\(/gi)||[]).length,0,'literal colors outside tokens');
assert.equal((css.replace(/@media\([^)]*\)/g,'').match(/-?\d+(?:\.\d+)?px/g)||[]).length,0,'sizes outside tokens (breakpoints excepted)');
assert.equal((css.match(/font-size:\s*(?!var\()[^;}]+/g)||[]).length,0,'font sizes outside tokens');
for(const m of css.matchAll(/border-radius:\s*([^;}]+)/g)) assert.ok(/var\(|^0$|^50%$/.test(m[1]),'radius outside tokens: '+m[1]);
assert.ok(fs.readFileSync(new URL('index.html',root),'utf8').indexOf('tokens.css')<fs.readFileSync(new URL('index.html',root),'utf8').indexOf('app.css'));
assert.equal(fs.readFileSync(new URL('fixtures.js',root),'utf8'),fs.readFileSync(new URL('../../fixtures.js',import.meta.url),'utf8'),'fixture modified');
const parse=s=>Object.fromEntries([...s.matchAll(/--([\w-]+):\s*(#[\da-f]{6});/gi)].map(m=>[m[1],m[2]]));
const light=parse(tokens.split(':root[data-theme=dark]')[0]);
const dark=parse(tokens.split(':root[data-theme=dark]')[1].split(':root[data-display')[0]);
assert.deepEqual(Object.keys(light).sort(),Object.keys(dark).sort(),'theme token parity');
function luminance(h){const c=[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return .2126*c[0]+.7152*c[1]+.0722*c[2]}
function ratio(a,b){const [x,y]=[luminance(a),luminance(b)].sort((a,b)=>b-a);return(x+.05)/(y+.05)}
let results=[];
for(const [name,t] of [['light',light],['dark',dark]]){
 const pairs=[...['fg','muted','brand-ink','critical','warning','good'].flatMap(f=>['bg','surface'].map(b=>[f,b])),['fg','critical-bg'],['muted','critical-bg'],['critical','critical-bg'],['warning','warning-bg'],['white','brand']];
 for(const [fg,bg] of pairs){const v=ratio(t[fg],t[bg]);assert.ok(v>=4.5,`${name} ${fg} / ${bg} = ${v}`);results.push({theme:name,foreground:fg,background:bg,ratio:+v.toFixed(2)});}
 for(const [fg,bg] of [['control-line','surface'],['control-line','bg'],['chart','soft'],['focus','bg'],['focus','surface'],['critical','critical-bg']])assert.ok(ratio(t[fg],t[bg])>=3,`${name} graphic ${fg}/${bg}`);
}
fs.writeFileSync(new URL('contrast.json',import.meta.url),JSON.stringify(results,null,2));
console.log(`Design guard passed: ${results.length} text pairs, meaningful graphics, theme parity, font and color tokens, fixture identity.`);
