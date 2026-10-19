import fs from 'node:fs';
import assert from 'node:assert/strict';
const dir=new URL('../app/',import.meta.url);
const css=fs.readFileSync(new URL('app.css',dir),'utf8');
const tokens=fs.readFileSync(new URL('tokens.css',dir),'utf8');
const html=fs.readFileSync(new URL('index.html',dir),'utf8');
const vars=s=>Object.fromEntries([...s.matchAll(/--([\w-]+):\s*([^;]+);/g)].map(m=>[m[1],m[2].trim()]));
const light=vars(tokens.split(':root[data-theme="dark"]')[0]);
const dark=vars(tokens.split(':root[data-theme="dark"]')[1].split(':root[data-display')[0]);
const lum=hex=>{let [r,g,b]=[1,3,5].map(i=>parseInt(hex.slice(i,i+2),16)/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return .2126*r+.7152*g+.0722*b};
const contrast=(a,b)=>{let [x,y]=[lum(a),lum(b)].sort((a,b)=>b-a);return (x+.05)/(y+.05)};
assert(!/#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(/gi.test(css),'Literal colour in component CSS');
for(const declaration of [...css.matchAll(/(?:font-size|border-radius|box-shadow):\s*([^;}]+)/g)])assert(declaration[1].startsWith('var('),'Non-token type, radius or shadow: '+declaration[0]);
for(const k of Object.keys(light).filter(k=>light[k].startsWith('#')))assert(k in dark,'Missing dark token: '+k);
const defined=new Set([...tokens.matchAll(/--([\w-]+):/g)].map(m=>m[1]));
for(const m of css.matchAll(/var\(--([\w-]+)\)/g))assert(defined.has(m[1]),'Undefined token '+m[1]);
assert(html.indexOf('tokens.css')<html.indexOf('app.css'),'Tokens must precede component styles');
const report=[];
for(const [theme,t] of [['light',light],['dark',{...light,...dark}]]){
 for(const fg of ['fg','muted'])for(const bg of ['bg','surface','critical-bg']){const r=contrast(t[fg],t[bg]);assert(r>=4.5,`${theme} ${fg}/${bg}: ${r}`);report.push({theme,fg,bg,ratio:+r.toFixed(2)})}
 for(const [fg,bg] of [['critical','critical-bg'],['critical','surface'],['caution','caution-bg'],['caution','surface'],['teal','surface'],['teal','bg'],['white','navy'],['header-muted','navy']]){const r=contrast(t[fg],t[bg]);assert(r>=4.5,`${theme} ${fg}/${bg}: ${r}`);report.push({theme,fg,bg,ratio:+r.toFixed(2)})}
 assert(contrast(t['control-line'],t['surface'])>=3,`${theme}: control boundary contrast`);
 assert(contrast(t['teal-fill'],t['bar-track'])>=3,`${theme}: chart graphic contrast`);
}
assert(fs.readFileSync(new URL('fixtures.js',dir),'utf8')===fs.readFileSync(new URL('../../fixtures.js',dir),'utf8'),'Copied fixture changed');
fs.writeFileSync(new URL('contrast.json',import.meta.url),JSON.stringify(report,null,2));
console.log('PASS: token use, token definitions, theme parity, text and chart contrast, stylesheet wiring, unchanged fixture.');
