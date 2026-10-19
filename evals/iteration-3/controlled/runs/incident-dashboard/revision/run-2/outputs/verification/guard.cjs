const fs=require('node:fs'),assert=require('node:assert/strict'),path=require('node:path');
const root=path.resolve(__dirname,'../app');
const tokens=fs.readFileSync(path.join(root,'tokens.css'),'utf8');
const css=fs.readFileSync(path.join(root,'app.css'),'utf8');
const vars=s=>Object.fromEntries([...s.matchAll(/--([\w-]+):\s*([^;}]+)(?:[;}]|$)/g)].map(m=>[m[1],m[2].trim()]));
const light=vars(tokens.match(/:root\{([^}]+)/)[1]),dark=vars(tokens.match(/:root\[data-theme="dark"\]\{([^}]+)/)[1]);
assert(!/#[0-9a-f]{3,8}\b|rgba?\(|hsla?\(/i.test(css),'literal colour outside tokens');
for(const rule of css.matchAll(/(?:font-size|border-radius|box-shadow|transition-duration):([^;}]+)/g))assert(/var\(--/.test(rule[1]),'untokenized style '+rule[0]);
const defined=vars(tokens);for(const m of css.matchAll(/var\(--([\w-]+)\)/g))assert(m[1] in defined,'undefined '+m[1]);
for(const k of Object.keys(light).filter(k=>/^#/.test(light[k])))assert(k in dark,'dark parity '+k);
const lum=h=>{const c=[1,3,5].map(i=>parseInt(h.slice(i,i+2),16)/255).map(v=>v<=.04045?v/12.92:((v+.055)/1.055)**2.4);return c[0]*.2126+c[1]*.7152+c[2]*.0722};
const ratio=(a,b)=>{let x=lum(a),y=lum(b);return(Math.max(x,y)+.05)/(Math.min(x,y)+.05)};
const scores=[];for(const [name,t]of [['light',light],['dark',{...light,...dark}]]){for(const fg of ['fg','muted'])for(const bg of ['bg','surface','surface-alt','critical-bg']){let r=ratio(t[fg],t[bg]);assert(r>=4.5,`${name} ${fg}/${bg} ${r}`);scores.push([name,fg,bg,+r.toFixed(2)])}for(const [fg,bg,min]of [['critical','critical-bg',4.5],['critical','surface',4.5],['warning','warning-bg',4.5],['warning','surface',4.5],['good','bg',4.5],['chart','bg',3],['on-brand','brand',4.5],['focus','surface',3]]){let r=ratio(t[fg],t[bg]);assert(r>=min,`${name} ${fg}/${bg} ${r}`);scores.push([name,fg,bg,+r.toFixed(2)])}}
assert(fs.readFileSync(path.join(root,'fixtures.js'),'utf8')===fs.readFileSync(path.join(root,'../../fixtures.js'),'utf8'),'fixture altered');
const html=fs.readFileSync(path.join(root,'index.html'),'utf8');assert(html.indexOf('tokens.css')<html.indexOf('app.css'));
fs.writeFileSync(path.join(__dirname,'contrast.json'),JSON.stringify(scores,null,2));console.log('PASS: tokens, theme parity, contrast pairs, token wiring and unchanged fixtures');
